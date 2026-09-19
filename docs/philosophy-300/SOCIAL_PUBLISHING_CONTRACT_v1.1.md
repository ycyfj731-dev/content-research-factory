# Philosophy 300 — Social Publishing Contract v1.1

Status: **FROZEN**

## Core rule

> **完整正文就是小红书正文；小红书只做分页和视觉编辑，不再额外降密度。**

The frozen lesson prose is the source of truth. The carousel is a layout of that prose, not an independent simplified rewrite.

## Regular page budget

- Normal target: **8–10 pages**.
- Regular maximum: **10 pages** unless a lesson has an explicit approved exception.
- When content is dense, first merge adjacent cognitive actions and improve page utilization.
- Do not delete knowledge merely to hit the page limit.

## One page, one cognitive action

A page may:
- introduce a thinker or setting;
- explain a term;
- present evidence;
- distinguish ancient source from later interpretation;
- answer one part of the central question;
- close the current lesson;
- introduce the next lesson after closure.

Adjacent actions may share one page when they are naturally connected.

## Internal lesson-value checks are not public modules

KNOW / CORRECT / TOOL / PERSON / LIKE / SAVE / FOLLOW are **backstage acceptance dimensions**.

They do **not** require public sections named:
- 阅读工具
- 本讲总结
- 你学会了什么
- 为什么值得收藏

A reusable tool should normally emerge naturally from the lesson. Do not create a standalone “tool page” unless the content itself genuinely requires one.

## Fixed publication chrome

Every standard carousel page uses:
- top left: `PHILOSOPHY 300`
- top right: lesson progress, e.g. `002 / 300`
- bottom left: `《西方哲学，从0开始》 · @每天读一点哲学`
- bottom right: lesson progress + page number.

## Section marker

Standard content pages use a two-digit section marker:
- `01`
- `02`
- `03`

The number uses the page accent color; the section name is black.
Do not use Chinese numeral kickers such as “一 · 泰勒斯是谁”.

## Sources and internal metadata

The public Sources page contains sources the lesson actually depends on.

Do not show readers:
- internal frozen-version labels;
- engineering filenames;
- QA filenames;
- internal repository paths;
- build metadata.

Those remain in the repository.

## Relationship to frozen prose

A published deck may change:
- page breaks;
- hierarchy;
- typography;
- evidence placement;
- source-page presentation.

It may not silently change:
- historical claims;
- terminology;
- source boundaries;
- approved prose meaning;
- lesson closure.

If the prose changes, create a new frozen prose version first, then regenerate the deck.
