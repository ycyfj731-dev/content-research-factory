from content_research_factory.consensus.discovery import build_discovery_plan


CONFIG = "config/consensus/lithium_carbonate.yaml"


def test_lc_discovery_plan_is_web_wide_and_contains_core_market_terms():
    plan = build_discovery_plan(CONFIG)
    queries = {item.query for item in plan}

    assert "碳酸锂" in queries
    assert "LC2701" in queries
    assert "碳酸锂 仓单注销" in queries
    assert "碳酸锂 看多" in queries
    assert "碳酸锂 看空" in queries
    assert "碳酸锂 津巴布韦" in queries
    assert "碳酸锂 基差" in queries
    assert all(item.lane == "web_wide" for item in plan)


def test_discovery_plan_has_no_duplicate_queries():
    plan = build_discovery_plan(CONFIG)
    queries = [item.query for item in plan]
    assert len(queries) == len(set(queries))


def test_dynamic_terms_are_added_without_changing_core_plan():
    base = build_discovery_plan(CONFIG)
    expanded = build_discovery_plan(
        CONFIG,
        dynamic_terms=["枧下窝复产", "宁德时代", "枧下窝复产"],
    )

    base_queries = {item.query for item in base}
    expanded_queries = {item.query for item in expanded}

    assert base_queries.issubset(expanded_queries)
    assert "碳酸锂 枧下窝复产" in expanded_queries
    assert "碳酸锂 宁德时代" in expanded_queries
    assert len(expanded_queries) == len(base_queries) + 2
