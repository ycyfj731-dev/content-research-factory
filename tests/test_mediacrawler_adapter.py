import json

from content_research_factory.adapters.mediacrawler_mcp import MediaCrawlerMCPAdapter


class FakeMCP:
    def __init__(self):
        self.calls = []

    def call(self, method, params):
        self.calls.append((method, params))
        return "success to crawl"


def test_search_calls_real_crawl_search_and_reads_json(tmp_path):
    data_dir = tmp_path / "data" / "xhs"
    data_dir.mkdir(parents=True)
    payload = [
        {
            "note_id": "abc",
            "title": "example",
            "desc": "body",
        }
    ]
    target = data_dir / "search_contents_20260918.json"
    target.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    adapter = object.__new__(MediaCrawlerMCPAdapter)
    adapter.mcp = FakeMCP()
    adapter.project_dir = tmp_path
    adapter.platforms = ("xhs",)
    adapter.search_tool = "crawl_search"
    adapter.detail_tool = "crawl_detail"

    rows = adapter.search("AI 家居", platform="xhs")

    assert rows[0]["note_id"] == "abc"
    assert rows[0]["origin_tool"] == "MediaCrawler"
    assert adapter.mcp.calls[0][0] == "crawl_search"
    assert adapter.mcp.calls[0][1]["store_type"] == "json"


def test_platform_aliases_are_normalized():
    assert MediaCrawlerMCPAdapter._platform("xiaohongshu") == "xhs"
    assert MediaCrawlerMCPAdapter._platform("bilibili") == "bili"
