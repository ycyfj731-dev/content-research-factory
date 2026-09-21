"""Candidate-pool helpers for 足彩 V0.3.

Standard-library only. This module does not fetch live data; it enforces the
shared ticket cutoff and input-availability rules on already collected data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class TimedValue:
    value: Any
    available_at: datetime
    source: str | None = None


@dataclass(frozen=True)
class MatchSnapshot:
    match_id: str
    kickoff_time: datetime
    probabilities: Mapping[str, float]
    execution_odds: Mapping[str, float] | None = None
    features: Mapping[str, TimedValue] = field(default_factory=dict)
    executable: bool = True


def ticket_time(matches: Sequence[MatchSnapshot]) -> datetime:
    """Return T_ticket = earliest kickoff among selected matches - 30 minutes."""
    if not matches:
        raise ValueError("matches must not be empty")
    return min(m.kickoff_time for m in matches) - timedelta(minutes=30)


def validate_probabilities(probabilities: Mapping[str, float], tol: float = 1e-9) -> None:
    keys = set(probabilities)
    if keys != {"H", "D", "A"}:
        raise ValueError(f"probabilities must have H/D/A, got {sorted(keys)}")
    vals = list(probabilities.values())
    if any((not isinstance(x, (int, float))) or x < 0 for x in vals):
        raise ValueError("probabilities must be finite non-negative numbers")
    total = float(sum(vals))
    if abs(total - 1.0) > tol:
        raise ValueError(f"probabilities must sum to 1, got {total}")


def snapshot_is_usable(match: MatchSnapshot, cutoff: datetime) -> bool:
    """True when every recorded feature was available no later than cutoff."""
    validate_probabilities(match.probabilities)
    if not match.executable:
        return False
    return all(tv.available_at <= cutoff for tv in match.features.values())


def filter_candidate_pool(
    matches: Iterable[MatchSnapshot],
    cutoff: datetime,
) -> list[MatchSnapshot]:
    """Keep only matches executable using information available at cutoff."""
    usable = [m for m in matches if snapshot_is_usable(m, cutoff)]
    usable.sort(key=lambda m: (m.kickoff_time, m.match_id))
    return usable


def eligible_at_decision_time(
    matches: Iterable[MatchSnapshot],
    decision_time: datetime,
) -> list[MatchSnapshot]:
    """Return matches usable at decision_time and not already inside the 30m lock.

    A match must kick off at least 30 minutes after decision_time.
    """
    min_kickoff = decision_time + timedelta(minutes=30)
    return [
        m for m in filter_candidate_pool(matches, decision_time)
        if m.kickoff_time >= min_kickoff
    ]
