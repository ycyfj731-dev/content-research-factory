from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .mcp_stdio import MCPStdioConfig, MCPStdioToolClient


@dataclass(frozen=True)
class RedditMCPConfig:
    stdio: MCPStdioConfig


def _items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("results", "posts", "items", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            nested = _items(value)
            if nested:
                return nested
    return []


class RedditMCPAdapter:
    def __init__(self, config: RedditMCPConfig) -> None:
        self.client = MCPStdioToolClient(config.stdio)

    def search(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        payload = self.client.call(
            "reddit_search",
            {"query": query, "limit": max(1, min(limit, 100))},
        )
        rows = _items(payload)
        return [
            {
                "platform": "reddit",
                "source_id": row.get("id") or row.get("name"),
                "url": row.get("permalink") or row.get("url"),
                "author": row.get("author"),
                "title": row.get("title"),
                "text": row.get("selftext") or row.get("body") or row.get("title"),
                "published_at": row.get("created_utc") or row.get("created_at"),
                "origin_tool": "RedditMCP",
                "raw": row,
            }
            for row in rows[:limit]
        ]

    def deep_comment_search(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        payload = self.client.call(
            "reddit_deep_comment_search",
            {"query": query, "limit": max(1, min(limit, 100))},
        )
        rows = _items(payload)
        return [
            {
                "platform": "reddit",
                "source_id": row.get("id") or row.get("comment_id"),
                "parent_source_id": row.get("post_id"),
                "url": row.get("permalink"),
                "author": row.get("author"),
                "text": row.get("body") or row.get("text"),
                "published_at": row.get("created_utc") or row.get("created_at"),
                "origin_tool": "RedditMCP",
                "content_type": "comment",
                "raw": row,
            }
            for row in rows[:limit]
        ]
