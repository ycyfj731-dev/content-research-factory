from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AgentReachConfig:
    command: str = "agent-reach"
    platforms: tuple[str, ...] = ("twitter", "reddit", "bilibili", "xiaohongshu")
    per_platform_limit: int = 5
    timeout_seconds: int = 60


class AgentReachAdapter:
    """Cross-platform verifier following Agent-Reach's documented backend routing."""

    def __init__(self, config: AgentReachConfig):
        self.config = config

    def verify(self, query: str, *, candidates: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
        doctor = self._doctor()
        rows = []
        for platform in self.config.platforms:
            if len(rows) >= limit:
                break
            backend = self._active_backend(doctor, platform)
            command = self._command_for(platform, backend, query)
            if command is None:
                continue
            output = self._run(command)
            rows.extend(self._normalize_backend_output(platform, backend, output))
        return rows[:limit]

    def _doctor(self) -> Any:
        proc = subprocess.run(
            [self.config.command, "doctor", "--json"],
            text=True,
            capture_output=True,
            timeout=self.config.timeout_seconds,
            check=False,
        )
        if proc.returncode != 0:
            return {}
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _active_backend(doctor: Any, platform: str) -> str | None:
        if not isinstance(doctor, dict):
            return None
        candidates = doctor.get("channels") or doctor.get("platforms") or doctor
        if isinstance(candidates, dict):
            row = candidates.get(platform)
            if isinstance(row, dict):
                return row.get("active_backend") or row.get("backend")
        if isinstance(candidates, list):
            for row in candidates:
                if isinstance(row, dict) and row.get("name") == platform:
                    return row.get("active_backend") or row.get("backend")
        return None

    def _command_for(self, platform: str, backend: str | None, query: str) -> list[str] | None:
        n = str(self.config.per_platform_limit)
        if platform == "bilibili":
            return ["bili", "search", query, "--type", "video", "-n", n]
        if platform == "twitter":
            if backend and "OpenCLI" in backend:
                return ["opencli", "twitter", "search", query, "-f", "yaml"]
            return ["twitter", "search", query, "-n", n]
        if platform == "reddit":
            if backend and "OpenCLI" in backend:
                return ["opencli", "reddit", "search", query, "-f", "yaml"]
            return ["rdt", "search", query, "--limit", n]
        if platform == "xiaohongshu":
            return ["opencli", "xiaohongshu", "search", query, "-f", "yaml"]
        return None

    def _run(self, command: list[str]) -> str:
        proc = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=self.config.timeout_seconds,
            check=False,
            env=os.environ.copy(),
        )
        return proc.stdout.strip() if proc.returncode == 0 else ""

    @staticmethod
    def _normalize_backend_output(platform: str, backend: str | None, output: str) -> list[dict[str, Any]]:
        if not output:
            return []
        try:
            value = json.loads(output)
        except json.JSONDecodeError:
            try:
                import yaml
                value = yaml.safe_load(output)
            except Exception:
                value = None

        if isinstance(value, dict):
            for key in ("items", "results", "data"):
                if isinstance(value.get(key), list):
                    value = value[key]
                    break
            else:
                value = [value]
        elif not isinstance(value, list):
            value = [{"text": output}]

        rows = []
        for item in value:
            row = dict(item) if isinstance(item, dict) else {"text": str(item)}
            row.setdefault("platform", platform)
            row.setdefault("verification_backend", backend)
            row.setdefault("origin_tool", "Agent-Reach")
            rows.append(row)
        return rows
