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
    platform="weibo",
    source_id=None,
    parent_source_id=None,
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
        platform=platform,
        source_id=source_id,
        parent_source_id=parent_source_id,
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


def test_viral_single_post_can_move_raw_more_than_normalized():
    rows = [
        obs(
            group="institution",
            direction=-2,
            author=f"inst-{i}",
            platform="institution_web",
            source_id=f"inst-post-{i}",
        )
        for i in range(10)
    ]
    rows += [
        obs(
            group="crowd",
            direction=2,
            author=f"crowd-{i}",
            platform="douyin",
            source_id=f"comment-{i}",
            parent_source_id="viral-video",
        )
        for i in range(500)
    ]

    result = build_daily_scores(rows, now=NOW)

    assert result.raw_consensus_score > 90.0
    # Parent-post and group balancing prevent one viral thread from defining
    # the normalized market consensus.
    assert result.overall_consensus_score < result.raw_consensus_score - 20.0


def test_semantic_repetition_is_visible_in_raw_but_discounted_in_normalized():
    rows = [
        obs(
            group="kol",
            direction=2,
            author=f"copy-{i}",
            platform="weibo",
            source_id=f"copy-post-{i}",
            uniqueness=0.05,
        )
        for i in range(100)
    ]
    rows += [
        obs(
            group="kol",
            direction=-2,
            author=f"independent-{i}",
            platform="xiaohongshu",
            source_id=f"independent-post-{i}",
            uniqueness=1.0,
        )
        for i in range(15)
    ]

    result = build_daily_scores(rows, now=NOW)

    assert result.raw_group_scores["kol"] > 80.0
    assert result.group_scores["kol"] < 40.0


def test_platform_concentration_is_capped_in_normalized_score():
    rows = [
        obs(
            group="crowd",
            direction=2,
            author=f"wb-{i}",
            platform="weibo",
            source_id=f"wb-{i}",
            parent_source_id=f"wb-parent-{i}",
        )
        for i in range(300)
    ]
    rows += [
        obs(
            group="crowd",
            direction=-2,
            author=f"xhs-{i}",
            platform="xiaohongshu",
            source_id=f"xhs-{i}",
            parent_source_id=f"xhs-parent-{i}",
        )
        for i in range(50)
    ]

    result = build_daily_scores(rows, now=NOW)

    assert result.raw_group_scores["crowd"] > 80.0
    assert result.group_scores["crowd"] < result.raw_group_scores["crowd"]


def test_raw_and_normalized_match_when_sample_is_balanced_and_unique():
    rows = [
        obs(group="institution", direction=1, author="i1", platform="institution_web", source_id="i1"),
        obs(group="kol", direction=1, author="k1", platform="weibo", source_id="k1"),
        obs(group="crowd", direction=1, author="c1", platform="xiaohongshu", source_id="c1"),
    ]

    result = build_daily_scores(rows, now=NOW)

    assert result.raw_consensus_score == pytest.approx(75.0)
    assert result.overall_consensus_score == pytest.approx(75.0)
