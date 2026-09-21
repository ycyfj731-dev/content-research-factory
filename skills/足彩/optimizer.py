"""Exact baseline optimizer for 足彩 V0.3.

Correctness-first implementation using only the Python standard library.
For each 7-match set it enumerates all 3^7 exact-result paths, takes the
highest-probability 8, and then compares sets by total coverage probability.

This is exponential/combinatorial by design and is intended as a reproducible
baseline. Production-scale acceleration may use pruning/vectorization later,
but must preserve the same objective and be validated against this baseline.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from math import prod
from typing import Iterable, Mapping, Sequence

OUTCOMES = ("H", "D", "A")


@dataclass(frozen=True)
class MatchProb:
    match_id: str
    probabilities: Mapping[str, float]


@dataclass(frozen=True)
class Path:
    outcomes: tuple[str, ...]
    probability: float


@dataclass(frozen=True)
class Selection:
    matches: tuple[MatchProb, ...]
    paths: tuple[Path, ...]
    coverage: float


def _validate_match(match: MatchProb) -> None:
    keys = set(match.probabilities)
    if keys != set(OUTCOMES):
        raise ValueError(f"{match.match_id}: probabilities must contain H/D/A")
    vals = [float(match.probabilities[o]) for o in OUTCOMES]
    if any(v < 0 or v > 1 for v in vals):
        raise ValueError(f"{match.match_id}: probabilities outside [0,1]")
    if abs(sum(vals) - 1.0) > 1e-9:
        raise ValueError(f"{match.match_id}: probabilities must sum to 1")


def enumerate_paths(matches: Sequence[MatchProb]) -> list[Path]:
    for m in matches:
        _validate_match(m)
    paths: list[Path] = []
    for outcome_tuple in product(OUTCOMES, repeat=len(matches)):
        p = prod(
            float(match.probabilities[outcome])
            for match, outcome in zip(matches, outcome_tuple)
        )
        paths.append(Path(outcomes=outcome_tuple, probability=p))
    return paths


def top_k_paths(matches: Sequence[MatchProb], k: int = 8) -> tuple[Path, ...]:
    """Return deterministic Top-K by probability, then H/D/A lexical order."""
    if k <= 0:
        raise ValueError("k must be positive")
    paths = enumerate_paths(matches)
    # H/D/A desired deterministic order rather than Python alphabetical A/D/H.
    rank = {"H": 0, "D": 1, "A": 2}
    paths.sort(
        key=lambda x: (
            -x.probability,
            tuple(rank[o] for o in x.outcomes),
        )
    )
    return tuple(paths[:k])


def coverage(paths: Iterable[Path]) -> float:
    """Sum probabilities of mutually exclusive exact-result paths."""
    return float(sum(p.probability for p in paths))


def optimize_fixed_matches(matches: Sequence[MatchProb], k: int = 8) -> Selection:
    if len(matches) != 7:
        raise ValueError("V0.3 fixed-ticket optimizer requires exactly 7 matches")
    best_paths = top_k_paths(matches, k=k)
    return Selection(
        matches=tuple(matches),
        paths=best_paths,
        coverage=coverage(best_paths),
    )


def optimize_joint(
    candidates: Sequence[MatchProb],
    choose: int = 7,
    k: int = 8,
    required_any_match_ids: set[str] | None = None,
) -> Selection:
    """Exact joint search over every choose-match subset.

    Tie-break: coverage descending, then selected match_id tuple ascending.
    """
    if len(candidates) < choose:
        raise ValueError("not enough candidate matches")
    if choose != 7:
        raise ValueError("V0.3 production rule currently fixes choose=7")

    best: Selection | None = None
    for subset in combinations(candidates, choose):
        if required_any_match_ids is not None:
            subset_ids = {m.match_id for m in subset}
            if not (subset_ids & required_any_match_ids):
                continue
        current = optimize_fixed_matches(subset, k=k)
        if best is None:
            best = current
            continue
        if current.coverage > best.coverage + 1e-15:
            best = current
        elif abs(current.coverage - best.coverage) <= 1e-15:
            ids_current = tuple(m.match_id for m in current.matches)
            ids_best = tuple(m.match_id for m in best.matches)
            if ids_current < ids_best:
                best = current
    if best is None:
        raise ValueError("no feasible 7-match subset satisfies the joint-search constraints")
    return best
