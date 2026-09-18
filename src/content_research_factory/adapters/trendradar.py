from __future__ import annotations

from typing import Any, Mapping, Sequence

from .mcp_stdio import MCPStdioConfig, MCPStdioToolClient


class TrendRadarAdapter:
    """Adapter for sansan0/TrendRadar's real MCP server."""

    def __init__(
        self,
        config: MCPStdioConfig,
        *,
        search_tool: str = "search_news",
        trending_tool: str = "get_trending_topics",
    ) -> None:
        self.mcp = MCPStdioToolClient(config)
        self.search_tool = search_tool
        self.trending_tool = trending_tool

    def discover(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        search_result = self.mcp.call(
            self.search_tool,
            {
                "query": query,
                "limit": limit,
                "sort_by": "relevance",
                "include_url": True,
                "include_rss": True,
            },
        )
        rows = self._normalize(search_result)

        trending = self.mcp.call(
            self.trending_tool,
            {
                "top_n": min(limit, 20),
                "mode": "current",
                "extract_mode": "auto_extract",
            },
        )
        trends = self._normalize(trending)

        seen = set()
        merged = []
        for item in [*rows, *trends]:
            key = str(item.get("url") or item.get("source_url") or item.get("title") or item)
            if key in seen:
                continue
            seen.add(key)
            row = dict(item)
            row.setdefault("origin_tool", "TrendRadar")
            merged.append(row)
            if len(merged) >= limit:
                break
        return merged

    @staticmethod
    def _normalize(result: Any) -> list[dict[str, Any]]:
        if result is None:
            return []
        if isinstance(result, Mapping):
            for key in ("items", "data", "results", "news", "hot_news", "topics", "trending_topics"):
                value = result.get(key)
                if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                    return [dict(x) for x in value if isinstance(x, Mapping)]
            return [dict(result)]
        if isinstance(result, Sequence) and not isinstance(result, (str, bytes)):
            return [dict(x) for x in result if isinstance(x, Mapping)]
        return [{"text": str(result)}]
