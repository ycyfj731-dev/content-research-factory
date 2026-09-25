---
name: concept-archaeology-visual
description: Create and quality-check a distinctive visual system for research-driven faceless video essays. Use for video frames, diagrams, source cards, editorial posters, thumbnails, storyboard scenes, and motion prompts when the project should feel documentary, editorial, evidence-led, restrained, and anti-PPT.
metadata:
  version: "0.1.0"
---

# Concept Archaeology Visual

Turn an argument into a visual experience where reality is primary, sources are evidence objects, diagrams are traces of thinking, and visual polish never outruns evidentiary certainty.

The default aesthetic is **documentary research + editorial graphics + restrained motion**. It is not a generic infographic style and not a fixed poster template.

## Core narrative cycle

Use this visual cycle whenever it fits the argument:

1. **WORLD** — begin from a recognizable real-world scene, object, interface, archive, or lived situation.
2. **SOURCE** — introduce the document, data, archive, or primary evidence that supports the claim.
3. **MODEL** — visualize the relation only when a diagram or motion sequence genuinely improves understanding.
4. **BACK TO WORLD** — return to reality after explanation, ideally with the viewer now noticing something differently.

Do not force all four stages into every beat. The cycle is a reasoning pattern, not a mandatory slideshow sequence.

## Visual philosophy

- Reality is the base layer.
- Sources are evidence objects, not decorative screenshots.
- Diagrams are traces of thought, not finished corporate infographics.
- Dark-red annotation signals that interpretation is happening.
- Leave room for uncertainty, contradiction and incompleteness.
- Do not make complex social reality look cleaner than the evidence allows.
- Reuse motifs across episodes so channel identity comes from grammar, not expensive imagery.

## Modes

Read [references/modes.md](references/modes.md) when producing a concrete artifact.

Supported modes:
- `video-frame`
- `diagram`
- `source-card`
- `editorial-poster`
- `thumbnail`
- `storyboard`
- `motion-prompt`

## Visual system

Read [references/visual-grammar.md](references/visual-grammar.md) for composition, typography, annotation, motion, color, source treatment, and recurring motifs.

## Evidence behavior

- Never fabricate a source page, quote, statistic, platform result, historical document, or archival artifact.
- If a source is recreated for legibility, label it as a reconstruction and preserve the factual wording/citation.
- Generated imagery may illustrate a hypothetical scene but must never authenticate a real event, diagnosis, study result or historical claim.
- The stronger the factual claim, the more restrained the visual treatment should be.
- Clinical labels must not look like personality quizzes or deterministic identity categories.

## Anti-PPT / Anti-AI-infographic rules

Reject or revise a visual if it relies on:
- symmetrical card grids by default;
- dashboard composition;
- glassmorphism;
- 3D icons;
- icon clouds;
- every noun getting its own picture;
- overly complete flowcharts;
- glossy AI faces;
- generic “sad person looking at phone” imagery;
- motion with no argumentative purpose;
- every frame sharing the same entrance animation;
- a diagram that could be dropped into a startup deck unchanged.

## Output behavior

For a requested visual:
1. classify the beat as WORLD / SOURCE / MODEL / BACK TO WORLD;
2. decide the best mode;
3. state the visual purpose in one sentence;
4. define source/evidence constraints;
5. produce the artifact or production prompt;
6. run the visual QA in [references/qa.md](references/qa.md);
7. revise before delivery if the result fails.

For multi-beat video work, do not generate all beats as posters. Alternate evidence, lived scenes, source material, motion, and diagrams according to the argument.

## Relationship to YouTube Intellectual Essay

This skill is the visual execution layer for `youtube-intellectual-essay`.

- Stage 07 uses it for visual reasoning and storyboard treatment.
- Stage 08 uses it to classify source / diagram / B-roll / archive / generated asset roles.
- Stage 10 uses it to preserve visual grammar during assembly.
- Stage 11 may use its thumbnail mode, but packaging promise still comes from the parent essay skill.

Do not duplicate research or evidence rules from the parent skill. When claim support is uncertain, defer to the parent Evidence Gate.
