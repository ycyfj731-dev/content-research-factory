from __future__ import annotations

from pathlib import Path

from .export import write_research_package
from .reporting import write_brief


SMOKE_QUERY = "AI 生成四格漫画：普通人如何用 AI 做连续角色、持续更新并变现"


def run_smoke_test(pipeline, output_dir: str | Path = "outputs/smoke-test"):
    package = pipeline.run(
        SMOKE_QUERY,
        discovery_limit=8,
        verification_limit=8,
        deep_limit=4,
        comments_limit=20,
        produce_video=False,
    )
    root = Path(output_dir)
    write_research_package(package, root / "research.json")
    write_brief(package, root / "brief.md")
    return package, root
