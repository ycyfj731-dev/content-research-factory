from content_research_factory import cli
from content_research_factory.models import ResearchPackage


class FakePipeline:
    def run(self, query):
        return ResearchPackage(
            query=query,
            discoveries=[],
            verifications=[],
            deep_research=[],
            synthesis={
                "discovery_count": 0,
                "verification_count": 0,
                "deep_research_count": 0,
                "comment_count": 0,
                "verified_source_count": 0,
                "platform_counts": {},
                "ready_for_production": False,
            },
        )


def test_cli_writes_artifacts(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "build_pipeline", lambda config: FakePipeline())

    code = cli.main(
        [
            "research",
            "AI 五行饮食",
            "--output-dir",
            str(tmp_path),
        ]
    )

    assert code == 0
    run_dir = tmp_path / "ai-五行饮食"
    assert (run_dir / "research.json").exists()
    assert (run_dir / "brief.md").exists()
