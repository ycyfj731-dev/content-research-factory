from pathlib import Path

from content_research_factory.routing import EXPECTED_ROUTING, load_routing


def test_fixed_routing_matches_repository_config():
    routes = load_routing(Path("config/routing.yaml"))

    assert set(routes) == set(EXPECTED_ROUTING)

    for stage, (tool, responsibility) in EXPECTED_ROUTING.items():
        assert routes[stage].tool == tool
        assert routes[stage].responsibility == responsibility
