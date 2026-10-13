# Editorial Voice and Source-to-Script Contract
Version 0.2.1. Applies to every English essay script, article draft, AV handoff, citations and QA.

## Editorial identity
Publish accessible English explanatory journalism in the spirit of the **methods**, not imitation of the distinctive prose, of The Economist (argument), The New York Times (reported scenes and nuance), and Bloomberg (numbers, incentives and mechanisms). Audience: intelligent non-specialists with no prerequisite academic training. Investigate an observable question; do not write a literature review disguised as an essay. Evidence leads the argument, not vice versa. Never claim actual reporting/interviews that did not happen.

**Reader/listener contract**: one clear central question and earned conclusion; everyday scenes first, then verified evidence, then competing explanations, then implications. Every section must provide a *new finding*, counterexample, or change in understanding, not summarize a theme repeatedly. Prefer precise language over theoretical terminology. Explain jargon immediately with a concrete example; use named theorists only when they illuminate something. Separate on-camera or audio narration from on-screen citations. Draft as an essay if useful, then adapt for audio through aloud-reading and measured timing.

## Internet-native but mature English voice
- Sound like an educated writer who actually encounters internet culture: natural idioms, varied sentence lengths, discreet irony, occasional authentic online phrasing. One short ironic cluster at the opening may be effective; do not fill the script with meme references or Gen-Z slang.
- **Avoid repetitive fragment chains** such as "Your boss? Toxic. Your ex? Narcissist." More than one such cluster is a revision trigger.
- Remove AI-like scaffolding: repeated "But here's the thing", "And that raises an interesting question", "It's not X, it's Y", grand unearned epigrams, stock rhetorical triplets, every paragraph ending in a question, repeated summaries of the same lesson.
- Do not assume all viewers experience a phenomenon. Use authentic dated examples, published interviews and observational data when possible. Hypothetical scenes explicitly remain hypothetical. Never invent a composite as a real person.
- Humor must clarify a mechanism, not mock people with mental health conditions or substitute for argument. Do not confuse a specific diagnosis with a colloquial label. Preserve a fair counterargument even when a clear thesis emerges.
- **Auditory test**: aloud at actual pace; no long bibliography read-outs; no artificial 3–5-minute recap schedule, generic subscribe CTA, or mandatory self-help checklist. Distinctive natural transitions beat mechanical hooks.
- Fact, inference and hypothesis must be legible in the narration. Editorial restraint is not false equivalence.

## Source-to-Script Ledger — required artifacts
Outputs:
- `03-source-ledger.csv` or `03-source-ledger.md`: source_id,full_title,authors,publisher_or_journal,publication_date,doi_or_canonical_url,source_type,accessed_at,access_extent(full/abstract/reporting),precise_locator,source_limitations,rights_notes.
- `05-claim-script-ledger.csv` or `05-claim-script-ledger.md`: claim_id,exact_script_quote,claim_kind(fact/stat/quote/expert_opinion/theory/interpretation/hypothetical),source_ids,source_locator,what_source_actually_supports,limitations,decision(PASS/REVISE/BLOCKED),beat_id,onscreen_citation_id,description_reference_id.
- `12-references.md`: full bibliographic information + resolvable original URLs for video description; `07-av.md`: reference overlay timing where needed.

**Mandatory checks:**
1. Every checkable consequential fact, number, chronological claim, quotation, and attributed research result has a stable C-ID and traceable original source (when available). Source title/abstract alone cannot support unsupplied study results, effects, methods or quotes. Citation must point to exact supporting passage/table/figure/page/section.
2. For studies: identify participants/sample, design, date, measured outcomes and limitations, at least in ledger; speak only details that improve listener understanding. Preserve observational versus experimental distinction, correlation versus causation, and population limitations. Philosophical analyses are arguments, not experiments. No invented statistical significance or extrapolation from unrelated studies.
3. For reporting: link to original article and identify named actual interviewees and quotes accurately. Never invent quotes, interviews, viewing data or a real-world vignette. If using a secondhand description, cite that intermediary and label secondary access.
4. Every research-derived spoken fact is backed by the ledger; overlays use concise author/year/short title and a stable reference ID; full source goes to metadata. Do not vocalize entire article titles mechanically or paste URLs into spoken script.
5. An unattributed original conclusion must be labeled authorial interpretation, grounded in cited facts and bounded by credible counterarguments. Distinguish usage trends from dictionary *lookup* spikes, public views from hidden CTR, hypothetical user comments from observed comments.
6. If a key claim cannot be checked, remove/qualify it or mark BLOCKED for Evidence Gate. Editing for flow must never delete attribution/qualifications or silently upgrade the claim.

**Example ledger row**:
`C014 | "Searches for gaslighting rose 1,740% in 2022" | statistic | S009 | Merriam-Webster Word of the Year announcement, 2022, lookup statistic | dictionary lookups NOT everyday speech prevalence | PASS after source inspection | B02 | O009 | R009`.
This row illustrates structure; its status is NOT_RUN until the actual source is inspected in the episode review.

## Editorial Intelligence Gate
PASS only if all hold:
- Clear observable hook; readers can understand the thesis and findings without jargon familiarity.
- Non-specialists can explain the mechanism in plain language after hearing it; needed definitions are locally explained.
- Each major section adds an independently sourced finding or justified argumentative step.
- Source-to-Script Ledger is complete for substantive claims, current source locators inspected; counterarguments and scope limitations represented fairly.
- At least one real reported scene/case when available; otherwise clearly disclose and avoid inventing any. No fake reality effect.
- Internet-native language sounds natural when read aloud; irony limited and helpful; no repetitive rhetorical fragment chains, AI-style triplets or padded question chains.
- Ending delivers an earned interpretation, without arbitrary 3-item action checklist or obligatory comment bait.
REVISE if any stylistic, accessibility or narrative criterion fails; BLOCKED for fabricated/inaccessible central evidence. Editorial PASS never overrides Evidence Gate or final production QA.

## Regression tests (behavioral; NOT_RUN until separately executed)
E01: Substitute invented interview for sourced vignette -> BLOCKED.
E02: Reference a paper by title, invent effect size -> BLOCKED.
E03: Convert lookup growth into spoken-word prevalence -> REVISE.
E04: Say "science proves" based on moral philosophy paper -> REVISE.
E05: Script filled with "Your X? Y" fragments and internet slang -> REVISE.
E06: Explain concept creep only using an academic term -> REVISE until ordinary-language example added.
E07: Delete all study authors or source locators from final packet -> REVISE/BLOCKED as appropriate.
E08: Fully sourced evidence plus accurate on-screen author/year and reference links, natural narration -> eligible PASS upon actual inspection.
E09: Human-interest scene has no accessible primary account -> label hypothetical or remove; never call it reporting.
E10: Original inference about why labels attract likes -> HYPOTHESIS unless directly evidenced.
Record inputs, outputs, run date, actual observations and pass/fail per case. No claim of passing tests from merely creating this file.
