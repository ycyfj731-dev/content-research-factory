from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

from .adapters.agent_reach import AgentReachAdapter, AgentReachConfig
from .adapters.mcp_stdio import MCPStdioConfig
from .adapters.mediacrawler_mcp import MediaCrawlerMCPAdapter
from .adapters.moneyprinterturbo import MoneyPrinterTurboAdapter, MoneyPrinterTurboConfig
from .adapters.trendradar import TrendRadarAdapter
from .consensus.collector import ConsensusCollector, write_jsonl
from .consensus.discovery import build_discovery_plan, plan_as_dicts
from .consensus.runner import score_observation_file
from .doctor import run_doctor
from .export import write_research_package
from .pipeline import ContentResearchPipeline
from .reporting import write_brief
from .smoke import SMOKE_QUERY, run_smoke_test


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

    plan = subparsers.add_parser("consensus-plan")
    plan.add_argument(
        "--config",
        default="config/consensus/lithium_carbonate.yaml",
        help="Consensus asset configuration.",
    )
    plan.add_argument(
        "--dynamic-term",
        action="append",
        default=[],
        help="Optional same-day dynamic term; may be repeated.",
    )

    collect = subparsers.add_parser("consensus-collect")
    collect.add_argument(
        "--config",
        default="config/consensus/lithium_carbonate.yaml",
        help="Consensus asset configuration.",
    )
    collect.add_argument(
        "--output",
        default="outputs/consensus/raw/lithium_carbonate.jsonl",
        help="Append-only raw evidence JSONL.",
    )
    collect.add_argument(
        "--max-queries",
        type=int,
        default=None,
        help="Optional cap for smoke/testing; production should normally run the full plan.",
    )
    collect.add_argument(
        "--dynamic-term",
        action="append",
        default=[],
        help="Optional same-day dynamic term; may be repeated.",
    )
    collect.add_argument("--comments-limit", type=int, default=50)
    collect.add_argument("--deep-posts-per-query", type=int, default=2)

    consensus = subparsers.add_parser("consensus-score")
    consensus.add_argument("input", help="JSON observations file.")
    consensus.add_argument(
        "--config",
        default="config/consensus/lithium_carbonate.yaml",
        help="Consensus asset configuration.",
    )
    consensus.add_argument(
        "--now",
        default=None,
        help="Optional ISO-8601 scoring timestamp with timezone.",
    )

    subparsers.add_parser("doctor")

    smoke = subparsers.add_parser("smoke-test")
    smoke.add_argument(
        "--output-dir",
        default="outputs/smoke-test",
        help="Directory for the fixed first smoke-test artifacts.",
    )

    args = parser.parse_args(argv)

    if args.command == "consensus-plan":
        plan_items = build_discovery_plan(
            args.config,
            dynamic_terms=args.dynamic_term,
        )
        print(json.dumps(plan_as_dicts(plan_items), ensure_ascii=False, indent=2))
        return 0

    if args.command == "consensus-collect":
        plan_items = build_discovery_plan(
            args.config,
            dynamic_terms=args.dynamic_term,
        )
        if args.max_queries is not None:
            plan_items = plan_items[: max(0, args.max_queries)]
        pipeline = build_pipeline(enable_video=False)
        collector = ConsensusCollector(
            trend_radar=pipeline.trend_radar,
            agent_reach=pipeline.agent_reach,
            media_crawler=pipeline.media_crawler,
        )
        records = collector.collect(
            plan_items,
            comments_limit=args.comments_limit,
            deep_posts_per_query=args.deep_posts_per_query,
        )
        target = write_jsonl(records, args.output)
        print(json.dumps({
            "output": str(target),
            "queries": len(plan_items),
            "records": len(records),
        }, ensure_ascii=False, indent=2))
        return 0

    if args.command == "consensus-score":
        now = None
        if args.now:
            now = datetime.fromisoformat(args.now.replace("Z", "+00:00"))
            if now.tzinfo is None:
                raise ValueError("--now must include a timezone")
        result = score_observation_file(
            args.input,
            config_path=args.config,
            now=now,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == "doctor":
        checks = run_doctor()
        for check in checks:
            print(f"{check.name:20} {check.status:14} {check.detail}")
        return 0 if all(c.status in {"READY", "PARTIAL", "NOT_CONFIGURED"} for c in checks) else 1

    if args.command == "smoke-test":
        pipeline = build_pipeline(enable_video=False)
        package, root = run_smoke_test(pipeline, args.output_dir)
        print(f"query: {SMOKE_QUERY}")
        print(f"output: {root}")
        print(f"discoveries: {len(package.discoveries)}")
        print(f"verifications: {len(package.verifications)}")
        print(f"deep_research: {len(package.deep_research)}")
        print(f"comments: {package.synthesis.get('comment_count', 0)}")
        return 0

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
