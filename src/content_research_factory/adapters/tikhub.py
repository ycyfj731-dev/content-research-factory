from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class TikHubUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class TikHubConfig:
    api_key: str | None = None
    timeout_seconds: float = 30.0
    platforms: tuple[str, ...] = ("douyin", "xiaohongshu", "weibo")


def _plain(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if hasattr(value, "model_dump"):
        return _plain(value.model_dump())
    if hasattr(value, "dict"):
        return _plain(value.dict())
    return str(value)


def _collect_candidates(value: Any) -> list[dict[str, Any]]:
    value = _plain(value)
    rows: list[dict[str, Any]] = []
    if isinstance(value, list):
        for item in value:
            rows.extend(_collect_candidates(item))
    elif isinstance(value, dict):
        if any(
            key in value
            for key in (
                "desc",
                "title",
                "content",
                "text",
                "note_id",
                "aweme_id",
                "mblogid",
                "mid",
            )
        ):
            rows.append(value)
        for child in value.values():
            if isinstance(child, (dict, list)):
                rows.extend(_collect_candidates(child))
    return rows


class TikHubAdapter:
    def __init__(self, config: TikHubConfig | None = None) -> None:
        self.config = config or TikHubConfig()

    def _client(self):
        try:
            from tikhub import TikHub
        except ImportError as exc:
            raise TikHubUnavailable(
                "tikhub is not installed; install the 'sources' extra"
            ) from exc
        return TikHub(
            api_key=self.config.api_key,
            timeout=self.config.timeout_seconds,
        )

    def search(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        all_rows: list[dict[str, Any]] = []
        with self._client() as client:
            if "douyin" in self.config.platforms:
                payload = client.douyin_search.fetch_general_search_v1(
                    keyword=query,
                    cursor=0,
                    sort_type="0",
                    publish_time="0",
                    filter_duration="0",
                    content_type="0",
                    search_id="",
                    backtrace="",
                )
                all_rows.extend(self._normalize(payload, "douyin"))

            if "xiaohongshu" in self.config.platforms:
                payload = client.xiaohongshu_web.search_notes(
                    keyword=query,
                    page=1,
                    sort="general",
                    noteType="_0",
                    noteTime="",
                )
                all_rows.extend(self._normalize(payload, "xiaohongshu"))

            if "weibo" in self.config.platforms:
                payload = client.weibo_web.fetch_search(
                    keyword=query,
                    page=1,
                )
                all_rows.extend(self._normalize(payload, "weibo"))

        unique: list[dict[str, Any]] = []
        seen: set[str] = set()
        for row in all_rows:
            key = str(row.get("source_id") or row.get("url") or row.get("text"))
            if not key or key in seen:
                continue
            seen.add(key)
            unique.append(row)
            if len(unique) >= limit:
                break
        return unique

    def _normalize(self, payload: Any, platform: str) -> list[dict[str, Any]]:
        rows = _collect_candidates(payload)
        normalized: list[dict[str, Any]] = []
        for row in rows:
            source_id = (
                row.get("note_id")
                or row.get("aweme_id")
                or row.get("mblogid")
                or row.get("mid")
                or row.get("id")
            )
            text = (
                row.get("desc")
                or row.get("title")
                or row.get("content")
                or row.get("text")
            )
            if not text:
                continue
            normalized.append(
                {
                    "platform": platform,
                    "source_id": source_id,
                    "url": row.get("url")
                    or row.get("share_url")
                    or row.get("note_url"),
                    "author": row.get("nickname")
                    or row.get("screen_name")
                    or row.get("author"),
                    "title": row.get("title"),
                    "text": text,
                    "published_at": row.get("create_time")
                    or row.get("created_at")
                    or row.get("time"),
                    "origin_tool": "TikHub",
                    "raw": row,
                }
            )
        return normalized
