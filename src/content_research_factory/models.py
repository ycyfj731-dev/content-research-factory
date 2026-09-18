from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvidenceItem:
    stage: str
    tool: str
    platform: str | None = None
    source_id: str | None = None
    url: str | None = None
    author: str | None = None
    title: str | None = None
    text: str | None = None
    published_at: str | None = None
    engagement: dict[str, Any] = field(default_factory=dict)
    comments: list[dict[str, Any]] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ResearchPackage:
    query: str
    discoveries: list[EvidenceItem]
    verifications: list[EvidenceItem]
    deep_research: list[EvidenceItem]
    synthesis: dict[str, Any]
    production_handoff: dict[str, Any] | None = None
