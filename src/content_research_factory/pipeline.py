from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Any

from .clients import (
    AgentReachClient,
    MediaCrawlerClient,
    MoneyPrinterTurboClient,
    TrendRadarClient,
)
from .models import EvidenceItem, ResearchPackage


class ContentResearchPipeline:
    def __init__(
        self,
        *,
        trend_radar: TrendRadarClient,
        agent_reach: AgentReachClient,
        media_crawler: MediaCrawlerClient,
        money_printer_turbo: MoneyPrinterTurboClient | None = None,
    ) -> None:
        self.trend_radar = trend_radar
        self.agent_reach = agent_reach
        self.media_crawler = media_crawler
        self.money_printer_turbo = money_printer_turbo

    def run(
        self,
        query: str,
        *,
        discovery_limit: int = 20,
        verification_limit: int = 20,
        deep_limit: int = 10,
        comments_limit: int = 100,
        produce_video: bool = False,
    ) -> ResearchPackage:
        discoveries_raw = self.trend_radar.discover(query, limit=discovery_limit)
        discoveries = [
            self._to_evidence(item, stage="trend_discovery", tool="TrendRadar")
            for item in discoveries_raw
        ]

        verifications_raw = self.agent_reach.verify(
            query,
            candidates=discoveries_raw,
            limit=verification_limit,
        )
        verifications = [
            self._to_evidence(
                item,
                stage="cross_platform_verification",
                tool="Agent-Reach",
            )
            for item in verifications_raw
        ]

        deep_candidates = self.media_crawler.search(query, limit=deep_limit)
        deep_research: list[EvidenceItem] = []

        for item in deep_candidates[:deep_limit]:
            source_id = item.get("source_id") or item.get("id")
            platform = item.get("platform")
            if source_id:
                detail = self.media_crawler.detail(
                    str(source_id),
                    platform=platform,
                )
                comments = self.media_crawler.comments(
                    str(source_id),
                    platform=platform,
                    limit=comments_limit,
                )
                detail = dict(detail)
                detail["comments"] = comments
                deep_research.append(
                    self._to_evidence(
                        detail,
                        stage="chinese_social_deep_research",
                        tool="MediaCrawler",
                    )
                )
            else:
                deep_research.append(
                    self._to_evidence(
                        item,
                        stage="chinese_social_deep_research",
                        tool="MediaCrawler",
                    )
                )

        synthesis = self._synthesize(
            query=query,
            discoveries=discoveries,
            verifications=verifications,
            deep_research=deep_research,
        )

        package = ResearchPackage(
            query=query,
            discoveries=discoveries,
            verifications=verifications,
            deep_research=deep_research,
            synthesis=synthesis,
        )

        if produce_video:
            if self.money_printer_turbo is None:
                raise ValueError(
                    "produce_video=True requires a MoneyPrinterTurbo client"
                )
            handoff = self.money_printer_turbo.produce(asdict(package))
            package = ResearchPackage(
                query=package.query,
                discoveries=package.discoveries,
                verifications=package.verifications,
                deep_research=package.deep_research,
                synthesis=package.synthesis,
                production_handoff=handoff,
            )

        return package

    @staticmethod
    def _to_evidence(
        item: dict[str, Any],
        *,
        stage: str,
        tool: str,
    ) -> EvidenceItem:
        return EvidenceItem(
            stage=stage,
            tool=tool,
            platform=item.get("platform"),
            source_id=item.get("source_id") or item.get("id"),
            url=item.get("url") or item.get("source_url"),
            author=item.get("author") or item.get("nickname"),
            title=item.get("title"),
            text=item.get("text") or item.get("content") or item.get("desc"),
            published_at=item.get("published_at") or item.get("publish_time"),
            engagement=item.get("engagement") or {},
            comments=item.get("comments") or [],
            raw=item,
        )

    @staticmethod
    def _synthesize(
        *,
        query: str,
        discoveries: list[EvidenceItem],
        verifications: list[EvidenceItem],
        deep_research: list[EvidenceItem],
    ) -> dict[str, Any]:
        platforms = Counter(
            item.platform
            for item in [*verifications, *deep_research]
            if item.platform
        )
        comment_count = sum(len(item.comments) for item in deep_research)
        verified_urls = {
            item.url for item in verifications if item.url
        }

        return {
            "query": query,
            "discovery_count": len(discoveries),
            "verification_count": len(verifications),
            "deep_research_count": len(deep_research),
            "comment_count": comment_count,
            "verified_source_count": len(verified_urls),
            "platform_counts": dict(platforms),
            "ready_for_production": bool(verifications or deep_research),
        }
