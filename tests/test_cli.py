from content_research_factory import cli
from content_research_factory.doctor import Check
from content_research_factory.models import ResearchPackage


class FakePipeline:
    def run(self, query, *, produce_video=False, **kwargs):
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
            production_handoff=(
                {"status": "completed"} if produce_video else None
            ),
        )


def test_cli_writes_artifacts(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "build_pipeline", lambda enable_video=False: FakePipeline())
    code = cli.main(["research", "AI 五行饮食", "--output-dir", str(tmp_path)])
    assert code == 0
    run_dir = tmp_path / "ai-五行饮食"
    assert (run_dir / "research.json").exists()
    assert (run_dir / "brief.md").exists()


def test_cli_can_enable_video(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "build_pipeline", lambda enable_video=False: FakePipeline())
    code = cli.main([
        "research",
        "AI 五行饮食",
        "--output-dir",
        str(tmp_path),
        "--produce-video",
    ])
    assert code == 0


def test_cli_doctor(monkeypatch):
    monkeypatch.setattr(
        cli,
        "run_doctor",
        lambda: [
            Check("TrendRadar", "READY", "ok"),
            Check("Agent-Reach", "PARTIAL", "some channels need login"),
            Check("MediaCrawler", "READY", "ok"),
            Check("MoneyPrinterTurbo", "NOT_CONFIGURED", "optional"),
        ],
    )
    assert cli.main(["doctor"]) == 0


def test_cli_smoke_test(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "build_pipeline", lambda enable_video=False: FakePipeline())

    def fake_run_smoke_test(pipeline, output_dir):
        root = tmp_path / "smoke"
        package = pipeline.run("test")
        return package, root

    monkeypatch.setattr(cli, "run_smoke_test", fake_run_smoke_test)
    assert cli.main(["smoke-test", "--output-dir", str(tmp_path)]) == 0
