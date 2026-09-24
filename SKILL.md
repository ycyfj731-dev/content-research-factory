---
name: content-research-factory
description: Route requests to independent skills and shared research infrastructure. Concrete skill rules live only inside their own skill directories.
---

# CONTENT-RESEARCH-FACTORY Router

This file is a lightweight router. It must not duplicate detailed rules from individual skills.

## Skill registry

### Content
- `skills/youtube-intellectual-essay/SKILL.md` — English faceless intellectual video essays; topic, evidence and visual-quality gates.
- `skills/content/complex-to-clear/SKILL.md` — turn complex material into clear, readable content.
- `skills/content/editorial-visual-system/SKILL.md` — editorial visual and publishing system.

### Markets
- `skills/markets/market-consensus-radar/SKILL.md` — financial-market consensus research and scoring.
- `skills/markets/football-betting/SKILL.md` — football 7-leg ticket research, optimization and validation.

## Shared research infrastructure

TrendRadar, Agent-Reach, MediaCrawler and MoneyPrinterTurbo are currently shared runtime adapters, not standalone skills:

- TrendRadar = 热点发现
- Agent-Reach = 跨平台验证
- MediaCrawler = 中文社媒深抓和评论
- MoneyPrinterTurbo = 视频生产

Their implementation remains under `src/content_research_factory/adapters/` and their routing contract remains in `config/routing.yaml`.

Do not invent a standalone skill directory for an adapter unless it gains its own invocation contract, rules and tests.

## Isolation rule

When working on one skill, read and modify that skill's directory first. Do not copy its detailed rules into another skill or into this router.

Long references belong in `references/`, executable helpers in `scripts/`, tests in `tests/`, and historical material in `archive/` or a clearly named reference file.
