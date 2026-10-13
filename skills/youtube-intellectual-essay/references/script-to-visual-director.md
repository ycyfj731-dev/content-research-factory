# Script-to-Visual Director — narration, picture, and captions
Version 0.3.0. Mandatory for AV storyboard (Stage 07), asset sourcing (08), voice/caption alignment (09), assembly (10), and final QA (13).

## Intent and hard separation
Transform an evidence-verified English essay into a *visual argument*, not one new illustration per sentence. Three distinct tracks:
1. **NARRATION:** verified English script spoken as authored; the source of rhetorical pace.
2. **VISUAL:** diagrams, real documents, illustrations, motion typography, and carefully selected on-screen words that ADD mechanism, evidence, context, contrast or comic effect. Never default to reproducing each narrated sentence as large on-screen text.
3. **CAPTIONS:** accurate speech text, aligned to the **actual recorded** voice; output switchable English SRT/VTT. A separate burn-in preview is for inspection; final burn-in requires a deliberate delivery choice. Do not confuse authored display text with captions.

## Beat extraction and editorial triage
- Break the verified script into *semantic beats*: a claim, explanation, pivot, objection, concrete example, source fact or earned pause. Retain beat IDs and exact script spans and claim/source IDs. A beat may span multiple sentences; one visual can span several beats.
- Classify as OBSERVATION, HUMOR, MECHANISM, EVIDENCE, HISTORY, CONTRAST, COUNTERARGUMENT, PAUSE or TRANSITION.
- For every beat ask: **What can the viewer understand by seeing that narration alone cannot communicate as efficiently?** If none, HOLD an existing meaningful image, use restrained character reaction, archive/contextual b-roll with cleared rights, or intentional whitespace. Do not make text-only posters per sentence.
- Prioritize verified evidence even when it is not visually flashy. Editorial heuristic only: rate transformation, evidence, contrast, humor/emotional turn each 0–2. Scores 6–8 favor original motion, 3–5 simple supported visuals, 0–2 hold/minimal; this is not a scientifically validated score or a mandatory threshold. Source-dependent research can override any score.
- Avoid repeating an explanation in sequential shots; visual progression must advance the argument.
- Source papers must display correct author/year/short title or verified essential statistic and must link source IDs; illustrative material never impersonates authentic screenshots or participants.
- For online comments either use verifiable sourced excerpts with rights/provenance or clearly label **Illustrative example / Illustrative comments**. No invented engagement counts, handles or statistics.

## Shot selection — default vocabulary (not forced templates)
- OBSERVATION: fictional life vignette / restrained fixed Border Collie / illustrative social feed.
- HUMOR: ironic spatial contrast, deliberate pause or mascot glance; do not force mascot in every shot.
- MECHANISM: semantic extraction, label transformation or motion diagram; show the inferential gap where the essay argues a label is unverified.
- EVIDENCE: genuine research page, bibliography / source card, verified values and qualifying notes; allow reading time. Never swap authentic proof for generative art.
- HISTORY: sourced archives, documents, dates on a restrained timeline.
- CONTRAST/COUNTERARGUMENT: two-column evidence/claim comparison with visible qualifiers.
- PAUSE/TRANSITION: reuse an element or hold a frame; not gratuitous visual switching.
Before designing a new animated motif, test whether existing validated components can achieve the same explanatory purpose.

## Required artifacts
- `07-visual-director.json`: one row per semantic beat with `beat_id, narration_span, claim_ids, source_ids, beat_type, what_visual_adds, treatment, shot_id, on_screen_text, illustrative, timing_basis, evidence_asset_id, character_asset_id, caption_collision_notes, editorial_status`.
- `07-av.md`: human-readable visual plan mapped to beat/shot IDs and the three independent tracks; include source and licensing notes.
- `09-captions.en.srt` or `.vtt` only after the actual audio exists, with source audio version, alignment status and reviewer status. If no recording, produce a caption *plan* marked NOT_RUN; do not invent timings.
- `10-timeline.json`: every shot's in/out, source clips, audio spans, subtitle cues, fonts, source IDs, asset versions and render status.
- `13-visual-qa.md`: actual frame timestamps inspected, legibility/caption collisions/character consistency, source validation and outcome; no PASS from a mere prompt.

## Subtitle-safe composition
- Use 1920×1080 / 16:9 by default, true #FFFFFF canvas and consistent near-black typography; design for both desktop and phone readability.
- Reserve a bottom **caption exclusion band** in *composition*, provisionally the bottom ~16–20% of the picture, adjustable after viewing two-line captions. Never put essential citations, keywords or character faces behind this area. Adaptive placement may be necessary for unusual footage.
- Captions: generally one or two naturally broken lines, English punctuation, stable position, readable white lettering with dark backing/stroke appropriate to the scene; validate in video, do not prescribe one universal styling for YouTube's viewer-controlled CC renderer. Avoid word-by-word bouncing subtitles.
- Source document text and speech captions should not compete: show the critical source extract/highlight and leave enough time to read it. Avoid three simultaneous paragraphs (source, restated graphic and caption).
- Important rhetorical words MAY deliberately appear in both visual and caption; default to non-redundant imagery.

## Synchronization & motion requirements
- Start with verified narration and ideally recorded VO. Align caption cues to actual audio; link motion events to spoken phrase/word timestamps, not arbitrary guessed seconds.
- Favor deterministic frame- or absolute-time calculation; no transition that depends on how the playhead got to that state. Every frame must be independently reproducible.
- Locked character image / layered mascot assets only; never approximate the Border Collie afresh as SVG geometry for each shot. Do not claim the canonical asset is locked until an actual approved reference file exists.
- A primary label can travel between visual states, but on-screen logic must not convert reported behavior into a factual diagnosis. Simulated commentary is hypothetical.
- Locked shared fonts, measured bounds, safe margins, finite easing, authored overlap allowances, explicit entrance / hold / exit; no opacity blanks at direct seek. Avoid one-cut-per-sentence slides.
- Render keyframes at beginning, midpoint and end of each transition, plus long reading holds, at final dimensions. Inspect subtitle-on AND subtitle-off previews.

## Gates
**EDITORIAL_VISUAL_PASS** only when: each key beat has an additive visual or justified hold; claims/limitations survive transformation; no repeated concepts or gratuitous mascot; no fabricated evidence.
**CAPTION_PASS** only when: actual VO has been aligned; exact spoken meaning, legibility, punctuation and collision tested with final visuals; a file really exists.
**MOTION_PASS** only after actual deterministic render plus frame-level inspection: no clipping, collisions beyond declared allowances, disappearing required text, flicker, wrong character or unreadable data.
Any failure => REVISE the affected shots; rerun dependent checks; preserve unrelated locked shots. Without audio/rendered asset, keep relevant gate NOT_RUN, not PASS.

## Adversarial tests
T01: An ironic sentence with no new visual data must not generate a duplicate full-screen transcript.
T02: An evidence-heavy paragraph with low motion appeal still obtains a traceable sourced visual.
T03: Two long caption lines do not cover a key research number or question.
T04: A hypothetical comment is labeled and has no fake user or engagement count.
T05: A manually sought frame matches the same frame in sequential playback.
T06: Extraction never introduces words absent from the cited narration as if they were direct extractions.
T07: Changing a spoken line invalidates dependent subtitle timings and motion cues.
T08: Character-less evidence shots do not insert a decorative mascot.
