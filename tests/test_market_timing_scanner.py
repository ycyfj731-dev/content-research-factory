from datetime import datetime, timezone

from content_research_factory.market_timing import (
    EvidenceEvent,
    SourceStatus,
    scan_events,
)


def _event(
    event_id: str,
    hour: int,
    *,
    geometry_key: str | None = None,
    underlying_event_id: str | None = None,
    status: SourceStatus = SourceStatus.BOOK_EXACT,
):
    return EvidenceEvent(
        event_id=event_id,
        timestamp=datetime(2026, 9, 21, hour, tzinfo=timezone.utc),
        family="test",
        rule_id="TEST-R01",
        source_status=status,
        chart_context="MARKET",
        geometry_key=geometry_key,
        underlying_event_id=underlying_event_id,
    )


def test_same_geometry_is_counted_once():
    events = [
        _event("square", 1, geometry_key="JUPITER_SATURN_90_20260921"),
        _event("d45", 1, geometry_key="JUPITER_SATURN_90_20260921"),
        _event("h8", 1, geometry_key="JUPITER_SATURN_90_20260921"),
    ]

    result = scan_events(events)

    assert len(result.accepted) == 3
    assert len(result.independent) == 1


def test_underlying_anchor_event_is_counted_once():
    events = [
        _event("eclipse-anchor", 2, underlying_event_id="ECLIPSE_20260921"),
        _event("historical-anchor", 2, underlying_event_id="ECLIPSE_20260921"),
    ]

    result = scan_events(events)

    assert len(result.independent) == 1


def test_open_and_rejected_are_blocked():
    events = [
        _event("open", 3, status=SourceStatus.OPEN),
        _event("rejected", 4, status=SourceStatus.REJECTED_AS_SOURCE),
        _event("ok", 5),
    ]

    result = scan_events(events)

    assert [e.event_id for e in result.independent] == ["ok"]
    assert {e.event_id for e in result.blocked} == {"open", "rejected"}


def test_engineered_event_requires_approval():
    event = _event("engineered", 6, status=SourceStatus.ENGINEERED)

    blocked = scan_events([event])
    allowed = scan_events([event], engineered_approval=True)

    assert len(blocked.independent) == 0
    assert len(allowed.independent) == 1


def test_cluster_window_requires_explicit_approval():
    events = [_event("a", 7), _event("b", 8)]

    no_approval = scan_events(events, cluster_window_hours=2)
    approved = scan_events(
        events,
        cluster_window_hours=2,
        engineered_approval=True,
    )

    assert no_approval.clusters == []
    assert len(approved.clusters) == 1
    assert [e.event_id for e in approved.clusters[0]] == ["a", "b"]
