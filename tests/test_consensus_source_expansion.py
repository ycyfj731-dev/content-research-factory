from datetime import datetime, timezone

from content_research_factory.consensus.collector import ConsensusCollector
from content_research_factory.consensus.discovery import DiscoveryQuery
from content_research_factory.consensus.source_factory import build_source_expansion


NOW = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)


class BaseTrend:
    def discover(self, query, *, limit=20):
        return []


class BaseReach:
    def verify(self, query, *, candidates, limit=20):
        return []


class BaseMedia:
    def search(self, query, *, platform=None, limit=20):
        return []

    def detail(self, source_id, *, platform=None):
        return {}

    def comments(self, source_id, *, platform=None, limit=100):
        return []


class ExtraSource:
    def search(self, query, *, limit=20):
        return [
            {
                "platform": "reddit",
                "source_id": "r1",
                "text": "Lithium carbonate still looks oversupplied",
                "origin_tool": "RedditMCP",
            }
        ]


class BrokenSource:
    def search(self, query, *, limit=20):
        raise RuntimeError("provider unavailable")


def test_no_env_keeps_v01_source_expansion_empty():
    expansion = build_source_expansion({})
    assert expansion.supplemental_sources == ()
    assert expansion.web_crawler is None
    assert expansion.enabled_sources == ()


def test_env_enables_declared_sources_without_importing_optional_sdks():
    expansion = build_source_expansion(
        {
            "TRENDSCOPE_URL": "http://127.0.0.1:8000",
            "REDDITAPIS_KEY": "secret",
            "TIKHUB_API_KEY": "secret2",
            "CRF_ENABLE_CRAWL4AI": "true",
        }
    )
    assert set(expansion.enabled_sources) == {
        "TrendScope",
        "RedditMCP",
        "TikHub",
        "Crawl4AI",
    }


def test_supplemental_source_is_collected_and_covered():
    collector = ConsensusCollector(
        trend_radar=BaseTrend(),
        agent_reach=BaseReach(),
        media_crawler=BaseMedia(),
        supplemental_sources=(("RedditMCP", ExtraSource()),),
    )
    rows = collector.collect(
        [DiscoveryQuery(query="碳酸锂", category="core", priority=1)],
        captured_at=NOW,
    )

    assert len(rows) == 1
    assert rows[0].origin_tool == "RedditMCP"
    coverage = {row.source: row for row in collector.last_coverage}
    assert coverage["RedditMCP"].status == "ok"
    assert coverage["RedditMCP"].records == 1


def test_failed_supplemental_source_does_not_abort_collection():
    collector = ConsensusCollector(
        trend_radar=BaseTrend(),
        agent_reach=BaseReach(),
        media_crawler=BaseMedia(),
        supplemental_sources=(("TikHub", BrokenSource()),),
    )
    rows = collector.collect(
        [DiscoveryQuery(query="碳酸锂", category="core", priority=1)],
        captured_at=NOW,
    )

    assert rows == []
    coverage = {row.source: row for row in collector.last_coverage}
    assert coverage["TikHub"].status == "failed"
    assert "provider unavailable" in coverage["TikHub"].error
