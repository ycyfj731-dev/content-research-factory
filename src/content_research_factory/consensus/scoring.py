from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import sqrt
from typing import Iterable, Mapping


DEFAULT_HALF_LIFE_DAYS: dict[str, float] = {
    "intraday": 0.5,
    "1_5d": 2.0,
    "6_20d": 7.0,
    "21_60d": 21.0,
    "longer": 60.0,
    "unspecified": 7.0,
}

DEFAULT_GROUP_WEIGHTS: dict[str, float] = {
    "institution": 0.45,
    "kol": 0.30,
    "crowd": 0.25,
}


@dataclass(frozen=True)
class ConsensusObservation:
    source_group: str
    direction: int
    published_at: datetime
    horizon: str = "unspecified"
    source_weight: float = 1.0
    classifier_confidence: float = 1.0
    conviction: float = 0.5
    uniqueness_factor: float = 1.0
    position_disclosed: bool = False
    disclosed_position: str | None = None
    author_id_hash: str | None = None

    def __post_init__(self) -> None:
        if self.source_group not in DEFAULT_GROUP_WEIGHTS:
            raise ValueError(f"unsupported source_group: {self.source_group}")
        if self.direction not in {-2, -1, 0, 1, 2}:
            raise ValueError("direction must be one of -2, -1, 0, 1, 2")
        if self.horizon not in DEFAULT_HALF_LIFE_DAYS:
            raise ValueError(f"unsupported horizon: {self.horizon}")
        if self.source_weight <= 0:
            raise ValueError("source_weight must be > 0")
        for name, value in (
            ("classifier_confidence", self.classifier_confidence),
            ("conviction", self.conviction),
            ("uniqueness_factor", self.uniqueness_factor),
        ):
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.published_at.tzinfo is None:
            raise ValueError("published_at must be timezone-aware")


@dataclass(frozen=True)
class DailyConsensusScores:
    group_scores: dict[str, float | None]
    overall_consensus_score: float
    crowding_score: float
    raw_sample_size: int
    unique_author_count: int
    effective_sample_size: float


def freshness_weight(age_days: float, half_life_days: float) -> float:
    if half_life_days <= 0:
        raise ValueError("half_life_days must be > 0")
    age_days = max(0.0, age_days)
    return 0.5 ** (age_days / half_life_days)


def _position_matches_direction(observation: ConsensusObservation) -> bool:
    if not observation.position_disclosed:
        return False
    if observation.direction > 0 and observation.disclosed_position == "long":
        return True
    if observation.direction < 0 and observation.disclosed_position == "short":
        return True
    return False


def effective_weight(
    observation: ConsensusObservation,
    *,
    now: datetime,
    half_life_days: Mapping[str, float] | None = None,
    explicit_position_factor: float = 1.25,
    conviction_floor: float = 0.25,
    conviction_scale: float = 0.75,
) -> float:
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    half_lives = half_life_days or DEFAULT_HALF_LIFE_DAYS
    half_life = half_lives[observation.horizon]
    age_days = max(
        0.0,
        (now.astimezone(timezone.utc) - observation.published_at.astimezone(timezone.utc)).total_seconds()
        / 86400.0,
    )

    conviction_factor = conviction_floor + conviction_scale * observation.conviction
    position_factor = (
        explicit_position_factor
        if _position_matches_direction(observation)
        else 1.0
    )

    return (
        observation.source_weight
        * observation.classifier_confidence
        * conviction_factor
        * freshness_weight(age_days, half_life)
        * observation.uniqueness_factor
        * position_factor
    )


def _directional_mean(
    weighted: list[tuple[ConsensusObservation, float]],
) -> float:
    denominator = sum(weight for _, weight in weighted)
    if denominator <= 0:
        return 0.0
    return sum(weight * (obs.direction / 2.0) for obs, weight in weighted) / denominator


def _score_from_mean(mean_direction: float) -> float:
    return max(0.0, min(100.0, 50.0 * (1.0 + mean_direction)))


def effective_sample_size(weights: Iterable[float]) -> float:
    values = [max(0.0, float(value)) for value in weights]
    total = sum(values)
    square_sum = sum(value * value for value in values)
    if total <= 0 or square_sum <= 0:
        return 0.0
    return (total * total) / square_sum


def build_daily_scores(
    observations: Iterable[ConsensusObservation],
    *,
    now: datetime,
    group_weights: Mapping[str, float] | None = None,
    half_life_days: Mapping[str, float] | None = None,
    explicit_position_factor: float = 1.25,
    conviction_floor: float = 0.25,
    conviction_scale: float = 0.75,
) -> DailyConsensusScores:
    rows = list(observations)
    weights_by_observation: list[tuple[ConsensusObservation, float]] = [
        (
            obs,
            effective_weight(
                obs,
                now=now,
                half_life_days=half_life_days,
                explicit_position_factor=explicit_position_factor,
                conviction_floor=conviction_floor,
                conviction_scale=conviction_scale,
            ),
        )
        for obs in rows
    ]

    group_scores: dict[str, float | None] = {}
    for group in DEFAULT_GROUP_WEIGHTS:
        group_rows = [
            pair for pair in weights_by_observation if pair[0].source_group == group
        ]
        positive_weight = sum(weight for _, weight in group_rows)
        group_scores[group] = (
            _score_from_mean(_directional_mean(group_rows))
            if positive_weight > 0
            else None
        )

    configured_group_weights = dict(group_weights or DEFAULT_GROUP_WEIGHTS)
    available = [
        group
        for group, score in group_scores.items()
        if score is not None and configured_group_weights.get(group, 0.0) > 0
    ]
    if not available:
        overall = 50.0
    else:
        denominator = sum(configured_group_weights[group] for group in available)
        overall = sum(
            configured_group_weights[group] * float(group_scores[group])
            for group in available
        ) / denominator

    all_weight = sum(weight for _, weight in weights_by_observation)
    if all_weight <= 0:
        crowding = 0.0
    else:
        mean_direction = _directional_mean(weights_by_observation)
        participation = sum(
            weight * abs(obs.direction / 2.0)
            for obs, weight in weights_by_observation
        ) / all_weight
        crowding = 100.0 * sqrt(abs(mean_direction) * participation)

    unique_authors = {
        obs.author_id_hash
        for obs in rows
        if obs.author_id_hash
    }

    return DailyConsensusScores(
        group_scores=group_scores,
        overall_consensus_score=overall,
        crowding_score=crowding,
        raw_sample_size=len(rows),
        unique_author_count=len(unique_authors),
        effective_sample_size=effective_sample_size(
            weight for _, weight in weights_by_observation
        ),
    )
