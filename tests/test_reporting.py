from content_research_factory.models import EvidenceItem, ResearchPackage
from content_research_factory.reporting import write_brief


def test_write_brief(tmp_path):
    package = ResearchPackage(
        query="AI 家居",
        discoveries=[],
        verifications=[],
        deep_research=[
            EvidenceItem(
                stage="chinese_social_deep_research",
                tool="MediaCrawler",
                platform="xiaohongshu",
                source_id="x1",
                title="示例帖子",
                comments=[{"id": "c1"}],
            )
        ],
        synthesis={
            "discovery_count": 1,
            "verification_count": 1,
            "deep_research_count": 1,
            "comment_count": 1,
            "verified_source_count": 1,
            "platform_counts": {"xiaohongshu": 1},
            "ready_for_production": True,
        },
    )

    output = write_brief(package, tmp_path / "brief.md")
    text = output.read_text(encoding="utf-8")

    assert "# Research Brief: AI 家居" in text
    assert "xiaohongshu: 1" in text
    assert "示例帖子" in text
