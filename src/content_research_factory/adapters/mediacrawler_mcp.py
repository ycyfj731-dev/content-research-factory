from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class MediaCrawlerError(RuntimeError):
    """Raised when the MediaCrawler MCP process returns an invalid response."""


@dataclass(frozen=True)
class MediaCrawlerConfig:
    command: str
    args: tuple[str, ...] = ()
    timeout_seconds: int = 60
    search_method: str = "search"
    detail_method: str = "detail"
    comments_method: str = "comments"


class MediaCrawlerMCPAdapter:
    """Small JSON-RPC-over-stdio adapter around a MediaCrawler MCP process.

    The factory talks to this normalized interface rather than importing
    MediaCrawler internals directly.
    """

    def __init__(self, config: MediaCrawlerConfig):
        self.config = config
        self._next_id = 1

    def search(
        self,
        query: str,
        *,
        platform: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"query": query, "limit": limit}
        if platform:
            params["platform"] = platform
        result = self._call(self.config.search_method, params)
        return self._normalize_items(result, kind="search")

    def detail(
        self,
        source_id: str,
        *,
        platform: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"source_id": source_id}
        if platform:
            params["platform"] = platform
        result = self._call(self.config.detail_method, params)
        if not isinstance(result, Mapping):
            raise MediaCrawlerError("detail result must be an object")
        return self._normalize_item(dict(result), kind="detail")

    def comments(
        self,
        source_id: str,
        *,
        platform: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"source_id": source_id, "limit": limit}
        if platform:
            params["platform"] = platform
        result = self._call(self.config.comments_method, params)
        return self._normalize_items(result, kind="comment")

    def _call(self, method: str, params: Mapping[str, Any]) -> Any:
        request_id = self._next_id
        self._next_id += 1

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": dict(params),
        }

        proc = subprocess.run(
            [self.config.command, *self.config.args],
            input=json.dumps(payload, ensure_ascii=False) + "\n",
            text=True,
            capture_output=True,
            timeout=self.config.timeout_seconds,
            check=False,
        )

        if proc.returncode != 0:
            raise MediaCrawlerError(
                f"MediaCrawler process failed ({proc.returncode}): "
                f"{proc.stderr.strip()}"
            )

        stdout = proc.stdout.strip()
        if not stdout:
            raise MediaCrawlerError("MediaCrawler returned no response")

        try:
            response = json.loads(stdout.splitlines()[-1])
        except json.JSONDecodeError as exc:
            raise MediaCrawlerError("MediaCrawler returned invalid JSON") from exc

        if response.get("id") != request_id:
            raise MediaCrawlerError("Mismatched JSON-RPC response id")
        if "error" in response:
            raise MediaCrawlerError(str(response["error"]))
        if "result" not in response:
            raise MediaCrawlerError("JSON-RPC response has no result")

        return response["result"]

    @staticmethod
    def _normalize_items(result: Any, *, kind: str) -> list[dict[str, Any]]:
        if isinstance(result, Mapping):
            if isinstance(result.get("items"), Sequence) and not isinstance(
                result.get("items"), (str, bytes)
            ):
                items = result["items"]
            elif isinstance(result.get("data"), Sequence) and not isinstance(
                result.get("data"), (str, bytes)
            ):
                items = result["data"]
            else:
                items = [result]
        elif isinstance(result, Sequence) and not isinstance(result, (str, bytes)):
            items = result
        else:
            raise MediaCrawlerError(f"{kind} result must contain item objects")

        normalized: list[dict[str, Any]] = []
        for item in items:
            if not isinstance(item, Mapping):
                raise MediaCrawlerError(f"{kind} item must be an object")
            normalized.append(
                MediaCrawlerMCPAdapter._normalize_item(dict(item), kind=kind)
            )
        return normalized

    @staticmethod
    def _normalize_item(item: dict[str, Any], *, kind: str) -> dict[str, Any]:
        source_id = (
            item.get("source_id")
            or item.get("id")
            or item.get("note_id")
            or item.get("aweme_id")
        )
        return {
            "kind": kind,
            "source_id": source_id,
            "platform": item.get("platform"),
            "url": item.get("url") or item.get("source_url"),
            "author": item.get("author") or item.get("nickname"),
            "title": item.get("title"),
            "text": item.get("text") or item.get("content") or item.get("desc"),
            "published_at": item.get("published_at") or item.get("publish_time"),
            "engagement": item.get("engagement") or {},
            "raw": item,
            "origin_tool": "MediaCrawler",
        }
