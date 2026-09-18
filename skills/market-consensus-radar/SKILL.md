---
name: market-consensus-radar
description: Measure market consensus, crowding, narrative saturation, and consensus-vs-reality divergence from institutions, finance creators, and public comments.
---

# MARKET-CONSENSUS-RADAR

## Purpose

Build a daily, append-only, auditable time series of what the market believes.

The skill does **not** treat "many bullish comments" as a trading signal. It measures:

1. direction: bullish / bearish / neutral;
2. strength: weak vs strong stance;
3. horizon: intraday, 1-5d, 6-20d, 21-60d, longer;
4. conviction: how certain the author sounds;
5. position disclosure: opinion vs actually long/short;
6. narrative: why the author is bullish/bearish;
7. uniqueness: original view vs copied/repeated narrative;
8. source class: institution / KOL / crowd.

The output is designed for later event studies and backtests.

## Fixed upstream routing

Inherit the repository routing invariant:

- TrendRadar = topic / narrative discovery
- Agent-Reach = cross-platform verification
- MediaCrawler = Chinese social deep retrieval and comments
- MoneyPrinterTurbo = not used by this skill

Do not reassign these responsibilities.

## V0.1 asset

First production target: China lithium carbonate futures (GFEX LC).

Configuration:
`config/consensus/lithium_carbonate.yaml`

## Core rule: fixed panel + dynamic discovery

Daily collection has two lanes.

### A. Fixed panel

Track the same institutions, creators, and seed communities every day.

Goal: comparability through time.

### B. Dynamic discovery

Discover new narratives, viral posts, new creators, and event-driven keywords every day.

Goal: detect narrative regime change.

Never replace the fixed panel with dynamic search results.

## Source groups

Calculate three independent group scores before any combined score:

- Institution Consensus
- KOL Consensus
- Crowd Consensus

Do not allow a high-volume crowd sample to numerically overwhelm the institution group.

The overall score combines group-level scores, not raw observation counts.

## Observation contract

Every classified observation should preserve:

- source identity or stable hash;
- source group;
- platform;
- URL / source ID;
- published timestamp;
- retrieval timestamp;
- raw text or traceable source payload;
- direction in {-2,-1,0,+1,+2};
- horizon;
- classifier confidence;
- conviction;
- whether a position is explicitly disclosed;
- disclosed position;
- reason tags;
- target price if explicitly stated;
- narrative cluster IDs;
- uniqueness factor;
- source weight;
- raw hash.

Schema:
`schemas/consensus_observation.schema.json`

## Direction labels

- -2 = strong bearish
- -1 = bearish
- 0 = neutral / no directional view
- +1 = bullish
- +2 = strong bullish

Do not infer a position from general sentiment if the author did not state one.

Example:

"Supply will rise" is not automatically a short position.

"我已经加空，11万见" is both a strong bearish opinion and an explicit short disclosure.

## Opinion / position / conviction must stay separate

Three observations that must not be scored identically:

1. "感觉可能还会跌。"
2. "我明确看空未来两周。"
3. "已经加空，11万必破。"

The third may receive more effective weight because it includes explicit position disclosure and higher conviction, but the weighting must be deterministic and documented.

## Freshness / half-life

Old opinions decay.

Use horizon-aware half-lives from the asset config.

A one-day call should lose relevance much faster than a one-month thesis.

Never keep stale opinions fully active just because the post remains online.

## Deduplication

Do not count copies of the same information as independent evidence.

Required sequence:

1. exact/raw-hash dedup;
2. near-duplicate text detection;
3. semantic narrative clustering;
4. assign uniqueness_factor in [0,1].

A repost or template copy should carry much less incremental weight than an original independent analysis.

## Narrative engine

Each observation can belong to one or more narrative clusters, e.g.:

- Zimbabwe lithium supply recovery
- Jiangxi lepidolite restart
- warehouse receipt cancellation
- holiday restocking
- high social inventory
- squeeze / deliverable supply shortage

For every major narrative track:

- first_seen_at;
- unique_originators;
- unique_spreaders;
- adoption by Institution/KOL/Crowd;
- saturation score;
- direction contribution.

The key question is not only "what does the market believe?" but also "how mature is that belief?"

## Consensus scoring

Scoring implementation:
`src/content_research_factory/consensus/scoring.py`

Formula documentation:
`skills/market-consensus-radar/SCORING.md`

Scores:

- 0 = maximally bearish
- 50 = balanced / neutral
- 100 = maximally bullish

Always output sample sizes and effective sample sizes beside scores.

A score without coverage information is incomplete.

## Crowding

Crowding measures one-sided directional commitment, not bullishness.

High crowding can occur at either 10/100 consensus or 90/100 consensus.

Do not use crowding alone as a contrarian trading rule.

## Daily output

Daily report schema:
`schemas/daily_consensus_report.schema.json`

Minimum output:

- date / asset;
- platform coverage;
- institution / KOL / crowd scores;
- overall consensus score;
- crowding score;
- effective sample size;
- dominant narratives and saturation;
- data-quality warnings;
- optional market/fundamental snapshot;
- optional divergence state.

## Divergence

V0.1 may ingest externally supplied market/fundamental fields but must not fabricate them.

Examples for LC:

- futures price;
- spot price;
- basis;
- warehouse receipts and daily delta;
- social inventory and weekly delta;
- open interest;
- near/far spread;
- production;
- import / ore arrival data.

Potential states:

- BEARISH_CONSENSUS_BULLISH_REALITY
- BULLISH_CONSENSUS_BEARISH_REALITY
- CONSENSUS_CONFIRMED
- MIXED
- INSUFFICIENT_DATA

Divergence is a research state, not an automatic buy/sell instruction.

## Append-only research rule

Daily consensus records are immutable after the daily lock time.

Corrections must be written as a new version or correction event.

Never revise yesterday's score because today's price action makes the old classification look wrong.

This rule is mandatory for valid backtests.

## No hindsight contamination

Historical model evaluation must use:

- only content available by the historical cutoff;
- model/version metadata;
- the original locked observation set;
- the original scoring parameters.

Do not relabel historical views using future returns.

## V0.1 boundaries

Included:

- schema;
- deterministic scoring;
- lithium carbonate config;
- daily report contract;
- tests for scoring invariants.

Not yet included:

- production scheduler;
- platform login/session management;
- commercial data provider integration;
- embedding-based narrative clusterer;
- automated historical event study;
- execution/trading integration.
