from content_research_factory.adapters.agent_reach import AgentReachAdapter
from content_research_factory.adapters.trendradar import TrendRadarAdapter


class FakeRPC:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def call(self, method, params):
        self.calls.append((method, params))
        return self.result


def test_trendradar_adapter_normalizes_items():
    adapter = object.__new__(TrendRadarAdapter)
    adapter.rpc = FakeRPC({"items": [{"id": "1", "title": "trend"}]})
    adapter.discover_method = "discover"

    rows = adapter.discover("AI")

    assert rows == [{"id": "1", "title": "trend"}]
    assert adapter.rpc.calls[0][0] == "discover"


def test_agent_reach_adapter_passes_candidates():
    adapter = object.__new__(AgentReachAdapter)
    adapter.rpc = FakeRPC([{"id": "v1"}])
    adapter.verify_method = "verify"

    rows = adapter.verify("AI", candidates=[{"id": "t1"}])

    assert rows == [{"id": "v1"}]
    assert adapter.rpc.calls[0][1]["candidates"] == [{"id": "t1"}]
