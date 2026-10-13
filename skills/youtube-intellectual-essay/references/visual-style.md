# Visual Style — White Minimal Editorial Comic + Border Collie Character
Version 0.3.0. Mandatory visual contract for episode planning, storyboards, art direction, generation, and final visual QA.

## Creative direction
**White Minimal Editorial Comic**: intellectually mature editorial illustration + pure-white minimalist information design. No live-action reenactments of human experience as the default. Make the explanation visually clear and memorable; do not decorate for decoration's sake.

- Canvas: separate native 16:9 frames (default 1920×1080); no multi-panel storyboard contact sheets masquerading as finished shots.
- Background: pure #FFFFFF, no cream, paper texture, gradients, fake torn magazine, cinematic filters.
- Typography: near-black #111111, gray #666666 secondary, consistent clean sans-serif (Arial/Helvetica-like); clear hierarchy and generous margins, approximately >=6% safety margin.
- Illustrations: clean black lines, simple shapes, restrained shadow and strict black-and-white character markings. No flashy palettes; any additional highlight must clarify a specific point.
- One meaningful visual idea per shot; allow white space; favor several well-composed layouts rather than identical centered slides.
- Motion: purposeful element continuity, precise typography, semantic extraction, restrained spatial transformation; use fades only when they serve the beat. Motion follows measured voiceover timing rather than obligatory 3-second cuts. Deterministic time/frames and verified text bounds are required for final animated delivery.
- Camera/visual balance: comic scenes for lived experiences, real documents/clean custom research cards for evidence. No decorative pseudo-academic visuals. Avoid 15-minute text-only slideshows.

## Recurring character — Black-and-white Border Collie (channel direction)
Use the same **black-and-white Border Collie wearing round glasses** as a recurring dry-humor observer when a character adds meaning. The channel direction is locked, but a pixel-consistent production asset must still be explicitly approved before claiming the character file is locked. Identity and anatomy must remain stable across episodes and outfits/poses.

Character bible:
- Breed: recognizable Border Collie; black ears and crown, white central facial blaze, white muzzle and chest, black back, thoughtful eyes, consistent round eyeglass frame. Preserve canine muzzle, ears, paws and breed proportions; do not drift into cat-like triangular ears or flat-faced cartoon shapes.
- Editorial comic look, tasteful linework, appealing and intelligent, mild dry-humor expressions; not a human-bodied cosplay animal by default; paws remain paws. Avoid ugly, distorted, uncanny, exaggeratedly grumpy/sleepy, chibi, plush-toy, children's-book, anime, or superhero treatments.
- Keep muzzle length, head-to-body ratio, ear size, facial blaze and fur patches consistent. Use an approved canonical reference image/character sheet as the generation anchor when available; until one is explicitly selected, do **not** claim exact image-to-image identity is locked just by text instructions.
- Expressions adapt to scenes: mildly skeptical while reading the phone; genuinely tired at work; thoughtful while considering a claim. Do not render everyone as distressed or the dog as permanently gloomy.
- For laptop/phone/desk situations use a few essential objects only. No automatic mugs, clocks, stacks of books, notification storms, or repetitive floating jargon labels.

When to use: hypothetical relationship scenes, social interactions, digital discourse, workplace stress, daily-life situations. Do **not** force character into citations, historical archives, evidence charts, timelines or detailed explanatory diagrams where it adds no comprehension. Other roles may be implied via cropped chat bubbles or neutral graphic signs; preserve recognizable Border Collie protagonist. Never depict an actual research participant as the Border Collie unless explicitly framed as a fictional illustrative scene.

## Evidence, provenance and rights
- Real historical material, reputable primary-source documents, accurate bibliographic detail, verified numbers, and charts are evidence; cartoon reconstructions must not impersonate actual screenshots, respondents or interviews.
- Illustrative comment cards are visibly labeled "Illustrative example" when not sourced; never add fake counts, accounts, reviews or quotations implying real-world evidence.
- Charts must use verified actual underlying values. Never fabricate time series from a single annual growth percentage or unverified Google Trends images.
- Research participant quotes must be verbatim and cited, or rendered as clearly marked summary without quotation marks; no synthesized testimonial.
- Generated illustrations are not archival photos or valid source citations. Maintain a source/rights ledger and distinguish original designs from sourced media.
- Academic conclusions displayed in graphics must retain qualifiers; the storyboard and narration claim IDs must map to source IDs.

## Composition patterns
A) Typographic insight: one short line or question, large and legible, ample white.
B) Border Collie scene: compact Border Collie vignette on one side, short informational text on the other; no random clutter.
C) Source reveal: cropped verifiable document/film information + carefully authored annotation with citation.
D) Mechanism: simple before/after words, label vs evidence, one controlled transition; illustrative examples flagged.
E) Numerical evidence: one verified statistic and clear unit, period, original source; no fake chart.

## Quality gate (VISUAL_PASS)
Reject or REVISE when:
1. Off-white background, over-designed collage, heavy color/texture or excessive decorations.
2. Border Collie inconsistent/unattractive, wrongly proportioned, overly infantilized, or gratuitously present.
3. Frame is a multi-shot sheet rather than an independent 16:9 shot.
4. Text unreadable at phone size; too much text; ornamental motion.
5. A comic/example is presented as authentic user testimony, a false chart or authentic source screenshot.
6. Frame merely restates narration and adds no evidence, emotional context, mechanism or editorial clarity.
7. User-selected reference mascot is disregarded; need stable reusable character reference with approval.
8. Different chapters look like unrelated visual products.

For storyboard and animation, reserve a caption exclusion band near the bottom (initially ~16–20% of frame), verify with two-line subtitles on and off, and do not put essential evidence or character faces in that band. Use approved consistent mascot image/layer assets; never redraw the mascot as crude SVG primitives. See [Script-to-Visual Director](script-to-visual-director.md) for beat selection, caption track, deterministic movement and checks.

Pass only after inspecting the actual image assets; a written storyboard or generated prompt is a DRAFT, not VISUAL_PASS.

## Testing (not automatically executed)
V01: opening and burnout scene share consistent Border Collie identity, lineweight, margins.
V02: source-only frame omits mascot and shows exact source ID.
V03: deliberately busy scene fails and is simplified.
V04: hypothetical comment UI visibly marked illustrative; no fake engagement statistics.
V05: 2022 dictionary +1740% is not visualized as invented 2017–2022 series.
V06: native single 16:9 assets generated; storyboard grid not treated as final frames.
V07: mobile-size text and safe margins inspection.
Record tested assets, reviewer judgment, and actual pass/fail separately.
