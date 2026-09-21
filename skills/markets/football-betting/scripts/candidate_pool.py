"""Candidate-pool helpers for 足彩 V0.3.

Standard-library only. This module does not fetch live data; it enforces the
shared ticket cutoff and input-availability rules on already collected data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from math import isfinite
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
    probability_available_at: datetime
    execution_odds: Mapping[str, float] | None = None
    execution_odds_available_at: datetime | None = None
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
    if any((not isinstance(x, (int, float))) or (not isfinite(float(x))) or x < 0 for x in vals):
        raise ValueError("probabilities must be finite non-negative numbers")
    total = float(sum(vals))
    if abs(total - 1.0) > tol:
        raise ValueError(f"probabilities must sum to 1, got {total}")


def snapshot_is_usable(match: MatchSnapshot, cutoff: datetime) -> bool:
    """True when every recorded feature was available no later than cutoff."""
    validate_probabilities(match.probabilities)
    if not match.executable:
        return False
    if match.probability_available_at > cutoff:
        return False
    if match.execution_odds is not None:
        if match.execution_odds_available_at is None:
            return False
        if match.execution_odds_available_at > cutoff:
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


def anchor_match_ids(
    matches: Iterable[MatchSnapshot],
    decision_time: datetime,
) -> set[str]:
    """Matches whose kickoff is exactly decision_time + 30 minutes.

    V0.3's A_t requires every searched 7-match set to contain at least one
    such anchor; because all other eligible matches kick off no earlier, this
    guarantees T_ticket(selected_set) == decision_time.
    """
    anchor_time = decision_time + timedelta(minutes=30)
    return {m.match_id for m in matches if m.kickoff_time == anchor_time}
