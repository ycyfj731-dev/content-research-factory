# CONTENT-RESEARCH-FACTORY

A research-to-production pipeline for discovering, validating, deep-reading, and producing social content.

## Fixed routing

| Tool | Responsibility |
|---|---|
| TrendRadar | 热点发现 |
| Agent-Reach | 跨平台验证 |
| MediaCrawler | 中文社媒深抓和评论 |
| MoneyPrinterTurbo | 视频生产 |

This routing is a project invariant. Do not silently swap responsibilities between tools.

## Repository layout

```text
.
├── SKILL.md
├── README.md
├── config/
│   └── routing.yaml
├── src/
│   └── content_research_factory/
│       ├── __init__.py
│       ├── routing.py
│       └── adapters/
│           ├── __init__.py
│           └── mediacrawler_mcp.py
├── tests/
│   ├── test_routing.py
│   └── test_mediacrawler_adapter.py
└── pyproject.toml
```

## First-stage pipeline

1. TrendRadar discovers candidate topics.
2. Agent-Reach verifies the topic across platforms.
3. MediaCrawler performs deep Chinese-social retrieval, including posts and comments.
4. MoneyPrinterTurbo receives an approved research package for video production.

## Development

Requires Python 3.11+.

```bash
python -m pip install -e ".[test]"
pytest
```

## MediaCrawler adapter

The starter adapter intentionally isolates MediaCrawler behind a normalized interface. The rest of the factory should consume normalized research records instead of depending on MediaCrawler-specific payload shapes.

Configuration lives in `config/routing.yaml`.
