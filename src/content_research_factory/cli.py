from __future__ import annotations

import argparse
import re
from pathlib import Path

from .adapters.agent_reach import AgentReachAdapter
from .adapters.jsonrpc_stdio import JSONRPCStdioConfig
from .adapters.mediacrawler_mcp import MediaCrawlerConfig, MediaCrawlerMCPAdapter
from .adapters.trendradar import TrendRadarAdapter
from .config import load_config
from .export import write_research_package
from .pipeline import ContentResearchPipeline
from .reporting import write_brief


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", value.strip().lower())
    return value.strip("-") or "research"


def build_pipeline(config_path: str | Path) -> ContentResearchPipeline:
    config = load_config(config_path)

    trend_cfg = config["trendradar"]
    reach_cfg = config["agent_reach"]
    media_cfg = config["mediacrawler"]

    trend = TrendRadarAdapter(
        JSONRPCStdioConfig(
            command=trend_cfg["command"],
            args=tuple(trend_cfg.get("args", [])),
            timeout_seconds=int(trend_cfg.get("timeout_seconds", 60)),
        ),
        discover_method=trend_cfg.get("methods", {}).get("discover", "discover"),
    )

    reach = AgentReachAdapter(
        JSONRPCStdioConfig(
            command=reach_cfg["command"],
            args=tuple(reach_cfg.get("args", [])),
            timeout_seconds=int(reach_cfg.get("timeout_seconds", 60)),
        ),
        verify_method=reach_cfg.get("methods", {}).get("verify", "verify"),
    )

    media = MediaCrawlerMCPAdapter(
        MediaCrawlerConfig(
            command=media_cfg["command"],
            args=tuple(media_cfg.get("args", [])),
            timeout_seconds=int(media_cfg.get("timeout_seconds", 60)),
            search_method=media_cfg.get("methods", {}).get("search", "search"),
            detail_method=media_cfg.get("methods", {}).get("detail", "detail"),
            comments_method=media_cfg.get("methods", {}).get("comments", "comments"),
        )
    )

    return ContentResearchPipeline(
        trend_radar=trend,
        agent_reach=reach,
        media_crawler=media,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crf")
    subparsers = parser.add_subparsers(dest="command", required=True)

    research = subparsers.add_parser("research")
    research.add_argument("query")
    research.add_argument(
        "--config",
        default="config/routing.yaml",
        help="Path to repository config.",
    )
    research.add_argument(
        "--output-dir",
        default="outputs",
        help="Base directory for generated research artifacts.",
    )

    args = parser.parse_args(argv)

    if args.command == "research":
        pipeline = build_pipeline(args.config)
        package = pipeline.run(args.query)

        run_dir = Path(args.output_dir) / slugify(args.query)
        write_research_package(package, run_dir / "research.json")
        write_brief(package, run_dir / "brief.md")

        print(run_dir)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
