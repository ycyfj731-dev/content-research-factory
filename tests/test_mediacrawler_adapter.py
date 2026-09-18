import json
from types import SimpleNamespace

import pytest

from content_research_factory.adapters.mediacrawler_mcp import (
    MediaCrawlerConfig,
    MediaCrawlerError,
    MediaCrawlerMCPAdapter,
)


def test_search_normalizes_result(monkeypatch):
    def fake_run(*args, **kwargs):
        request = json.loads(kwargs["input"])
        assert request["method"] == "search"
        return SimpleNamespace(
            returncode=0,
            stderr="",
            stdout=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": {
                        "items": [
                            {
                                "id": "abc",
                                "platform": "xiaohongshu",
                                "content": "example",
                                "nickname": "creator",
                            }
                        ]
                    },
                }
            ),
        )

    monkeypatch.setattr("subprocess.run", fake_run)

    adapter = MediaCrawlerMCPAdapter(MediaCrawlerConfig(command="dummy"))
    rows = adapter.search("AI 家居")

    assert rows[0]["source_id"] == "abc"
    assert rows[0]["text"] == "example"
    assert rows[0]["author"] == "creator"
    assert rows[0]["origin_tool"] == "MediaCrawler"


def test_rpc_error_is_raised(monkeypatch):
    def fake_run(*args, **kwargs):
        request = json.loads(kwargs["input"])
        return SimpleNamespace(
            returncode=0,
            stderr="",
            stdout=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "error": {"message": "boom"},
                }
            ),
        )

    monkeypatch.setattr("subprocess.run", fake_run)

    adapter = MediaCrawlerMCPAdapter(MediaCrawlerConfig(command="dummy"))

    with pytest.raises(MediaCrawlerError):
        adapter.search("test")
