from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class TrendScopeConfig:
    base_url: str = "http://127.0.0.1:8000"
    api_key: str | None = None
    timeout_seconds: float = 30.0


def _walk_items(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, list):
        for item in value:
            rows.extend(_walk_items(item))
    elif isinstance(value, dict):
        if any(
            key in value
            for key in (
                "title",
                "text",
                "content",
                "url",
                "source",
                "platform",
                "sentiment",
                "score",
            )
        ):
            rows.append(value)
        for child in value.values():
            if isinstance(child, (dict, list)):
                rows.extend(_walk_items(child))
    return rows


class TrendScopeAdapter:
    def __init__(self, config: TrendScopeConfig | None = None) -> None:
        self.config = config or TrendScopeConfig()

    def search(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        params = urlencode({"topic": query})
        url = f"{self.config.base_url.rstrip('/')}/trends?{params}"
        headers = {"Accept": "application/json"}
        if self.config.api_key:
            headers["X-API-Key"] = self.config.api_key

        request = Request(url, headers=headers, method="GET")
        with urlopen(request, timeout=self.config.timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))

        rows = _walk_items(payload)
        normalized: list[dict[str, Any]] = []
        seen: set[str] = set()

        for row in rows:
            text = (
                row.get("text")
                or row.get("content")
                or row.get("title")
                or row.get("name")
            )
            if text is None:
                continue
            source = str(
                row.get("platform")
                or row.get("source")
                or row.get("provider")
                or "trendscope"
            )
            url_value = row.get("url") or row.get("link") or row.get("permalink")
            key = f"{source}\n{url_value}\n{text}"
            if key in seen:
                continue
            seen.add(key)
            normalized.append(
                {
                    "platform": source,
                    "source_id": row.get("id") or row.get("source_id") or url_value,
                    "url": url_value,
                    "author": row.get("author") or row.get("username"),
                    "title": row.get("title"),
                    "text": text,
                    "published_at": row.get("published_at")
                    or row.get("created_at")
                    or row.get("timestamp"),
                    "origin_tool": "TrendScope",
                    "raw": row,
                }
            )
            if len(normalized) >= limit:
                break

        return normalized
