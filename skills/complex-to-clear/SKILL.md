---
name: complex-to-clear
description: Explain complex knowledge clearly without flattening, distorting, misattributing, or over-simplifying the source material. Use for educational content, scripts, courses, explainers, and beginner-facing knowledge translation.
---

# COMPLEX-TO-CLEAR v1.0

## Purpose

Turn difficult knowledge into beginner-comprehensible explanations **without reducing intellectual depth or source fidelity**.

Core principle:

> Lower the comprehension barrier, not the truth standard.

## Default explanation pipeline

```text
Known
  -> Bottleneck
  -> Minimum Sufficient Model
  -> Bridge / Metaphor
  -> Mechanism
  -> Term Reveal
  -> Misconception Check
  -> Counterexample / Boundary
  -> Retell Test
```

### Stage definitions

- **Known**: begin from something the intended reader already understands.
- **Bottleneck**: identify the exact conceptual obstacle preventing understanding.
- **Minimum Sufficient Model**: explain only the smallest model needed to cross that obstacle.
- **Bridge / Metaphor**: use a familiar analogy only when it preserves the source structure.
- **Mechanism**: state what is actually happening underneath the analogy.
- **Term Reveal**: introduce formal terminology only after the concept is understood.
- **Misconception Check**: state the most likely wrong interpretation.
- **Counterexample / Boundary**: show where the simplified model stops working.
- **Retell Test**: verify that a beginner can restate the idea without repeating jargon.

## Constitutional rule

**Propagation value never outranks truthfulness; accuracy never excuses avoidable obscurity.**

A catchy explanation that changes the claim is a failure.
An accurate explanation that merely repeats expert jargon is also a failure.

# HARD RULES

These rules are mandatory. Any FAIL blocks publication and returns the item to rewriting.

## H01 — Source Anchor

Every substantive explanation must be anchored to the best available source layer for the domain.

For philosophy and historical thought:
- identify the primary text when available;
- identify work / section / passage context;
- identify who is speaking when dialogue or reported speech is involved.

For other domains:
- identify the authoritative paper, law, standard, dataset, technical documentation, or first-party source when reasonably available.

Do not build the explanation solely from tertiary summaries when a stronger source is available.

## H02 — Attribution Integrity

Never collapse:
- author vs character;
- researcher vs hypothesis;
- court vs party argument;
- source claim vs commentator interpretation;
- model inference vs observed evidence.

If the source contains competing voices, preserve the distinction.

## H03 — No Fake Quotes

Do not fabricate quotations, aphorisms, or "famous sayings."

If wording is a paraphrase, label it as a paraphrase or write it in indirect speech.

A concise viral sentence must never be presented as a direct quote unless verified.

## H04 — Analogy Fidelity

An analogy may simplify access, but may not replace the original problem.

Run this test:

> If the analogy is removed, is the remaining claim still the source author's actual claim or problem?

If no, FAIL.

## H05 — No Historical or Disciplinary Backflow

Do not smuggle later concepts backward into earlier thinkers or domains.

Examples:
- do not explain Plato as if he used Kantian categories;
- do not describe an ancient argument as if it were modern neuroscience;
- do not turn a legal doctrine into a psychology claim;
- do not turn a statistical correlation into a causal mechanism.

Modern comparison is allowed only when explicitly marked as a later analogy or application.

## H06 — One Core Question per Unit

One lesson, segment, or short-form explainer must have one central conceptual question.

Supporting concepts may appear only if they serve that question.

Do not create the illusion of understanding by stacking multiple major theories in one unit.

## H07 — Term Reveal After Understanding

Do not use specialist terminology as the explanation.

Default order:

```text
problem -> intuition -> mechanism -> formal term
```

Not:

```text
formal term -> definition full of more formal terms
```

## H08 — Metaphor Is Not the Model

Every metaphor must be followed by a mechanism-level explanation.

The reader must be able to answer:

> What does each important part of the metaphor correspond to in the real concept?

If the reader only remembers the image but not the idea, FAIL.

## H09 — Boundary / Counterexample Required

Every simplified model must state at least one of:
- what it does not mean;
- where it stops applying;
- a counterexample;
- a common overextension.

This prevents "easy to remember" from becoming "wrong but sticky."

## H10 — Contested Interpretations Stay Contested

When qualified experts materially disagree, do not present one interpretation as uncontested fact.

The explanation does not need to reproduce the whole literature.

It must at least distinguish:
- well-established textual / empirical facts;
- dominant interpretation;
- important alternative interpretation;
- unresolved uncertainty.

## H11 — Modern Application Must Be Layered

Separate:

```text
SOURCE CLAIM
INTERPRETATION
MODERN APPLICATION
```

Never imply that an ancient thinker predicted social media, AI, capitalism, neuroscience, or another later phenomenon unless the historical evidence truly supports that claim.

## H12 — Dual Comprehension Test

A finished explanation must pass both:

### Beginner Test
A reader with no specialist training can restate the core idea in ordinary language.

### Distortion Test
A domain expert would recognize the explanation as simplified but not substantively changed.

Passing only one is a FAIL.

## H13 — Do Not Close the Problem Too Early

Do not force every lesson into:
- "therefore X was right";
- "the lesson is...";
- "what this teaches us is...";
- a motivational takeaway.

When the intellectual value lies in the unresolved problem, preserve the tension.

The reader should sometimes leave with a sharper question rather than a packaged answer.


## H14 — Explanation Consistency

Once a source passage has passed the DISTORTION GATE, freeze a **canonical explanation core** before any style rewrite.

The canonical core must record:
- what the passage is doing;
- what problem or claim it introduces;
- who is making that move;
- whether the passage asks a question, advances an argument, gives an answer, or sets up a later answer;
- what it does **not** yet establish;
- any essential boundary or unresolved issue.

All later versions — short, long, literary, conversational, video, article, child-friendly, or expert-facing — may change:
- wording;
- examples;
- rhythm;
- order of exposition;
- level of detail.

They may **not** change the canonical explanation core.

Run this comparison:

> Would a reader of Version A and Version B come away believing the source passage is doing the same philosophical / conceptual job?

If no, FAIL.

A style rewrite must never silently:
- turn a question into an answer;
- turn a character's challenge into the author's conclusion;
- import a later conclusion into an earlier passage;
- narrow or widen the claim;
- change the stated reason why the passage matters.

If a better reading of the source is discovered, update the canonical core explicitly, record the reason, and rerun the gate. Do not let explanation drift happen through copyediting.

# DISTORTION GATE

Run before any content enters final scripting or publication.

Required checks:

1. **SOURCE_FIDELITY**
   - Is the central problem or claim genuinely supported by the source?

2. **ATTRIBUTION**
   - Is the claim assigned to the correct speaker, author, school, party, study, or institution?

3. **QUOTE_INTEGRITY**
   - Are all direct quotations verified?
   - Are paraphrases clearly paraphrases?

4. **ANALOGY_FIDELITY**
   - Does the analogy preserve the original conceptual structure?

5. **TEMPORAL_DISCIPLINARY_CONTAMINATION**
   - Has a later concept or different discipline been silently imported?

6. **CORE_QUESTION_DISCIPLINE**
   - Is there exactly one main conceptual question?

7. **TERM_ORDER**
   - Was the concept made understandable before jargon was introduced?

8. **METAPHOR_TO_MECHANISM**
   - Is the real mechanism explained after the metaphor?

9. **BOUNDARY_CHECK**
   - Is at least one misconception, limit, or counterexample included?

10. **CONTESTEDNESS**
   - Are serious disagreements or uncertainties represented accurately?

11. **APPLICATION_LAYERING**
   - Are source, interpretation, and modern application separated?

12. **BEGINNER_RETELL**
   - Can a beginner restate the idea without merely repeating jargon?

13. **EXPERT_DISTORTION**
   - Would a knowledgeable reader accept the simplification as faithful?

14. **PREMATURE_CLOSURE**
   - Has the explanation preserved an open problem when closure would be artificial?

15. **EXPLANATION_CONSISTENCY**
   - Does this version preserve the frozen canonical explanation core from the source-approved version?
   - Would readers of different style/length versions understand the passage as doing the same conceptual job?

Any hard FAIL returns the content to:
```text
Bottleneck -> Minimum Model -> Bridge -> Mechanism
```
for reconstruction.

# Output contract

A normal COMPLEX-TO-CLEAR output should contain, in this order:

1. **Hook / concrete situation**
2. **The hidden problem**
3. **Minimum sufficient model**
4. **Mechanism**
5. **Formal term**
6. **What this does NOT mean**
7. **Counterexample / boundary / competing reading**
8. **Retell sentence**
9. **Open question or next-step tension**

## Retell sentence requirement

The retell sentence must be understandable without specialist vocabulary.

Bad:
> Plato's epistemology depends on ontological participation in Forms.

Better:
> Plato is asking how we can recognize a stable standard when the things we see keep changing.

# Philosophy adapter

When this skill is used for philosophy, prepend:

```text
Question
  -> Primary Source
  -> Historical / Dialogical Context
  -> Claim
  -> Speaker Attribution
  -> Competing Interpretations
  -> COMPLEX-TO-CLEAR
  -> Hook
  -> Script
  -> Freeze Canonical Explanation Core
  -> DISTORTION GATE
```

Never begin from "What did philosopher X believe?" when a sharper source-grounded problem is available.

Prefer:
- a dilemma;
- a contradiction;
- a thought experiment;
- a concrete human conflict;
- a question whose answer changes how the theory becomes intelligible.

# Publication rule

No item may be marked READY if any DISTORTION GATE item is FAIL or UNKNOWN.

Allowed status values:

- `READY`
- `REWRITE`
- `NEEDS_SOURCE`
- `NEEDS_EXPERT_CHECK`

There is no "publish with caveat" bypass for a failed hard rule.
