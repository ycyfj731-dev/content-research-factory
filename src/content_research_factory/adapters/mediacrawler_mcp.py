from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .mcp_stdio import MCPStdioConfig, MCPStdioToolClient


class MediaCrawlerError(RuntimeError):
    pass


class MediaCrawlerMCPAdapter:
    """Adapter for Bowenwin/MediaCrawler_MCP_Server.

    Upstream crawl tools write records to storage instead of returning post arrays.
    This adapter uses JSON storage and reads the generated content/comment files.
    """

    PLATFORM_ALIASES = {
        "xiaohongshu": "xhs", "xhs": "xhs",
        "douyin": "dy", "dy": "dy",
        "kuaishou": "ks", "ks": "ks",
        "bilibili": "bili", "bili": "bili",
        "weibo": "wb", "wb": "wb",
        "tieba": "tieba", "zhihu": "zhihu",
    }

    def __init__(
        self,
        config: MCPStdioConfig,
        *,
        project_dir: str | Path,
        platforms: tuple[str, ...] = ("xhs", "dy", "bili", "wb"),
        search_tool: str = "crawl_search",
        detail_tool: str = "crawl_detail",
    ):
        self.mcp = MCPStdioToolClient(config)
        self.project_dir = Path(project_dir)
        self.platforms = tuple(self._platform(p) for p in platforms)
        self.search_tool = search_tool
        self.detail_tool = detail_tool

    def search(self, query: str, *, platform: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        platforms = [self._platform(platform)] if platform else list(self.platforms)
        rows = []
        for current in platforms:
            before = self._snapshot(current)
            self.mcp.call(
                self.search_tool,
                {"platform": current, "store_type": "json", "keywords": query},
            )
            rows.extend(self._read_new_records(current, before, kind="content"))
            if len(rows) >= limit:
                break
        return rows[:limit]

    def detail(self, source_id: str, *, platform: str | None = None) -> dict[str, Any]:
        current = self._platform(platform or "xhs")
        before = self._snapshot(current)
        self.mcp.call(
            self.detail_tool,
            {"platform": current, "store_type": "json", "video_id": [source_id]},
        )
        rows = self._read_new_records(current, before, kind="content")
        if rows:
            return rows[-1]
        return {"source_id": source_id, "platform": current, "origin_tool": "MediaCrawler"}

    def comments(self, source_id: str, *, platform: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
        current = self._platform(platform or "xhs")
        rows = []
        for path in reversed(self._json_files(current, kind="comment")):
            for row in self._read_json_records(path):
                row_source = row.get("source_id") or row.get("note_id") or row.get("aweme_id") or row.get("video_id")
                if row_source is None or str(row_source) == str(source_id):
                    item = dict(row)
                    item.setdefault("platform", current)
                    item.setdefault("origin_tool", "MediaCrawler")
                    rows.append(item)
                    if len(rows) >= limit:
                        return rows
        return rows

    def _snapshot(self, platform: str) -> set[Path]:
        return set(self._json_files(platform, kind="content")) | set(self._json_files(platform, kind="comment"))

    def _read_new_records(self, platform: str, before: set[Path], *, kind: str) -> list[dict[str, Any]]:
        files = [p for p in self._json_files(platform, kind=kind) if p not in before]
        if not files:
            files = self._json_files(platform, kind=kind)[-2:]
        rows = []
        for path in files:
            for row in self._read_json_records(path):
                item = dict(row)
                item.setdefault("platform", platform)
                item.setdefault("origin_tool", "MediaCrawler")
                rows.append(item)
        return rows

    def _json_files(self, platform: str, *, kind: str) -> list[Path]:
        roots = [self.project_dir / "data" / platform, self.project_dir / "data"]
        patterns = ["*comment*.json", "*comments*.json"] if kind == "comment" else ["*content*.json", "*contents*.json", "*search*.json"]
        files = set()
        for root in roots:
            if not root.exists():
                continue
            for pattern in patterns:
                files.update(root.rglob(pattern))
        return sorted(files, key=lambda p: p.stat().st_mtime)

    @staticmethod
    def _read_json_records(path: Path) -> list[dict[str, Any]]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict):
            for key in ("items", "data", "records"):
                if isinstance(value.get(key), list):
                    return [x for x in value[key] if isinstance(x, dict)]
            return [value]
        return []

    @classmethod
    def _platform(cls, value: str) -> str:
        key = value.lower()
        if key not in cls.PLATFORM_ALIASES:
            raise MediaCrawlerError(f"Unsupported MediaCrawler platform: {value}")
        return cls.PLATFORM_ALIASES[key]
