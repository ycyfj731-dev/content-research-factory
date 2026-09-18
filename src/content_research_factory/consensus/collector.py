from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from ..clients import AgentReachClient, MediaCrawlerClient, TrendRadarClient
from .discovery import DiscoveryQuery


@dataclass(frozen=True)
class RawConsensusEvidence:
    captured_at: str
    query: str
    query_category: str
    discovery_lane: str
    origin_tool: str
    platform: str | None
    source_id: str | None
    parent_source_id: str | None
    url: str | None
    author: str | None
    title: str | None
    text: str | None
    published_at: str | None
    content_type: str
    raw_hash: str
    raw: dict[str, Any]


def _first(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return None


def _stable_hash(*parts: Any) -> str:
    payload = "\n".join("" if part is None else str(part) for part in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _source_key(item: dict[str, Any]) -> str:
    source_id = _first(item, "source_id", "id", "note_id", "aweme_id", "video_id")
    url = _first(item, "url", "source_url", "share_url")
    platform = item.get("platform")
    text = _first(item, "text", "content", "desc", "title")
    return _stable_hash(platform, source_id, url, text)


def _normalize_item(
    item: dict[str, Any],
    *,
    query: DiscoveryQuery,
    captured_at: str,
    default_tool: str,
    content_type: str = "post",
    parent_source_id: str | None = None,
) -> RawConsensusEvidence:
    source_id = _first(item, "source_id", "id", "note_id", "aweme_id", "video_id")
    platform = item.get("platform")
    url = _first(item, "url", "source_url", "share_url")
    author = _first(item, "author", "nickname", "user_name", "screen_name")
    title = item.get("title")
    text = _first(item, "text", "content", "desc", "comment_content")
    published_at = _first(item, "published_at", "publish_time", "create_time", "created_at")
    origin_tool = str(item.get("origin_tool") or default_tool)

    return RawConsensusEvidence(
        captured_at=captured_at,
        query=query.query,
        query_category=query.category,
        discovery_lane=query.lane,
        origin_tool=origin_tool,
        platform=str(platform) if platform is not None else None,
        source_id=str(source_id) if source_id is not None else None,
        parent_source_id=parent_source_id,
        url=str(url) if url is not None else None,
        author=str(author) if author is not None else None,
        title=str(title) if title is not None else None,
        text=str(text) if text is not None else None,
        published_at=str(published_at) if published_at is not None else None,
        content_type=content_type,
        raw_hash=_source_key(item),
        raw=dict(item),
    )


class ConsensusCollector:
    def __init__(
        self,
        *,
        trend_radar: TrendRadarClient,
        agent_reach: AgentReachClient,
        media_crawler: MediaCrawlerClient,
    ) -> None:
        self.trend_radar = trend_radar
        self.agent_reach = agent_reach
        self.media_crawler = media_crawler

    def collect(
        self,
        plan: Iterable[DiscoveryQuery],
        *,
        discovery_limit: int = 8,
        verification_limit: int = 12,
        social_limit: int = 12,
        deep_posts_per_query: int = 2,
        comments_limit: int = 50,
        captured_at: datetime | None = None,
    ) -> list[RawConsensusEvidence]:
        now = captured_at or datetime.now(timezone.utc)
        if now.tzinfo is None:
            raise ValueError("captured_at must be timezone-aware")
        captured = now.isoformat()

        records: list[RawConsensusEvidence] = []
        seen: set[str] = set()

        def append(record: RawConsensusEvidence) -> None:
            key = _stable_hash(
                record.platform,
                record.source_id,
                record.parent_source_id,
                record.url,
                record.text,
                record.content_type,
            )
            if key in seen:
                return
            seen.add(key)
            records.append(record)

        for query in plan:
            discovered = self.trend_radar.discover(
                query.query,
                limit=discovery_limit,
            )
            for item in discovered:
                append(
                    _normalize_item(
                        item,
                        query=query,
                        captured_at=captured,
                        default_tool="TrendRadar",
                    )
                )

            verified = self.agent_reach.verify(
                query.query,
                candidates=discovered,
                limit=verification_limit,
            )
            for item in verified:
                append(
                    _normalize_item(
                        item,
                        query=query,
                        captured_at=captured,
                        default_tool="Agent-Reach",
                    )
                )

            social = self.media_crawler.search(
                query.query,
                limit=social_limit,
            )
            for item in social:
                append(
                    _normalize_item(
                        item,
                        query=query,
                        captured_at=captured,
                        default_tool="MediaCrawler",
                    )
                )

            deep_count = 0
            for item in social:
                if deep_count >= deep_posts_per_query:
                    break
                source_id = _first(
                    item,
                    "source_id",
                    "id",
                    "note_id",
                    "aweme_id",
                    "video_id",
                )
                if source_id is None:
                    continue
                platform = item.get("platform")
                source_id_str = str(source_id)

                detail = self.media_crawler.detail(
                    source_id_str,
                    platform=platform,
                )
                append(
                    _normalize_item(
                        detail,
                        query=query,
                        captured_at=captured,
                        default_tool="MediaCrawler",
                    )
                )

                comments = self.media_crawler.comments(
                    source_id_str,
                    platform=platform,
                    limit=comments_limit,
                )
                for comment in comments:
                    append(
                        _normalize_item(
                            comment,
                            query=query,
                            captured_at=captured,
                            default_tool="MediaCrawler",
                            content_type="comment",
                            parent_source_id=source_id_str,
                        )
                    )
                deep_count += 1

        return records


def write_jsonl(
    records: Iterable[RawConsensusEvidence],
    path: str | Path,
) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(
                json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)
            )
            handle.write("\n")
    return target
