import json

from content_research_factory.export import write_research_package
from content_research_factory.models import ResearchPackage


def test_write_research_package(tmp_path):
    package = ResearchPackage(
        query="test",
        discoveries=[],
        verifications=[],
        deep_research=[],
        synthesis={"ready_for_production": False},
    )

    output = write_research_package(package, tmp_path / "package.json")

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["query"] == "test"
    assert payload["synthesis"]["ready_for_production"] is False
