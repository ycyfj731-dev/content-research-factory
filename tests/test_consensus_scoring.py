from datetime import datetime, timedelta, timezone

import pytest

from content_research_factory.consensus.scoring import (
    ConsensusObservation,
    build_daily_scores,
    effective_weight,
)


NOW = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)


def obs(
    *,
    group="crowd",
    direction=2,
    age_days=0,
    horizon="1_5d",
    conviction=1.0,
    confidence=1.0,
    uniqueness=1.0,
    position_disclosed=False,
    disclosed_position=None,
    author=None,
):
    return ConsensusObservation(
        source_group=group,
        direction=direction,
        published_at=NOW - timedelta(days=age_days),
        horizon=horizon,
        source_weight=1.0,
        classifier_confidence=confidence,
        conviction=conviction,
        uniqueness_factor=uniqueness,
        position_disclosed=position_disclosed,
        disclosed_position=disclosed_position,
        author_id_hash=author,
    )


def test_all_strong_bulls_score_and_crowding_are_100():
    result = build_daily_scores(
        [obs(author="a"), obs(author="b"), obs(author="c")],
        now=NOW,
    )
    assert result.group_scores["crowd"] == pytest.approx(100.0)
    assert result.overall_consensus_score == pytest.approx(100.0)
    assert result.crowding_score == pytest.approx(100.0)
    assert result.unique_author_count == 3


def test_equal_strong_bulls_and_bears_are_balanced_not_crowded():
    result = build_daily_scores(
        [
            obs(direction=2, author="a"),
            obs(direction=-2, author="b"),
        ],
        now=NOW,
    )
    assert result.group_scores["crowd"] == pytest.approx(50.0)
    assert result.overall_consensus_score == pytest.approx(50.0)
    assert result.crowding_score == pytest.approx(0.0)


def test_group_level_weighting_prevents_comment_volume_from_drowning_institution():
    rows = [obs(group="institution", direction=2, author="inst")]
    rows += [
        obs(group="crowd", direction=-2, author=f"crowd-{i}")
        for i in range(100)
    ]

    result = build_daily_scores(rows, now=NOW)

    assert result.group_scores["institution"] == pytest.approx(100.0)
    assert result.group_scores["crowd"] == pytest.approx(0.0)
    # Only institution and crowd are available, so 0.45/0.25 weights renormalize.
    assert result.overall_consensus_score == pytest.approx(
        100.0 * 0.45 / (0.45 + 0.25)
    )


def test_fresh_opinion_can_dominate_stale_opposite_view():
    result = build_daily_scores(
        [
            obs(direction=2, age_days=10, horizon="1_5d", author="old"),
            obs(direction=-2, age_days=0, horizon="1_5d", author="new"),
        ],
        now=NOW,
    )
    assert result.group_scores["crowd"] < 20.0


def test_explicit_matching_position_gets_bounded_weight_boost():
    plain = obs(direction=-2, position_disclosed=False)
    positioned = obs(
        direction=-2,
        position_disclosed=True,
        disclosed_position="short",
    )

    plain_weight = effective_weight(plain, now=NOW)
    positioned_weight = effective_weight(positioned, now=NOW)

    assert positioned_weight == pytest.approx(plain_weight * 1.25)


def test_invalid_direction_rejected():
    with pytest.raises(ValueError):
        ConsensusObservation(
            source_group="crowd",
            direction=3,
            published_at=NOW,
        )
