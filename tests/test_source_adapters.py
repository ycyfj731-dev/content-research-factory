from content_research_factory.adapters.reddit_mcp import _items
from content_research_factory.adapters.tikhub import TikHubAdapter
from content_research_factory.adapters.trendscope import _walk_items


def test_trendscope_walks_nested_signal_payloads():
    payload = {
        "sources": {
            "reddit": [
                {"title": "Lithium discussion", "url": "https://example.com/r"}
            ],
            "news": [
                {"content": "Supply is recovering", "source": "gdelt"}
            ],
        }
    }
    rows = _walk_items(payload)
    assert len(rows) == 2


def test_reddit_items_reads_common_wrappers():
    payload = {"data": {"results": [{"id": "abc", "title": "Lithium"}]}}
    assert _items(payload) == [{"id": "abc", "title": "Lithium"}]


def test_tikhub_normalizes_xiaohongshu_candidate_without_sdk_import():
    adapter = TikHubAdapter()
    payload = {
        "data": {
            "items": [
                {
                    "note_id": "n1",
                    "title": "碳酸锂怎么看",
                    "nickname": "研究员A",
                    "create_time": 123,
                }
            ]
        }
    }
    rows = adapter._normalize(payload, "xiaohongshu")
    assert len(rows) == 1
    assert rows[0]["source_id"] == "n1"
    assert rows[0]["platform"] == "xiaohongshu"
    assert rows[0]["origin_tool"] == "TikHub"
