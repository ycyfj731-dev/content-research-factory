from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Iterable


class SourceStatus(str, Enum):
    BOOK_EXACT = "BOOK-EXACT"
    BOOK_EXACT_EXAMPLE = "BOOK-EXACT-EXAMPLE"
    BOOK_INTERPRETED = "BOOK-INTERPRETED"
    SOURCE_UNSPECIFIED = "SOURCE_UNSPECIFIED"
    ENGINEERED = "ENGINEERED"
    VALIDATION = "VALIDATION"
    OPEN = "OPEN"
    REJECTED_AS_SOURCE = "REJECTED-AS-SOURCE"


_BLOCKED = {SourceStatus.OPEN, SourceStatus.REJECTED_AS_SOURCE}


@dataclass(frozen=True)
class EvidenceEvent:
    event_id: str
    timestamp: datetime
    family: str
    rule_id: str
    source_status: SourceStatus
    chart_context: str
    geometry_key: str | None = None
    underlying_event_id: str | None = None
    labels: tuple[str, ...] = ()
    note: str = ""

    def normalized_timestamp(self) -> datetime:
        if self.timestamp.tzinfo is None:
            return self.timestamp.replace(tzinfo=timezone.utc)
        return self.timestamp.astimezone(timezone.utc)


@dataclass(frozen=True)
class RealitySnapshot:
    timestamp: datetime
    warehouse_receipts: float | None = None
    receipt_cancellations: float | None = None
    basis: float | None = None
    social_inventory: float | None = None
    domestic_production: float | None = None
    import_arrivals: float | None = None
    demand_note: str = ""
    supply_note: str = ""
    policy_note: str = ""


@dataclass
class ScanResult:
    accepted: list[EvidenceEvent] = field(default_factory=list)
    blocked: list[EvidenceEvent] = field(default_factory=list)
    independent: list[EvidenceEvent] = field(default_factory=list)
    exact_coincidences: list[list[EvidenceEvent]] = field(default_factory=list)
    clusters: list[list[EvidenceEvent]] = field(default_factory=list)
    reality: list[RealitySnapshot] = field(default_factory=list)
    engineered_parameters: dict[str, object] = field(default_factory=dict)


def _dedup_key(event: EvidenceEvent) -> tuple[str, str]:
    """
    Prefer the lowest-level shared identity available.

    geometry_key deduplicates multiple representations of the same geometry
    (e.g. 90-degree aspect, D45 alignment, H8 projection).

    underlying_event_id deduplicates multiple labels attached to the same
    real/astronomical event (e.g. eclipse + historical-market-event).
    """
    if event.geometry_key:
        return ("geometry", event.geometry_key)
    if event.underlying_event_id:
        return ("underlying_event", event.underlying_event_id)
    return ("event", event.event_id)


def _deduplicate(events: Iterable[EvidenceEvent]) -> list[EvidenceEvent]:
    seen: set[tuple[str, str]] = set()
    out: list[EvidenceEvent] = []
    for event in sorted(events, key=lambda e: e.normalized_timestamp()):
        key = _dedup_key(event)
        if key in seen:
            continue
        seen.add(key)
        out.append(event)
    return out


def _exact_coincidences(events: Iterable[EvidenceEvent]) -> list[list[EvidenceEvent]]:
    buckets: dict[datetime, list[EvidenceEvent]] = {}
    for event in events:
        buckets.setdefault(event.normalized_timestamp(), []).append(event)
    return [
        bucket
        for _, bucket in sorted(buckets.items(), key=lambda item: item[0])
        if len(bucket) > 1
    ]


def _cluster(
    events: list[EvidenceEvent],
    window_hours: float,
) -> list[list[EvidenceEvent]]:
    if window_hours <= 0:
        raise ValueError("cluster_window_hours must be > 0")

    ordered = sorted(events, key=lambda e: e.normalized_timestamp())
    if not ordered:
        return []

    max_gap = timedelta(hours=window_hours)
    clusters: list[list[EvidenceEvent]] = [[ordered[0]]]

    for event in ordered[1:]:
        previous = clusters[-1][-1]
        gap = event.normalized_timestamp() - previous.normalized_timestamp()
        if gap <= max_gap:
            clusters[-1].append(event)
        else:
            clusters.append([event])

    return [cluster for cluster in clusters if len(cluster) > 1]


def scan_events(
    events: Iterable[EvidenceEvent],
    *,
    reality: Iterable[RealitySnapshot] = (),
    cluster_window_hours: float | None = None,
    engineered_approval: bool = False,
) -> ScanResult:
    """
    Source-faithful V0.1 scanner.

    No bullish/bearish mapping, weights, scores or default time-window is used.

    A numeric cluster window is ENGINEERED. It is only used when both:
      1) cluster_window_hours is explicitly supplied; and
      2) engineered_approval=True.
    """
    accepted: list[EvidenceEvent] = []
    blocked: list[EvidenceEvent] = []

    for event in events:
        if event.source_status in _BLOCKED:
            blocked.append(event)
        elif event.source_status is SourceStatus.ENGINEERED and not engineered_approval:
            blocked.append(event)
        else:
            accepted.append(event)

    independent = _deduplicate(accepted)
    exact = _exact_coincidences(independent)

    clusters: list[list[EvidenceEvent]] = []
    engineered_parameters: dict[str, object] = {}

    if cluster_window_hours is not None:
        engineered_parameters["cluster_window_hours"] = cluster_window_hours
        if engineered_approval:
            clusters = _cluster(independent, cluster_window_hours)

    return ScanResult(
        accepted=accepted,
        blocked=blocked,
        independent=independent,
        exact_coincidences=exact,
        clusters=clusters,
        reality=list(reality),
        engineered_parameters=engineered_parameters,
    )
