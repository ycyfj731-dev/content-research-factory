"""Ticket-level branch coverage diagnostics for 足彩 V0.3."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from optimizer import MatchProb, Path, Selection, OUTCOMES


@dataclass(frozen=True)
class BranchExposure:
    match_id: str
    outcome: str
    forecast_probability: float
    W_ir: float
    N_ir: int
    coverage_share: float


def branch_exposures(selection: Selection) -> tuple[BranchExposure, ...]:
    """Compute W_ir and N_ir for every selected match/outcome branch."""
    if selection.coverage <= 0:
        raise ValueError("selection coverage must be positive")

    rows: list[BranchExposure] = []
    for idx, match in enumerate(selection.matches):
        for outcome in OUTCOMES:
            matching = [p for p in selection.paths if p.outcomes[idx] == outcome]
            w = float(sum(p.probability for p in matching))
            rows.append(
                BranchExposure(
                    match_id=match.match_id,
                    outcome=outcome,
                    forecast_probability=float(match.probabilities[outcome]),
                    W_ir=w,
                    N_ir=len(matching),
                    coverage_share=w / selection.coverage,
                )
            )
    return tuple(rows)


def exposure_map(selection: Selection) -> Mapping[tuple[str, str], BranchExposure]:
    return {(x.match_id, x.outcome): x for x in branch_exposures(selection)}
