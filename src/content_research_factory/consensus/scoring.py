from __future__ import annotations

from collections import defaultdict
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

DEFAULT_NORMALIZATION_CAPS: dict[str, dict[str, float]] = {
    "institution": {
        "platform_max_share": 0.55,
        "author_max_share": 0.15,
        "parent_post_max_share": 1.0,
    },
    "kol": {
        "platform_max_share": 0.45,
        "author_max_share": 0.08,
        "parent_post_max_share": 0.20,
    },
    "crowd": {
        "platform_max_share": 0.40,
        "author_max_share": 0.02,
        "parent_post_max_share": 0.08,
    },
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
    platform: str = "unknown"
    source_id: str | None = None
    parent_source_id: str | None = None

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
    raw_group_scores: dict[str, float | None]
    group_scores: dict[str, float | None]
    raw_consensus_score: float
    overall_consensus_score: float
    raw_crowding_score: float
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
    apply_uniqueness: bool = True,
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
    uniqueness = observation.uniqueness_factor if apply_uniqueness else 1.0

    return (
        observation.source_weight
        * observation.classifier_confidence
        * conviction_factor
        * freshness_weight(age_days, half_life)
        * uniqueness
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


def _crowding_score(weighted: list[tuple[ConsensusObservation, float]]) -> float:
    total = sum(weight for _, weight in weighted)
    if total <= 0:
        return 0.0
    mean_direction = _directional_mean(weighted)
    participation = sum(
        weight * abs(obs.direction / 2.0)
        for obs, weight in weighted
    ) / total
    return 100.0 * sqrt(abs(mean_direction) * participation)


def effective_sample_size(weights: Iterable[float]) -> float:
    values = [max(0.0, float(value)) for value in weights]
    total = sum(values)
    square_sum = sum(value * value for value in values)
    if total <= 0 or square_sum <= 0:
        return 0.0
    return (total * total) / square_sum


def _cap_dimension(
    weighted: list[tuple[ConsensusObservation, float]],
    *,
    key_fn,
    max_share: float,
) -> list[tuple[ConsensusObservation, float]]:
    if not weighted or max_share >= 1.0:
        return weighted
    if max_share <= 0:
        raise ValueError("max_share must be > 0")

    total = sum(weight for _, weight in weighted)
    if total <= 0:
        return weighted

    buckets: dict[str, float] = defaultdict(float)
    for obs, weight in weighted:
        buckets[str(key_fn(obs))] += weight

    cap = total * max_share
    over_limit = [
        key for key, bucket_weight in buckets.items()
        if bucket_weight > cap
    ]

    # If every bucket is above the nominal cap, the constraint is infeasible
    # for the current sample (e.g. two authors with a 2% author cap). In that
    # case skip the cap rather than flattening all weights and erasing
    # freshness/conviction information. If only a subset is over the cap, trim
    # the dominant buckets; this still reduces concentration even when the
    # final renormalized share cannot mathematically reach the nominal cap.
    if over_limit and len(over_limit) == len(buckets):
        return weighted

    scales: dict[str, float] = {}
    for key, bucket_weight in buckets.items():
        scales[key] = min(1.0, cap / bucket_weight) if bucket_weight > 0 else 1.0

    return [
        (obs, weight * scales[str(key_fn(obs))])
        for obs, weight in weighted
    ]


def _normalize_group_weights(
    weighted: list[tuple[ConsensusObservation, float]],
    *,
    caps: Mapping[str, float],
) -> list[tuple[ConsensusObservation, float]]:
    result = list(weighted)

    # Repeat a few rounds because applying one cap changes the denominator used
    # by the next cap. Three deterministic rounds are enough for stable bounded
    # influence in this lightweight V0.1 implementation.
    for _ in range(3):
        result = _cap_dimension(
            result,
            key_fn=lambda obs: obs.platform or "unknown",
            max_share=float(caps.get("platform_max_share", 1.0)),
        )
        result = _cap_dimension(
            result,
            key_fn=lambda obs: obs.author_id_hash or f"anon:{obs.source_id or id(obs)}",
            max_share=float(caps.get("author_max_share", 1.0)),
        )
        result = _cap_dimension(
            result,
            key_fn=lambda obs: obs.parent_source_id or obs.source_id or f"source:{id(obs)}",
            max_share=float(caps.get("parent_post_max_share", 1.0)),
        )

    return result


def _group_scores(
    weighted: list[tuple[ConsensusObservation, float]],
) -> dict[str, float | None]:
    scores: dict[str, float | None] = {}
    for group in DEFAULT_GROUP_WEIGHTS:
        rows = [pair for pair in weighted if pair[0].source_group == group]
        scores[group] = (
            _score_from_mean(_directional_mean(rows))
            if sum(weight for _, weight in rows) > 0
            else None
        )
    return scores


def _combine_group_scores(
    scores: Mapping[str, float | None],
    group_weights: Mapping[str, float],
) -> float:
    available = [
        group
        for group, score in scores.items()
        if score is not None and group_weights.get(group, 0.0) > 0
    ]
    if not available:
        return 50.0

    denominator = sum(group_weights[group] for group in available)
    return sum(
        group_weights[group] * float(scores[group])
        for group in available
    ) / denominator


def build_daily_scores(
    observations: Iterable[ConsensusObservation],
    *,
    now: datetime,
    group_weights: Mapping[str, float] | None = None,
    half_life_days: Mapping[str, float] | None = None,
    normalization_caps: Mapping[str, Mapping[str, float]] | None = None,
    explicit_position_factor: float = 1.25,
    conviction_floor: float = 0.25,
    conviction_scale: float = 0.75,
) -> DailyConsensusScores:
    rows = list(observations)
    configured_group_weights = dict(group_weights or DEFAULT_GROUP_WEIGHTS)
    configured_caps = normalization_caps or DEFAULT_NORMALIZATION_CAPS

    # RAW: exact duplicates should already be removed upstream, but semantic
    # repetition is intentionally not discounted here. This shows what the
    # captured public stream actually looked like.
    raw_weighted = [
        (
            obs,
            effective_weight(
                obs,
                now=now,
                half_life_days=half_life_days,
                explicit_position_factor=explicit_position_factor,
                conviction_floor=conviction_floor,
                conviction_scale=conviction_scale,
                apply_uniqueness=False,
            ),
        )
        for obs in rows
    ]

    # NORMALIZED: semantic repetition is discounted, then platform/author/post
    # concentration is capped inside each source group.
    normalized_base = [
        (
            obs,
            effective_weight(
                obs,
                now=now,
                half_life_days=half_life_days,
                explicit_position_factor=explicit_position_factor,
                conviction_floor=conviction_floor,
                conviction_scale=conviction_scale,
                apply_uniqueness=True,
            ),
        )
        for obs in rows
    ]

    normalized_weighted: list[tuple[ConsensusObservation, float]] = []
    for group in DEFAULT_GROUP_WEIGHTS:
        group_rows = [pair for pair in normalized_base if pair[0].source_group == group]
        normalized_weighted.extend(
            _normalize_group_weights(
                group_rows,
                caps=configured_caps.get(group, {}),
            )
        )

    raw_group_scores = _group_scores(raw_weighted)
    normalized_group_scores = _group_scores(normalized_weighted)

    # Raw consensus deliberately pools the captured stream. It answers:
    # "What did the content stream look like before normalization?"
    raw_consensus = _score_from_mean(_directional_mean(raw_weighted))

    # Normalized consensus answers:
    # "After controlling concentration, what is the cross-group consensus?"
    normalized_consensus = _combine_group_scores(
        normalized_group_scores,
        configured_group_weights,
    )

    unique_authors = {
        obs.author_id_hash
        for obs in rows
        if obs.author_id_hash
    }

    return DailyConsensusScores(
        raw_group_scores=raw_group_scores,
        group_scores=normalized_group_scores,
        raw_consensus_score=raw_consensus,
        overall_consensus_score=normalized_consensus,
        raw_crowding_score=_crowding_score(raw_weighted),
        crowding_score=_crowding_score(normalized_weighted),
        raw_sample_size=len(rows),
        unique_author_count=len(unique_authors),
        effective_sample_size=effective_sample_size(
            weight for _, weight in normalized_weighted
        ),
    )
