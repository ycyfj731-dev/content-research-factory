from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class CoverageRecord:
    source: str
    status: str
    records: int = 0
    error: str | None = None

    def __post_init__(self) -> None:
        if self.status not in {"ok", "partial", "missing", "failed"}:
            raise ValueError(f"invalid coverage status: {self.status}")


def coverage_as_dicts(records: list[CoverageRecord]) -> list[dict[str, Any]]:
    return [asdict(record) for record in records]
