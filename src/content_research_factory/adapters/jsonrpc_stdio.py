from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any, Mapping


class JSONRPCStdioError(RuntimeError):
    """Raised when a JSON-RPC stdio process fails or returns invalid data."""


@dataclass(frozen=True)
class JSONRPCStdioConfig:
    command: str
    args: tuple[str, ...] = ()
    timeout_seconds: int = 60


class JSONRPCStdioClient:
    def __init__(self, config: JSONRPCStdioConfig):
        self.config = config
        self._next_id = 1

    def call(self, method: str, params: Mapping[str, Any]) -> Any:
        request_id = self._next_id
        self._next_id += 1

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": dict(params),
        }

        proc = subprocess.run(
            [self.config.command, *self.config.args],
            input=json.dumps(payload, ensure_ascii=False) + "\n",
            text=True,
            capture_output=True,
            timeout=self.config.timeout_seconds,
            check=False,
        )

        if proc.returncode != 0:
            raise JSONRPCStdioError(
                f"process failed ({proc.returncode}): {proc.stderr.strip()}"
            )

        stdout = proc.stdout.strip()
        if not stdout:
            raise JSONRPCStdioError("process returned no response")

        try:
            response = json.loads(stdout.splitlines()[-1])
        except json.JSONDecodeError as exc:
            raise JSONRPCStdioError("process returned invalid JSON") from exc

        if response.get("id") != request_id:
            raise JSONRPCStdioError("mismatched JSON-RPC response id")
        if "error" in response:
            raise JSONRPCStdioError(str(response["error"]))
        if "result" not in response:
            raise JSONRPCStdioError("JSON-RPC response has no result")

        return response["result"]
