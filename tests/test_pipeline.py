from content_research_factory.pipeline import ContentResearchPipeline


class FakeTrendRadar:
    def discover(self, query, *, limit=20):
        return [
            {
                "id": "trend-1",
                "platform": "web",
                "title": "Topic is rising",
                "url": "https://example.com/trend",
            }
        ]


class FakeAgentReach:
    def verify(self, query, *, candidates, limit=20):
        assert candidates
        return [
            {
                "id": "verify-1",
                "platform": "youtube",
                "title": "Independent mention",
                "url": "https://example.com/verify",
            }
        ]


class FakeMediaCrawler:
    def search(self, query, *, platform=None, limit=20):
        return [
            {
                "source_id": "xhs-1",
                "platform": "xiaohongshu",
                "title": "小红书帖子",
            }
        ]

    def detail(self, source_id, *, platform=None):
        assert source_id == "xhs-1"
        return {
            "source_id": source_id,
            "platform": platform,
            "author": "creator",
            "content": "深度正文",
            "url": "https://example.com/xhs-1",
        }

    def comments(self, source_id, *, platform=None, limit=100):
        return [
            {"id": "c1", "text": "想买"},
            {"id": "c2", "text": "哪里可以买"},
        ]


class FakeMoneyPrinterTurbo:
    def produce(self, research_package):
        assert research_package["synthesis"]["ready_for_production"] is True
        return {"status": "accepted", "job_id": "video-1"}


def test_pipeline_routes_in_fixed_order_and_builds_package():
    pipeline = ContentResearchPipeline(
        trend_radar=FakeTrendRadar(),
        agent_reach=FakeAgentReach(),
        media_crawler=FakeMediaCrawler(),
    )

    package = pipeline.run("AI 家居")

    assert len(package.discoveries) == 1
    assert package.discoveries[0].tool == "TrendRadar"
    assert package.verifications[0].tool == "Agent-Reach"
    assert package.deep_research[0].tool == "MediaCrawler"
    assert package.synthesis["comment_count"] == 2
    assert package.synthesis["ready_for_production"] is True


def test_pipeline_handoff_to_moneyprinterturbo():
    pipeline = ContentResearchPipeline(
        trend_radar=FakeTrendRadar(),
        agent_reach=FakeAgentReach(),
        media_crawler=FakeMediaCrawler(),
        money_printer_turbo=FakeMoneyPrinterTurbo(),
    )

    package = pipeline.run("AI 家居", produce_video=True)

    assert package.production_handoff == {
        "status": "accepted",
        "job_id": "video-1",
    }
