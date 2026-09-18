# CONTENT-RESEARCH-FACTORY

Research-to-production pipeline for content discovery, cross-platform verification, Chinese social deep research, comments, and optional video production.

## Fixed routing

| Tool | Responsibility |
|---|---|
| TrendRadar | 热点发现 |
| Agent-Reach | 跨平台验证 |
| MediaCrawler | 中文社媒深抓和评论 |
| MoneyPrinterTurbo | 视频生产 |

This routing is a project invariant.

## Real upstreams

The runtime is wired to these upstream projects:

- TrendRadar: sansan0/TrendRadar
  - interface: MCP
  - tools used: search_news, get_trending_topics
- Agent-Reach: Panniantong/Agent-Reach
  - interface: capability router + platform CLIs
  - health check: agent-reach doctor --json
- MediaCrawler MCP: Bowenwin/MediaCrawler_MCP_Server
  - based on NanmiCoder/MediaCrawler
  - interface: MCP
  - tools used: crawl_search, crawl_detail
- MoneyPrinterTurbo: harry0703/MoneyPrinterTurbo
  - interface: CLI
  - production entry: uv run python cli.py --video-subject ...

See config/upstreams.yaml for the pinned integration contract.

## Important license note

Bowenwin/MediaCrawler_MCP_Server states in its source header that it is for learning and research and must not be used commercially.

That means CONTENT-RESEARCH-FACTORY can use this adapter for research/testing, but a commercial deployment must replace or separately clear the MediaCrawler layer before production use.

## Install

Requires:

- Python 3.11+
- git
- uv

### Windows PowerShell

Run:

    .\scripts\bootstrap_upstreams.ps1
    python -m pip install -e ".[test]"

The PowerShell bootstrap sets these variables for the current shell:

- TREND_RADAR_DIR
- MEDIA_CRAWLER_DIR
- MONEY_PRINTER_TURBO_DIR

### macOS / Linux

Run:

    bash scripts/bootstrap_upstreams.sh
    export TREND_RADAR_DIR=.vendor/TrendRadar
    export MEDIA_CRAWLER_DIR=.vendor/MediaCrawler_MCP_Server
    export MONEY_PRINTER_TURBO_DIR=.vendor/MoneyPrinterTurbo
    python -m pip install -e ".[test]"

## Research

Run:

    crf research "AI 五行饮食"

Artifacts are written to:

    outputs/
    └── ai-五行饮食/
        ├── research.json
        └── brief.md

## Research + video production

Run:

    crf research "AI 五行饮食" --produce-video

MoneyPrinterTurbo is only invoked when --produce-video is explicitly supplied.

## Pipeline

    TrendRadar
      -> Agent-Reach
      -> MediaCrawler
      -> ResearchPackage
      -> synthesis
      -> optional MoneyPrinterTurbo

## Agent-Reach verification behavior

Agent-Reach is not treated as a fictional single verify API.

The adapter first runs:

    agent-reach doctor --json

Then it uses the documented read-only backend command for configured platforms, currently:

- Bilibili: bili search
- Twitter/X: twitter search or OpenCLI
- Reddit: rdt search or OpenCLI
- XiaoHongShu: OpenCLI

Unavailable or unconfigured platform backends are skipped instead of being fabricated.

## MediaCrawler behavior

The MediaCrawler MCP tools primarily write crawl results to storage.

The adapter therefore:

1. calls crawl_search or crawl_detail through real MCP stdio;
2. forces JSON storage;
3. reads the newly generated content/comment JSON files;
4. normalizes them into the factory evidence schema.

## Tests

Run:

    pytest -q

GitHub Actions configuration is in .github/workflows/test.yml.


## Health check

After bootstrap, run:

    crf doctor

Expected status classes:

- READY
- PARTIAL
- NOT_CONFIGURED
- FAIL

MoneyPrinterTurbo may be NOT_CONFIGURED when only research is needed.

## First smoke test

The repository has one fixed first smoke-test topic:

    AI 生成四格漫画：普通人如何用 AI 做连续角色、持续更新并变现

Run:

    crf smoke-test

The smoke test intentionally uses smaller limits than a full research run and writes:

    outputs/smoke-test/research.json
    outputs/smoke-test/brief.md

Run `crf doctor` first. Do not treat a smoke test as successful unless the real upstreams execute and the generated research package contains actual retrieved evidence.


## Market Consensus Radar

The repository now includes a V0.1 consensus-scoring layer for financial social research.

Initial asset:

    GFEX lithium carbonate (LC)

Key files:

    skills/market-consensus-radar/SKILL.md
    skills/market-consensus-radar/SCORING.md
    config/consensus/lithium_carbonate.yaml
    schemas/consensus_observation.schema.json
    schemas/daily_consensus_report.schema.json

Score an already collected/classified observation file:

    crf consensus-score observations.json

Use an explicit historical cutoff to make a run reproducible:

    crf consensus-score observations.json --now 2026-09-18T16:00:00+08:00

The scorer returns Institution/KOL/Crowd scores, an overall 0-100 consensus score,
a direction-agnostic crowding score, and raw/unique/effective sample sizes.

V0.1 deliberately separates scoring from collection. The existing fixed routing remains:

    TrendRadar -> Agent-Reach -> MediaCrawler -> Consensus classification/scoring

Historical scores must be append-only and must not be relabeled with hindsight.
