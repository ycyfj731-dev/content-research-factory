from content_research_factory.consensus.narratives import cluster_observations


def row(text, author):
    return {
        "raw_text": text,
        "author_id_hash": author,
        "source_group": "kol",
        "direction": -1,
        "narrative_ids": [],
        "uniqueness_factor": 1.0,
    }


def test_semantic_matrix_can_join_low_lexical_overlap_paraphrases():
    rows = [
        row("非洲矿进口恢复以后四季度盐端压力会增加", "a"),
        row("海外锂资源供应回来，后面碳酸锂供给更宽松", "b"),
    ]
    semantic = [
        [1.0, 0.88],
        [0.88, 1.0],
    ]

    _, clusters = cluster_observations(
        rows,
        similarity_threshold=0.95,
        semantic_matrix=semantic,
        semantic_threshold=0.80,
    )

    assert len(clusters) == 1


def test_semantic_similarity_below_threshold_does_not_force_cluster():
    rows = [
        row("津巴矿供应恢复", "a"),
        row("仓单持续注销", "b"),
    ]
    semantic = [
        [1.0, 0.31],
        [0.31, 1.0],
    ]

    _, clusters = cluster_observations(
        rows,
        similarity_threshold=0.95,
        semantic_matrix=semantic,
        semantic_threshold=0.80,
    )

    assert len(clusters) == 2
