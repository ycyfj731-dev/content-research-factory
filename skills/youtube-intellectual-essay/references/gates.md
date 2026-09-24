# Topic, Evidence and Anti-Slop gates

Record each check's result, artifact/version inspected, reason, evidence location and required repair. `PASS` requires completed checks; a known defect is `REVISE`; missing essential evidence or capability is `BLOCKED`; unperformed checks are `NOT_RUN`. No aggregate score overrides a hard failure. Gate reports are editorial judgments, not automated truth or virality detectors.

## 01 Topic Gate

Write the everyday tension, one central question, intended viewer, provisional answer, counterargument, two concrete examples, fresh angle and feasible visual treatment. State why the topic needs 10–15 minutes rather than stretching a short explanation.

Score each dimension 0–4. Use 0 for a demonstrated absence, 1 for weak, 2 for workable with a named gap, 3 for strong and 4 for unusually strong. Unknown is `UNKNOWN`, not a number. Every score needs a brief reason and observed input or explicitly labeled editorial judgment.

| Dimension | What earns a high score |
|---|---|
| Personal tension | A recognizable decision, contradiction or social pressure with a concrete example |
| Question and curiosity | A clear question whose answer changes understanding without a false promise |
| Explanatory depth | A coherent mechanism plus boundary/counterexample can sustain the duration |
| Evidence feasibility | Inspectable primary work/research exists for the central explanation |
| Distinct contribution | A specific gap or angle grounded in actual competitor observations |
| Visual feasibility | The mechanism can be shown through obtainable evidence and original graphics |

Decision defaults (local editorial heuristics, not YouTube benchmarks):

- `PASS`: at least 18/24, no dimension below 2, no UNKNOWN, no hard failure.
- `REVISE`: a complete scorecard fails those thresholds or the topic/packaging has a repairable flaw. Narrow, reframe or archive the idea and state why.
- `BLOCKED`: any essential dimension remains UNKNOWN. Permit targeted research and provisional packaging, but do not claim validated demand or proceed into expensive production.

Hard failures: invented demand data; a hook dependent on a false factual premise; diagnosis or universal human claims without appropriate support; no plausible source route for the core argument; a production plan that requires unavailable/uncleared assets without a feasible substitute. Popularity cannot compensate for an evidence failure.

Stage 01 can be provisional. Refresh evidence feasibility after Stage 03 and distinct contribution after Stage 02, then issue the final Topic decision before full scripting. If research access is unavailable, deliver a research-ready candidate with the unanswered checks rather than a false PASS. Never promise CTR, retention, views or revenue from a score.

## 06 Evidence Gate

1. Extract substantive claims from narration, on-screen text, graphics, hooks, titles and thumbnails. Include statistics, history, causal explanations, attributed theories and direct quotes. A rhetorical question with a presupposition is still a claim.
2. Assign claim IDs and types: `textual`, `empirical`, `interpretation`, `modern-application`, `illustrative` or `opinion`. A sentence may need splitting when it mixes types.
3. For every textual/empirical claim, inspect the underlying source and record an exact locator and what it supports. A bibliography, search snippet, abstract or DOI alone does not establish a detailed result. Record access limitations. An abstract can support only what it explicitly reports.
4. For philosophy, preserve author/speaker, work, edition/translation, passage context, theory versus observation and interpretive limits. For empirical work, preserve design, population, measured outcome, limitations and what causal inference is justified. Check relevant corrections, retractions or conflicting evidence when material.
5. Verify each quoted word against the actual passage and record translation details. Otherwise paraphrase without quotation marks. Do not invent page numbers. Keep the original exact wording in the internal ledger only to the extent needed for verification.
6. Distinguish the original theory, our interpretation, and a present-day application. Similarity between a study and a philosopher's framework is not proof of the entire framework. A mock scenario illustrates; it does not demonstrate prevalence.
7. Freeze a short explanation core: what is supported, attribution, strength, scope, boundary and what remains unresolved. Check all later simplifications against it.

Claim decisions:

| Status | Meaning | Required action |
|---|---|---|
| `PASS` | Inspected support fits the exact wording and scope; interpretation/illustration is visibly identified | Retain with the source mapping |
| `REVISE` | Overclaim, misattribution, false precision, unverifiable quote or omitted material limitation | Narrow, correct or remove; inspect the revised line again |
| `BLOCKED` | Necessary source/passage is inaccessible or contradictory evidence remains unresolved | Seek accessible support or replace/remove the claim |

Illustrations/opinions can PASS without empirical citations only when labeled and carrying no hidden factual premise. Interpretations and modern applications must identify their source framework and make the inferential step explicit. Direct quotes, precise numbers and causal conclusions require direct support; adding “may” does not repair absent evidence automatically.

Gate PASS requires 100% of retained substantive claims checked and passed, including title/thumbnail claims. Record removed claims and their dependent lines so they cannot silently return. One unresolved central claim blocks final script approval; an optional unsupported claim may be removed and the remaining packet re-reviewed. Recheck the final cut for new text or implied claims.

## Anti-Slop Gate (Stages 07, 10 and 13)

The question is whether the viewer learns something from the images beyond hearing the narration. Mixing media categories alone does not establish quality.

Hard checks:

- **Semantic purpose:** every shot has a named purpose: evidence, mechanism, comparison, context, orientation or an intentional reflective pause. Generic “mood/B-roll” without a relationship to the beat needs repair.
- **Explanatory sequences:** include at least two sequences that build understanding visually, such as a relationship diagram and an annotated document or controlled comparison. Specify the information revealed, not merely zooms/transitions.
- **No sentence-to-image treadmill:** fail a plan or cut dominated by interchangeable AI stills, stock clips or quote cards, including a still per sentence with pans/crossfades. Cosmetic motion and alternating categories do not repair this.
- **Evidence honesty:** generated historical scenes, philosopher portraits, social posts and interface mockups cannot masquerade as documentary evidence. Label reconstructions/illustrations where confusion is plausible. Charts need source data, units and honest scales; schematic diagrams must be visibly non-statistical.
- **Readable and intentional:** key text/diagrams survive small-screen inspection, qualifiers stay visible with the claims, and shot lengths permit comprehension. Repeated templates must serve recurring meaning, not fill time.

V0.1 planning defaults: at least three primary visual families across a full episode, and no more than 20% AI-generated imagery/video by visible timeline duration. These are house-style heuristics, not platform rules or proof of originality. A user-requested exception needs a recorded editorial reason and the same hard checks; it cannot bypass misleading evidence or an AI slideshow failure.

Compute proportions from non-overlapping timeline intervals. Count the union of all time where AI imagery/video is visible, including overlays; typography placed over an AI background does not hide AI time. Count each second only once in the AI numerator. For primary-family distribution, give each interval one dominant family: archive/document, licensed B-roll, screenshot, diagram/chart, typography or AI. Caption overlays are not an extra family. Do not count hypothetical assets as acquired or reviewed.

Inspect beginning, middle, ending and all evidence-heavy sequences; a full watch is required at Final QA. Run the swap test: if unrelated generic footage could replace a sequence without losing information, revise its visual reasoning or record why a brief deliberate pause is justified. A long-held primary document may be excellent; a mandated cut every few seconds is not a substitute for judgment.

Report separate `planned` and `rendered` gate results. Missing rendered media means rendered review `NOT_RUN`, never PASS. A plan with 10% AI can still fail; one with strong evidence graphics still fails if it presents synthetic footage as real.
