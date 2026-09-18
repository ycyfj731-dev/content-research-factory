from __future__ import annotations

import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MoneyPrinterTurboConfig:
    project_dir: str
    uv_command: str = "uv"
    timeout_seconds: int = 3600


class MoneyPrinterTurboAdapter:
    """CLI adapter for harry0703/MoneyPrinterTurbo."""

    def __init__(self, config: MoneyPrinterTurboConfig):
        self.config = config

    def produce(self, research_package: dict[str, Any]) -> dict[str, Any]:
        subject = self._subject(research_package)
        task_id = str(uuid.uuid4())
        proc = subprocess.run(
            [
                self.config.uv_command, "run", "python", "cli.py",
                "--video-subject", subject,
                "--task-id", task_id,
            ],
            cwd=Path(self.config.project_dir),
            text=True,
            capture_output=True,
            timeout=self.config.timeout_seconds,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"MoneyPrinterTurbo failed ({proc.returncode}): {proc.stderr.strip()}"
            )
        return {
            "status": "completed",
            "task_id": task_id,
            "stdout": proc.stdout.strip(),
            "origin_tool": "MoneyPrinterTurbo",
        }

    @staticmethod
    def _subject(research_package: dict[str, Any]) -> str:
        query = str(research_package.get("query") or "").strip()
        synthesis = research_package.get("synthesis") or {}
        platforms = synthesis.get("platform_counts") or {}
        if platforms:
            return f"{query}。参考已验证研究材料，覆盖平台：{'、'.join(platforms.keys())}"
        return query
