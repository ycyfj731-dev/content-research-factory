# Production and delivery

## 07 AV Storyboard

Write synchronized audio/visual rows, not a narration file with a B-roll wishlist. Each row specifies beat ID, start/end estimate, spoken text or exact script span, claim IDs, what changes on screen, visual purpose, asset IDs, sound and transition intent. Indicate `estimated` timing until audio exists. Longer arguments may use multiple shots; one sentence need not equal one image.

Prefer explanatory movement: reveal a relation, highlight a passage, compare two choices, add one variable to a diagram. Use a restrained palette, at most two main type families and consistent labels as defaults. Run planned Anti-Slop Gate before asset production. A failed sequence returns to the visual explanation, not to indiscriminate generation.

For generated or staged scenes, add a **scene packet** only when the beat genuinely needs generation. The packet records scene duration, shot progression, composition, camera movement, continuity constraints, sound intent and negative constraints. Preserve identity, wardrobe, props, geography, lighting direction and time of day across panels/shots. Do not generate a storyboard sheet merely to decorate a documentary/evidence beat that is better served by a real document, archive item or original diagram.

Storyboard timing must add up to the scene duration. Each panel/shot advances action, information or perspective; avoid near-duplicate frames. For recurring generated characters or locations, use the approved visual reference when one exists rather than relying on text-only descriptions.

## 08 Visual Source Plan

For each asset, record its source/creation method, creator, item URL, local path when acquired, visual family, intended beat, rights basis, license terms/link, attribution, restrictions and fallback. Status is `lead`, `verified`, `acquired` or `rejected`. A collection homepage, “found on Google,” age alone, or download availability does not establish reuse permission.

Archives and historical images: inspect item-level rights and provenance. Licensed B-roll/music/fonts: verify the intended use against the actual license. Screenshots/documents: capture only what is needed for commentary and record the use rationale; do not declare all screenshots fair use. If a legal conclusion is required, verify current authoritative guidance rather than inventing clearance. Prefer a cleared alternative when rights remain unresolved.

Diagrams/typography: original explanatory graphics; retain underlying data and citations for real charts. Label invented interfaces and hypothetical examples. AI shots: define narrative purpose, duration, continuity, prompt and disclosure needs; prefer short atmospheric bridges where a real asset would add no evidence. Never use generated material to authenticate a real event or person.

Keep rights evidence and attribution alongside the manifest. An unresolved asset blocks its use in a final render but not replacement planning. Do not acquire paid assets or generate paid media beyond the user's authorization.

## 09 Voiceover

Use an authorized synthetic voice suited to calm, interested English explanation. Record provider/model/voice identifier and settings actually used, pronunciation guidance for names and terms, and script version. Do not assume a specific provider is connected. Voice cloning requires rights/consent; a licensed stock voice is the default practical alternative.

When generation is authorized, test a short passage containing the hardest names and a quiet/animated transition before producing the full narration. Listen for mispronunciation, omitted qualifiers, repeated lines, rushed reasoning and unnatural joins. Regenerate affected segments rather than silently altering the explanation. Keep a clean master and the final edit audio.

Transcribe/align the actual audio to make SRT/VTT; compare against the verified script and correct recognition errors. Measure total duration and retime all downstream artifacts. Without audio, deliver only clean text and settings/pronunciation instructions; audio QC and measured timestamps remain NOT_RUN.

## 10 Video Assembly

Treat the **approved narration/audio as the timing spine** for a faceless essay. Visual edits follow speech structure unless a deliberate silent beat, archive sequence or sound-led transition justifies otherwise. Once real audio exists, update the storyboard and asset intervals from measured timing before assembly.

Use an explicit edit decision list or timeline manifest as the contract for assembly. Each row/entry resolves a beat to real source files, in/out points, output-timeline position, crop/scale behavior, overlays, captions and audio treatment. Do not let shell glob order, “latest file” heuristics or ad-hoc editor state determine sequence order.

Source files are read-only. Render cuts and intermediates into a dedicated edit/output directory. Prefer deterministic mechanical execution (for example FFmpeg for trims/concat and Remotion or equivalent for programmatic overlays) after the editorial decisions are frozen. AI decides what the beat means and what should stay; the renderer should execute those decisions reproducibly.

For source-video cuts, never cut inside a spoken word. Snap cut edges to transcript/word boundaries when available and leave small safety padding where timestamp drift would otherwise create clipped phonemes or pops. Add short audio fades at hard segment boundaries when needed. Build subtitle timing against the **output timeline**, not original-source timestamps, and apply captions after overlays so graphics do not cover them.

Use an available editor or FFmpeg workflow; this skill does not ship an assembler. The edit manifest must resolve each asset ID to a real file and timeline interval, with explicit trims, scaling/cropping, layering and audio levels. Check gaps, overlaps, zero-length shots and missing files before rendering.

Default delivery profile: 1920×1080, 16:9, H.264/AAC MP4 with a consistent frame rate suited to source footage (typically 24 or 30 fps). Choose a speech-forward mix; around -16 to -14 LUFS integrated and true peak at or below -1 dBTP are house starting targets, not mandatory platform policy. Measure the final mix, listen on headphones and ordinary speakers, and fix clipping or music masking.

Before delivery, inspect the actual render rather than trusting the manifest. Probe duration/streams/frame size; compare audio/video ends and subtitle timing; inspect frames around cut boundaries plus the first, last and several midpoints; check grade consistency, hidden captions, overlay timing, black frames, missing assets and repetitive visual patterns. Fix and rerender before presenting a final artifact. Run rendered Anti-Slop Gate; planned PASS is insufficient.

## 11 Thumbnail

Return to the selected promise after the cut exists. Make two or three meaningfully different compositions, not color-only changes. Show one clear relation/object or dilemma, readable contrast and limited text. Inspect the actual thumbnail at roughly 160×90 as well as full size; avoid tiny text, fabricated quote attribution and synthetic “evidence.” Brief-only work remains DRAFT until an image is rendered and inspected. A/B testing is a later measurement task, not a predicted result.

## 12 Metadata

Prepare selected title, concise English description, source links, asset credits, relevant tags, language, category, audience setting with rationale, intended visibility and any applicable synthetic-content disclosure. Match the final cut; remove unsupported claims or unused sources. If current platform field limits, audience rules or disclosure policy matter to upload, check official YouTube guidance at execution time and record the date. Do not hard-code past monetization claims as channel strategy.

Derive chapter times from the final edit; estimated chapter outlines stay labeled DRAFT and cannot masquerade as measured timestamps. A draft visibility suggestion is not authorization to upload. Publishing is outside the default thirteen-stage deliverable: perform it only when the user requests it and the destination/settings are known.

## 13 Final QA

Record artifact versions and evidence for every check:

- Final Topic decision and packaging promise still match the episode.
- Retained factual claims, quoted words, charts, titles, captions and modern applications pass Evidence Gate.
- Storyboard and actual cut pass Anti-Slop; duration shares use the final timeline.
- All included visuals, music, fonts and voice have documented usable rights or an explicitly resolved use basis; credits are present where needed.
- Actual narration is faithful and intelligible; pronunciation, mix and captions were inspected.
- Export is 10–15 minutes (or a recorded user-approved different target), technically playable and synchronized; no missing assets or draft placeholders.
- Thumbnail is legible at small size; metadata and chapter timestamps match the export.
- Full video has been watched, with required policy/disclosure settings verified for an intended upload.

Only issue `READY` when all applicable checks PASS with actual artifacts. A planning-only packet is `DRAFT`; unavailable required tools/assets make production `BLOCKED`. List exact repairs or missing inputs, and deliver completed work without implying that files were generated, tests were run or publishing occurred when they did not.
