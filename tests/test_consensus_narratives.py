import pytest

from content_research_factory.consensus.narratives import (
    cluster_observations,
    jaccard_similarity,
    narrative_summary,
)


def row(text, author, group="crowd"):
    return {
        "raw_text": text,
        "author_id_hash": author,
        "source_group": group,
        "direction": -1,
        "narrative_ids": [],
        "uniqueness_factor": 1.0,
    }


def test_similar_repeated_zimbabwe_supply_text_clusters_and_decays():
    rows = [
        row("津巴布韦锂矿已经到港，后续供应压力增加", "a", "institution"),
        row("津巴锂矿陆续到港，供应压力增加", "b", "kol"),
        row("津巴矿到港了，后面供应压力大", "c", "crowd"),
    ]

    clustered, clusters = cluster_observations(rows, similarity_threshold=0.35)

    assert len(clusters) == 1
    assert clusters[0].narrative_id == "zimbabwe_supply"
    assert clustered[0]["uniqueness_factor"] >= clustered[1]["uniqueness_factor"]
    assert clustered[1]["uniqueness_factor"] >= clustered[2]["uniqueness_factor"]


def test_unrelated_warehouse_receipt_story_stays_separate():
    rows = [
        row("津巴布韦锂矿已经到港，供应压力增加", "a"),
        row("交易所碳酸锂仓单连续注销，现货端偏紧", "b"),
    ]

    _, clusters = cluster_observations(rows, similarity_threshold=0.4)
    ids = {cluster.narrative_id for cluster in clusters}

    assert "zimbabwe_supply" in ids
    assert "warehouse_receipts" in ids
    assert len(clusters) == 2


def test_narrative_summary_reports_direction_and_saturation():
    rows = [
        row("碳酸锂仓单注销继续增加", "a", "institution"),
        row("仓单注销还在加速", "b", "kol"),
        row("仓单还在注销", "c", "crowd"),
    ]
    clustered, clusters = cluster_observations(rows, similarity_threshold=0.25)
    summary = narrative_summary(clustered, clusters)

    assert summary
    top = summary[0]
    assert top["narrative_id"] == "warehouse_receipts"
    assert top["direction"] < 0
    assert 0 <= top["saturation"] <= 100


def test_jaccard_is_higher_for_near_duplicates():
    near = jaccard_similarity(
        "碳酸锂仓单连续注销",
        "碳酸锂仓单继续注销",
    )
    far = jaccard_similarity(
        "碳酸锂仓单连续注销",
        "新能源汽车销量增长",
    )
    assert near > far
