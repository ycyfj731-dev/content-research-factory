from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .models import ResearchPackage


def write_research_package(
    package: ResearchPackage,
    path: str | Path,
) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(package), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path
