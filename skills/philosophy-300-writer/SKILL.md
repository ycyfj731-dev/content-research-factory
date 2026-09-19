---
name: philosophy-300-writer
description: Produce source-grounded, zero-baseline philosophy lessons for the Philosophy 300 course while preserving frozen canonical cores, approved prose, source boundaries, and surgical revision discipline.
version: 0.1.0
---

# PHILOSOPHY-300-WRITER v0.1

## Purpose

This is the course-level controller for **《西方哲学，从0开始》 / Philosophy 300**.

It does not replace `skills/complex-to-clear/SKILL.md`.
It orchestrates that skill with source discipline, canonical-core protection, editorial writing rules, lesson closure, source selection, and freeze control.

Core principle:

> Lower the comprehension barrier, not the truth standard.

Second principle:

> A lesson should feel clear because the thinking is clear, not because the history was simplified into a myth.

Third principle:

> Approved material is an asset. Local feedback triggers local repair.

---

# AUTHORITATIVE INPUTS

Before drafting a lesson, check the relevant frozen course artifacts.

Required course sources:
- `docs/philosophy-300/CANONICAL_CORES_001_030_v1.0.md` for lectures 001–030.
- `docs/philosophy-300/SOURCE_SCREEN_001_010.md`
- `docs/philosophy-300/SOURCE_SCREEN_011_030.md`
- `skills/complex-to-clear/SKILL.md`

If a later version exists, use the latest explicitly frozen version rather than silently merging versions.

A frozen canonical core outranks stylistic preference.

---

# PRODUCTION PIPELINE

```
Lesson Question
→ Source Check
→ Source Layer Classification
→ Canonical Core
→ Zero-Baseline Bottleneck
→ Minimum Sufficient Model
→ Draft
→ Editorial Writing Gate
→ Distortion Gate
→ Lesson Closure
→ Next-Lesson Hook
→ Sources Selection
→ Freeze / Surgical Revision
```

Do not skip directly from “topic” to prose.

---

# SOURCE LAYERS

Every substantive claim must be tagged internally as one of:

- SOURCE CLAIM
- LATER TESTIMONY
- SCHOLARLY RECONSTRUCTION
- HISTORIOGRAPHICAL FRAME
- COURSE BRIDGE
- CONTESTED INTERPRETATION

Never blur these layers.

Examples:
- Aristotle reporting Thales ≠ direct quotation from Thales.
- Plato presenting Socrates ≠ automatic access to the historical Socrates.
- A modern reconstruction ≠ an ancient thinker’s stated motive.
- A course bridge may be pedagogically useful but must not be attributed to the historical thinker.

---

# LESSON CONTRACT

Each lesson must answer one central question.

Before writing, record:

1. **Question** — what exact problem is this lesson solving?
2. **Canonical explanation** — what must the reader understand by the end?
3. **Evidence anchor** — what source or source layer supports it?
4. **Must not say** — what tempting but false simplification must be blocked?
5. **Stop point** — what belongs to a later lesson and must not be stolen?
6. **Beginner bottleneck** — what will a true beginner fail to understand if left unexplained?

If any of these are unknown, do not draft final prose.

---

# ZERO-BASELINE RULE

The reader is assumed to know **nothing** about the textbook story of philosophy.

Begin from:
- ordinary experience;
- familiar language;
- directly observable situations;
- concepts already established in earlier lessons.

Do not begin from:
- unexplained schools;
- unexplained philosophers;
- period labels;
- specialist vocabulary;
- textbook slogans;
- contested narratives presented as background fact.

If a formal term is needed:

```
ordinary-language problem
→ concrete meaning
→ mechanism / relation
→ term reveal
```

Never use an abstract term to explain another abstract term.

---

# ANTI-AI PROSE — HARD GATE

Before public delivery, apply:
`references/ANTI_AI_PROSE_GATE.md`

The goal is not to add personality or imitate a writer. Remove model habits:
- repetition;
- empty transitions;
- fake dramatic rhythm;
- generic profundity;
- over-signposting;
- abstract noun inflation;
- forced symmetry;
- unearned “golden sentences”.

Delete before rewriting whenever possible.

---

# CHINESE NATIVE PROSE — FROZEN

Before finalizing any public lesson, apply:
`references/CHINESE_NATIVE_PROSE_GATE.md`

Use English-language philosophy writers only for reasoning structure, source caution, and explanatory sequencing. Do not translate their syntax into Chinese.

For Chinese prose, apply the frozen **Chinese Prose Core** in `references/CHINESE_NATIVE_PROSE_GATE.md`:

> 自然中文第一。清楚优先于漂亮，准确优先于气势。

Capability references only:
- 王小波：直接、清楚、少废话；
- 陈嘉映：概念精确；
- 葛兆光：史料边界与历史语境；
- 刘擎、梁文道：通识可读性与自然讲述；
- 许知远：仅参考节奏与停顿；
- 杨照：仅参考背景组织。

Never imitate any living writer's distinctive voice, phrasing, rhythm, signature metaphors, or verbal tics.

Hard deletion rule:

> **一段话如果删掉以后信息没有减少，就删掉。**

Preferred logical order when appropriate:

```
fact
→ question
→ explanation
```

Do not repeat the same question before and after the evidence. Do not use abstract summary phrases such as “整理前人” when a concrete action can be stated instead.

---

# WRITING STYLE — FROZEN

These are hard editorial rules for this course.

## W01 — Judgment first

State the actual point before commentary around it.

Avoid delayed-answer writing when the answer can be stated directly.

## W02 — One sentence, one move

A sentence should normally perform one intellectual action.

Do not pack:
- claim;
- qualification;
- historical background;
- metaphor;
- conclusion

into one sentence.

## W03 — Every paragraph advances

A paragraph must add:
- a new fact;
- a new distinction;
- a new example;
- a new consequence;
- or a necessary boundary.

If it merely restates the previous paragraph more elegantly, delete it.

## W04 — Do not circle the conclusion

Once a conclusion lands, do not repeat it in three formulations.

No:
- conclusion;
- paraphrased conclusion;
- dramatic one-line conclusion;
- summary of the same conclusion.

## W05 — No AI prose

Reject:
- generic scene-setting;
- “答案其实没有那么神秘”;
- “真正重要的是……” used repeatedly;
- empty dramatic fragments;
- fake profundity;
- motivational wrap-up;
- over-produced transitions;
- abstract editorial filler.

The prose should sound written because there was something precise to say.

## W06 — No rhetorical-question chains

Questions are allowed when they genuinely carry the argument.

Do not manufacture momentum by stacking question after question.

## W07 — No performance of thinking

Do not narrate the writer’s process:
- “我们不妨先想一想”
- “仔细看就会发现”
- “事情开始变得有趣”
- “这里有一个关键点”

unless the sentence actually contributes information.

## W08 — Avoid unexplained abstraction

Phrases such as:
- “一种新的探究方式”
- “自然内部的秩序”
- “更深层的原则”
- “重新组织问题”

must be made concrete before use.

A beginner should be able to retell the sentence in ordinary language.

## W09 — Concrete before technical

For example, prefer:

> 这些看起来完全不同的东西，会不会其实来自同一种更基本的东西？

before introducing a term like “principle”.

## W10 — Do not steal later lessons

Respect the frozen stop point.

A lesson may create curiosity about the next problem, but may not solve it early.

---

# HISTORICAL DISCIPLINE

## H1 — No myth-to-reason fairy tale

Do not say philosophy suddenly replaced myth, religion, or gods.

Continuity, overlap, and mixed explanatory practices must be preserved where relevant.

## H2 — No “first” without qualification

Labels such as:
- first philosopher;
- first scientist;
- founder of X

must be treated as retrospective historiographical labels unless unusually well established.

## H3 — No motive invention

Do not write:
> “X chose this because…”

when the evidence only shows what X was reported to have said.

Separate:
- attested claim;
- ancient explanation;
- modern reconstruction.

## H4 — No later vocabulary as ancient self-description

If Aristotle uses later conceptual language to classify an earlier thinker, say so.

Do not silently turn Aristotle’s vocabulary into Thales’ own vocabulary.

## H5 — Contested interpretations stay contested

Do not hide real scholarly disagreement for cleaner storytelling.

The lesson can remain simple while marking:
- what is secure;
- what is inferred;
- what is disputed.

---

# EDITORIAL BOUNDARY RULES

## B01 — Background only when necessary

Interesting background is not automatically useful.

If removing a background fact does not hurt understanding of the current question, move it elsewhere.

## B02 — Comparison is optional

Cross-cultural parallels are never mandatory.

If used, preserve:
- chronology;
- precise similarity;
- difference;
- transmission status.

Never write “Chinese version of X” or “they were saying the same thing” without evidence.

## B03 — Metaphor must pay rent

A metaphor is allowed only if it reduces the beginner bottleneck.

After the metaphor, explain the real structure.

If the metaphor is more memorable than the concept, it failed.

---

# LESSON CLOSURE

Every lesson must reach pedagogical closure.

By the end the reader must know:
- what was asked;
- what was established;
- what remains uncertain;
- why the lesson can stop here.

Do not end with a cliffhanger before the current question is complete.

A next-lesson hook, if used, comes **after** closure and clearly opens a new question.

---

# SOURCES POLICY

The public Sources page should normally contain **3–5 sources only**.

Select sources that materially support the published lesson.

Priority:
1. primary text / surviving fragment / direct ancient evidence;
2. strong ancient testimony when primary text is absent;
3. current authoritative reference work;
4. major scholarly book/chapter when needed.

Do not list every source consulted.

Do not use an obsolete archived reference page when a current official entry is available, unless version history is itself relevant.

Distinguish:
- current edition date;
- substantive revision date.

Sources should support the actual published claims, not merely the general topic.

---

# PRESERVE APPROVED MATERIAL — HARD RULE

Once the user explicitly approves:
- a paragraph;
- sentence;
- analogy;
- section;
- order;
- hook;
- conclusion;

freeze it by default.

Local feedback means surgical revision.

Examples:
- “这句绕” → fix that sentence.
- “这段不清楚” → fix that paragraph.
- “第二部分重复” → fix that section.

Do not rewrite the entire article to make it feel stylistically uniform.

Full rewrite is allowed only if:
- the canonical core changed;
- the central question is wrong;
- the structure fails;
- local repair would create contradiction.

Before a full rewrite, identify the structural reason internally.

---

# ANTI-REPETITION GATE

Before finalizing, mark every paragraph with its job.

If two adjacent paragraphs have the same job, merge or delete one.

Check specifically for repeated claims about:
- why the thinker matters;
- why the answer is unusual;
- why later people continued the question;
- why the historical label is retrospective;
- why myth and reason overlap;
- why uncertainty matters.

These are common course themes and must not be re-explained in full every lesson.

---

# DISTORTION GATE

Use the full gate in `skills/complex-to-clear/SKILL.md`.

For Philosophy 300, publication additionally requires:

- canonical core preserved;
- source layer preserved;
- no invented motive;
- no fake quote;
- no later vocabulary silently back-projected;
- no contested interpretation presented as settled;
- stop point respected;
- beginner bottleneck solved;
- approved material preserved;
- current lesson closed before hook.

Allowed status:
- READY
- REWRITE
- NEEDS_SOURCE
- NEEDS_EXPERT_CHECK

No failed hard rule may be published with a caveat.

---

# WORKING OUTPUT FORMAT

For each new lesson, create internally:

```
LESSON:
QUESTION:
TYPE:
CANONICAL CORE:
SOURCE LAYERS:
EVIDENCE:
MUST NOT SAY:
STOP POINT:
BEGINNER BOTTLENECK:
APPROVED/FROZEN PASSAGES:
DRAFT STATUS:
```

Then draft the lesson.

Do not expose this scaffold to the public article unless useful.

---

# FREEZE RULE

When a lesson is approved:
1. freeze the exact approved prose;
2. freeze its source list;
3. record the canonical core version;
4. record any approved wording that must survive later edits;
5. later changes use version increments when they alter meaning, source framing, or structure.

Visual production is downstream and may not rewrite frozen prose unless explicitly authorized.
