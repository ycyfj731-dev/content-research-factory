from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from .adapters.agent_reach import AgentReachAdapter, AgentReachConfig
from .adapters.mcp_stdio import MCPStdioConfig
from .adapters.mediacrawler_mcp import MediaCrawlerMCPAdapter
from .adapters.moneyprinterturbo import MoneyPrinterTurboAdapter, MoneyPrinterTurboConfig
from .adapters.trendradar import TrendRadarAdapter
from .export import write_research_package
from .pipeline import ContentResearchPipeline
from .reporting import write_brief


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", value.strip().lower())
    return value.strip("-") or "research"


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing {name}. Run scripts/bootstrap_upstreams.sh and export the printed path."
        )
    return value


def build_pipeline(*, enable_video: bool = False) -> ContentResearchPipeline:
    trend_dir = require_env("TREND_RADAR_DIR")
    media_dir = require_env("MEDIA_CRAWLER_DIR")

    trend = TrendRadarAdapter(
        MCPStdioConfig(
            command="uv",
            args=(
                "--directory",
                trend_dir,
                "run",
                "python",
                "-m",
                "mcp_server.server",
            ),
        )
    )

    reach = AgentReachAdapter(AgentReachConfig())

    media = MediaCrawlerMCPAdapter(
        MCPStdioConfig(
            command="uv",
            args=(
                "--directory",
                media_dir,
                "run",
                "main.py",
            ),
            env={
                **os.environ,
                "ENABLE_GET_COMMENTS": "true",
                "CRAWLER_MAX_NOTES_COUNT": "20",
                "MAX_CONCURRENCY_NUM": "1",
            },
        ),
        project_dir=media_dir,
    )

    money = None
    if enable_video:
        money_dir = require_env("MONEY_PRINTER_TURBO_DIR")
        money = MoneyPrinterTurboAdapter(
            MoneyPrinterTurboConfig(project_dir=money_dir)
        )

    return ContentResearchPipeline(
        trend_radar=trend,
        agent_reach=reach,
        media_crawler=media,
        money_printer_turbo=money,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crf")
    subparsers = parser.add_subparsers(dest="command", required=True)

    research = subparsers.add_parser("research")
    research.add_argument("query")
    research.add_argument(
        "--output-dir",
        default="outputs",
        help="Base directory for generated research artifacts.",
    )
    research.add_argument(
        "--produce-video",
        action="store_true",
        help="Send the completed research package to MoneyPrinterTurbo.",
    )

    args = parser.parse_args(argv)

    if args.command == "research":
        pipeline = build_pipeline(enable_video=args.produce_video)
        package = pipeline.run(
            args.query,
            produce_video=args.produce_video,
        )

        run_dir = Path(args.output_dir) / slugify(args.query)
        write_research_package(package, run_dir / "research.json")
        write_brief(package, run_dir / "brief.md")
        print(run_dir)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
