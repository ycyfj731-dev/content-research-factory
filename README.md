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

    skills/markets/market-consensus-radar/SKILL.md
    skills/markets/market-consensus-radar/SCORING.md
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


### Web-wide LC collection

Preview the deterministic daily query plan:

    crf consensus-plan

Add same-day dynamic terms without changing the core baseline:

    crf consensus-plan --dynamic-term 枧下窝复产 --dynamic-term 宁德时代

Run the web-wide collector and append raw evidence:

    crf consensus-collect

Smoke-test only the first few queries:

    crf consensus-collect --max-queries 3 --comments-limit 10

Default raw ledger:

    outputs/consensus/raw/lithium_carbonate.jsonl

The collection architecture is **web-wide first**. The fixed panel is a calibration
anchor, not the market universe.

Daily scoring stores both:

- Raw Consensus: exact-deduped captured stream before semantic/concentration controls
- Normalized Consensus: semantic-repeat discounted, platform/author/post capped,
  then Institution/KOL/Crowd balanced

Never compare daily scores without checking platform coverage and effective sample size.


### Process raw LC evidence into observations and narratives

After collection:

    crf consensus-process outputs/consensus/raw/lithium_carbonate.jsonl

Default outputs:

    outputs/consensus/processed/lithium_carbonate.observations.json
    outputs/consensus/processed/lithium_carbonate.observations.narratives.json

Then score the processed observations:

    crf consensus-score outputs/consensus/processed/lithium_carbonate.observations.json

Current classification mode is a conservative, deterministic LC baseline. It keeps
factual news neutral unless a directional view is explicit, distinguishes quoted and
conditional views, preserves explicit long/short disclosures, and neutralizes ambiguous
sarcasm.

Narrative clustering is auditable in V0.1: seeded LC narratives plus character-ngram
similarity. Repeated narratives receive lower uniqueness weight before Normalized
Consensus is calculated.


## Market Consensus Radar V0.2 source expansion

Optional source expansion is enabled only when configured. V0.1 remains the default.

Install source adapters:

    pip install -e ".[sources]"

Install multilingual semantic/topic analysis:

    pip install -e ".[semantic]"

Or everything:

    pip install -e ".[full]"

Optional environment switches:

    CRF_ENABLE_CRAWL4AI=true
    TRENDSCOPE_URL=http://127.0.0.1:8000
    TRENDSCOPE_API_KEY=...
    REDDITAPIS_KEY=...
    TIKHUB_API_KEY=...

When enabled, `crf consensus-collect` supplements the existing
TrendRadar -> Agent-Reach -> MediaCrawler route with:

- Crawl4AI: public web page enrichment
- TrendScope: international trend intelligence
- Reddit MCP: Reddit posts and deep comment search
- TikHub: Douyin / Xiaohongshu / Weibo fallback search

Every collection writes a coverage ledger beside the raw JSONL. A provider failure
is recorded as `partial` or `failed` and does not abort the entire daily run.

Semantic narrative clustering is opt-in:

    crf consensus-process RAW.jsonl \
      --semantic-model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

BERTopic can be added as a discovery-only layer:

    crf consensus-process RAW.jsonl --bertopic

The semantic/topic layer may group and discover narratives, but it does not directly
assign bullish/bearish stance.


## Skill layout

Concrete skills are isolated by domain. The root `SKILL.md` is routing-only and must not duplicate detailed skill rules.

```text
skills/
├── content/
│   ├── complex-to-clear/
│   └── editorial-visual-system/
└── markets/
    ├── market-consensus-radar/
    │   ├── SKILL.md
    │   └── references/
    └── football-betting/
        ├── SKILL.md
        ├── scripts/
        ├── tests/
        └── references/
```

TrendRadar, Agent-Reach, MediaCrawler and MoneyPrinterTurbo remain shared runtime adapters under `src/content_research_factory/adapters/`; they are not presented as standalone skills until they have independent skill contracts.
