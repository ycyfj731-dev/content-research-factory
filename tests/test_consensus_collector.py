from datetime import datetime, timezone

from content_research_factory.consensus.collector import ConsensusCollector
from content_research_factory.consensus.discovery import DiscoveryQuery


NOW = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)


class FakeTrend:
    def discover(self, query, *, limit=20):
        return [
            {
                "title": "碳酸锂仓单继续下降",
                "url": "https://example.com/news/1",
                "origin_tool": "TrendRadar",
            }
        ]


class FakeReach:
    def verify(self, query, *, candidates, limit=20):
        return [
            {
                "platform": "weibo",
                "source_id": "wb-1",
                "text": "我觉得碳酸锂短期偏多",
                "origin_tool": "Agent-Reach",
            }
        ]


class FakeMedia:
    def search(self, query, *, platform=None, limit=20):
        return [
            {
                "platform": "xhs",
                "source_id": "xhs-1",
                "text": "仓单一直注销，现货更强",
                "origin_tool": "MediaCrawler",
            }
        ]

    def detail(self, source_id, *, platform=None):
        return {
            "platform": platform,
            "source_id": source_id,
            "text": "仓单一直注销，现货更强",
            "origin_tool": "MediaCrawler",
        }

    def comments(self, source_id, *, platform=None, limit=100):
        return [
            {
                "platform": platform,
                "source_id": "comment-1",
                "text": "空头要小心了",
                "origin_tool": "MediaCrawler",
            },
            {
                "platform": platform,
                "source_id": "comment-2",
                "text": "供应恢复还是会跌",
                "origin_tool": "MediaCrawler",
            },
        ]


def test_collector_combines_discovery_verification_social_and_comments():
    collector = ConsensusCollector(
        trend_radar=FakeTrend(),
        agent_reach=FakeReach(),
        media_crawler=FakeMedia(),
    )
    plan = [DiscoveryQuery(query="碳酸锂 仓单", category="physical_market", priority=1)]

    rows = collector.collect(plan, captured_at=NOW)

    assert len(rows) == 5
    assert {row.origin_tool for row in rows} == {"TrendRadar", "Agent-Reach", "MediaCrawler"}
    comments = [row for row in rows if row.content_type == "comment"]
    assert len(comments) == 2
    assert all(row.parent_source_id == "xhs-1" for row in comments)
    assert all(row.discovery_lane == "web_wide" for row in rows)


class DuplicateMedia(FakeMedia):
    def search(self, query, *, platform=None, limit=20):
        row = {
            "platform": "xhs",
            "source_id": "same",
            "text": "same",
            "origin_tool": "MediaCrawler",
        }
        return [row, dict(row)]

    def comments(self, source_id, *, platform=None, limit=100):
        return []


def test_collector_exact_deduplicates_same_source():
    collector = ConsensusCollector(
        trend_radar=FakeTrend(),
        agent_reach=FakeReach(),
        media_crawler=DuplicateMedia(),
    )
    plan = [DiscoveryQuery(query="碳酸锂", category="core", priority=1)]

    rows = collector.collect(plan, captured_at=NOW)

    social = [row for row in rows if row.source_id == "same"]
    assert len(social) == 1
