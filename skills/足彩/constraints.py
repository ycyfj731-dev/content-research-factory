"""Predeclared return constraints for 足彩 V0.3.

Only MIN_PATH_GROSS is implemented here because it preserves a simple exact
solution: filter infeasible paths first, then take probability Top-K.
Combination-level constraints (CONDITIONAL_MEAN_GROSS and EXPECTED_NET) are
intentionally not approximated by a greedy algorithm; they require a solver
with an explicit optimality guarantee before entering the executable baseline.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import prod
from typing import Mapping, Sequence

from optimizer import MatchProb, OUTCOMES, Path, Selection


@dataclass(frozen=True)
class MatchMarket:
    match: MatchProb
    execution_odds: Mapping[str, float]


@dataclass(frozen=True)
class PricedPath:
    path: Path
    decimal_odds: float
    gross_return: float


def price_paths(markets: Sequence[MatchMarket], stake_per_path: float = 2.0) -> list[PricedPath]:
    priced: list[PricedPath] = []
    for outcome_tuple in product(OUTCOMES, repeat=len(markets)):
        p = prod(
            float(m.match.probabilities[o])
            for m, o in zip(markets, outcome_tuple)
        )
        odds = prod(
            float(m.execution_odds[o])
            for m, o in zip(markets, outcome_tuple)
        )
        priced.append(
            PricedPath(
                path=Path(outcomes=outcome_tuple, probability=p),
                decimal_odds=odds,
                gross_return=stake_per_path * odds,
            )
        )
    return priced


def optimize_min_path_gross(
    markets: Sequence[MatchMarket],
    min_gross_return: float,
    k: int = 8,
    stake_per_path: float = 2.0,
) -> Selection:
    """Exact fixed-7 solver for MIN_PATH_GROSS."""
    if len(markets) != 7:
        raise ValueError("MIN_PATH_GROSS baseline requires exactly 7 matches")
    feasible = [
        p for p in price_paths(markets, stake_per_path=stake_per_path)
        if p.gross_return >= min_gross_return
    ]
    if len(feasible) < k:
        raise ValueError("INFEASIBLE: fewer than k paths satisfy MIN_PATH_GROSS")
    rank = {"H": 0, "D": 1, "A": 2}
    feasible.sort(
        key=lambda x: (
            -x.path.probability,
            tuple(rank[o] for o in x.path.outcomes),
        )
    )
    chosen = tuple(x.path for x in feasible[:k])
    return Selection(
        matches=tuple(m.match for m in markets),
        paths=chosen,
        coverage=float(sum(p.probability for p in chosen)),
    )
