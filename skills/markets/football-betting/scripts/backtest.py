"""Leakage-safe backtest scaffolding for 足彩 V0.3.

No historical results are bundled here. The caller must supply timestamped
snapshots captured or reconstructable as-of each decision time.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Callable, Iterable, Sequence

from candidate_pool import MatchSnapshot, anchor_match_ids, eligible_at_decision_time
from optimizer import MatchProb, Selection, optimize_joint


@dataclass(frozen=True)
class BacktestDecision:
    decision_time: datetime
    candidate_count: int
    selection: Selection | None
    status: str


def run_decision(
    all_snapshots: Iterable[MatchSnapshot],
    decision_time: datetime,
    min_candidates: int = 7,
) -> BacktestDecision:
    """Build the as-of pool and run the exact COVER baseline if feasible."""
    pool = eligible_at_decision_time(all_snapshots, decision_time)
    if len(pool) < min_candidates:
        return BacktestDecision(
            decision_time=decision_time,
            candidate_count=len(pool),
            selection=None,
            status="NOT_EXECUTABLE",
        )

    anchors = anchor_match_ids(pool, decision_time)
    if not anchors:
        return BacktestDecision(
            decision_time=decision_time,
            candidate_count=len(pool),
            selection=None,
            status="NOT_EXECUTABLE_NO_ANCHOR",
        )

    probs = [
        MatchProb(match_id=m.match_id, probabilities=m.probabilities)
        for m in pool
    ]
    selection = optimize_joint(probs, required_any_match_ids=anchors)
    return BacktestDecision(
        decision_time=decision_time,
        candidate_count=len(pool),
        selection=selection,
        status="OK",
    )


def append_result_record(
    decision: BacktestDecision,
    actual_results: dict[str, str],
) -> dict:
    """Create a new result record without mutating the frozen decision object."""
    record = {
        "decision": {
            "decision_time": decision.decision_time.isoformat(),
            "candidate_count": decision.candidate_count,
            "status": decision.status,
        },
        "actual_results": dict(actual_results),
    }
    if decision.selection is not None:
        record["decision"]["selected_matches"] = [
            m.match_id for m in decision.selection.matches
        ]
        record["decision"]["coverage"] = decision.selection.coverage
        record["decision"]["paths"] = [
            {"outcomes": list(p.outcomes), "probability": p.probability}
            for p in decision.selection.paths
        ]
    return record
