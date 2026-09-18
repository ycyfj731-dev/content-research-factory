---
name: content-research-factory
description: Orchestrate topic discovery, cross-platform verification, Chinese social-media deep research, comments analysis, and video-production handoff.
---

# CONTENT-RESEARCH-FACTORY

## Purpose

Turn a content-research request into a traceable research package and, when requested, a production handoff.

## Fixed tool routing

The routing below is mandatory:

- **TrendRadar** = 热点发现
- **Agent-Reach** = 跨平台验证
- **MediaCrawler** = 中文社媒深抓和评论
- **MoneyPrinterTurbo** = 视频生产

Do not reassign these responsibilities without an explicit repository-level change.

## Default execution order

```text
TrendRadar
  -> Agent-Reach
  -> MediaCrawler
  -> evidence synthesis
  -> MoneyPrinterTurbo
```

A stage may be skipped only when the user request clearly does not require it.

## Research contract

Every research item should preserve, when available:

- query/topic
- platform
- source URL or source identifier
- author/account
- title/text
- published timestamp
- engagement signals
- comments
- retrieval timestamp
- originating tool
- verification status

## Evidence rules

1. Discovery is not verification.
2. A cross-platform mention is not automatically an independent source.
3. MediaCrawler is the deep-retrieval layer for Chinese social platforms and comments.
4. Keep raw source identity so later synthesis can trace claims back to evidence.
5. Separate observed source content from model inference.
6. Do not hand a topic to video production until the research package is explicit enough to support a script.

## MediaCrawler adapter contract

The adapter must expose normalized operations for:

- search
- detail/deep fetch
- comments

It may translate these operations into the concrete MediaCrawler MCP method names configured for the environment.

## Output boundary

The research layer should produce structured evidence first. Creative packaging and video generation belong downstream.
