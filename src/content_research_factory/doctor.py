from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _run(command: list[str], *, cwd: str | None = None, timeout: int = 20) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, "", str(exc)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def run_doctor() -> list[Check]:
    checks: list[Check] = []

    uv = shutil.which("uv")
    if not uv:
        return [
            Check("TrendRadar", "FAIL", "uv not found"),
            Check("Agent-Reach", "FAIL", "agent-reach/uv not ready"),
            Check("MediaCrawler", "FAIL", "uv not found"),
            Check("MoneyPrinterTurbo", "FAIL", "uv not found"),
        ]

    trend_dir = os.environ.get("TREND_RADAR_DIR")
    if not trend_dir or not Path(trend_dir).exists():
        checks.append(Check("TrendRadar", "FAIL", "TREND_RADAR_DIR missing"))
    else:
        code, out, err = _run(
            [uv, "--directory", trend_dir, "run", "python", "-m", "mcp_server.server", "--help"],
            timeout=20,
        )
        checks.append(
            Check("TrendRadar", "READY" if code == 0 else "FAIL", out or err or "MCP server probe")
        )

    agent = shutil.which("agent-reach")
    if not agent:
        checks.append(Check("Agent-Reach", "FAIL", "agent-reach command not found"))
    else:
        code, out, err = _run([agent, "doctor", "--json"], timeout=30)
        if code != 0:
            checks.append(Check("Agent-Reach", "FAIL", err or out or "doctor failed"))
        else:
            try:
                payload = json.loads(out)
                text = json.dumps(payload, ensure_ascii=False)
                checks.append(Check("Agent-Reach", "READY", text))
            except json.JSONDecodeError:
                checks.append(Check("Agent-Reach", "PARTIAL", out or "doctor returned non-JSON"))

    media_dir = os.environ.get("MEDIA_CRAWLER_DIR")
    if not media_dir or not Path(media_dir).exists():
        checks.append(Check("MediaCrawler", "FAIL", "MEDIA_CRAWLER_DIR missing"))
    else:
        main_py = Path(media_dir) / "main.py"
        if main_py.exists():
            checks.append(Check("MediaCrawler", "READY", "MCP entrypoint main.py found"))
        else:
            checks.append(Check("MediaCrawler", "FAIL", "main.py missing"))

    money_dir = os.environ.get("MONEY_PRINTER_TURBO_DIR")
    if not money_dir or not Path(money_dir).exists():
        checks.append(Check("MoneyPrinterTurbo", "NOT_CONFIGURED", "MONEY_PRINTER_TURBO_DIR missing"))
    else:
        code, out, err = _run(
            [uv, "run", "python", "cli.py", "--help"],
            cwd=money_dir,
            timeout=30,
        )
        checks.append(
            Check(
                "MoneyPrinterTurbo",
                "READY" if code == 0 else "FAIL",
                out[:500] if out else (err[:500] if err else "CLI probe"),
            )
        )

    return checks
