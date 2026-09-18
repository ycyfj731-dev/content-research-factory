from content_research_factory.adapters.agent_reach import AgentReachAdapter, AgentReachConfig
from content_research_factory.adapters.trendradar import TrendRadarAdapter


class FakeMCP:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def call(self, method, params):
        self.calls.append((method, params))
        return self.responses.pop(0)


def test_trendradar_uses_real_tool_names_and_merges_results():
    adapter = object.__new__(TrendRadarAdapter)
    adapter.mcp = FakeMCP([
        {"items": [{"id": "1", "title": "query hit"}]},
        {"topics": [{"title": "hot topic"}]},
    ])
    adapter.search_tool = "search_news"
    adapter.trending_tool = "get_trending_topics"

    rows = adapter.discover("AI", limit=10)

    assert rows[0]["title"] == "query hit"
    assert rows[1]["title"] == "hot topic"
    assert adapter.mcp.calls[0][0] == "search_news"
    assert adapter.mcp.calls[1][0] == "get_trending_topics"


def test_agent_reach_bilibili_uses_documented_cli():
    adapter = AgentReachAdapter(AgentReachConfig(platforms=("bilibili",)))
    command = adapter._command_for("bilibili", None, "AI")
    assert command == ["bili", "search", "AI", "--type", "video", "-n", "5"]
