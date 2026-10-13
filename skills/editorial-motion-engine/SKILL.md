---
name: editorial-motion-engine
description: Implement and verify deterministic, caption-safe animated editorial shots for evidence-led faceless video essays.
metadata:
  version: "0.1.0"
---

# Editorial Motion Engine 0.1.0

Working prototype: [demo/index.html](demo/index.html). Two regression scenes: semantic extraction and JUDGMENT/EVIDENCE. This is NOT a finished MP4 renderer.

## Input and ownership
- Read [Script-to-Visual Director](../youtube-intellectual-essay/references/script-to-visual-director.md) and parent visual-style contract; narration/visual/captions remain distinct tracks.
- AI chooses meaningful shot type and validated content; deterministic renderer owns exact text geometry and time.
- Preserve source IDs, illustrative labels, verified content, and copyright metadata; no AI reconstruction of scientific paper data.
- Never approximate the canonical Border Collie from fresh SVG paths. Only insert a user-approved, versioned asset; the proof-of-concept deliberately omits the character.

## Determinism
- Compute visual state using pure absolute-time seek(t), frame n = t × FPS. No setInterval/CSS keyframe sequencing in final frames.
- Separate text from motion transforms. Essential evidence should never disappear in a direct seek.
- Typography must fit all frame boundaries with caption-safe band reserved; avoid duplicating spoken captions in the main scene.
- Direct seeking, replaying and independent rendering of a frame must produce equivalent state. Verify on the exact toolchain/environment before calling PASS.

## Reproducible local testing
```bash
cd skills/editorial-motion-engine
npm install
npx playwright install chromium
npm test
```
Playwright tests in [tests/motion.spec.js](tests/motion.spec.js) check direct seek, retained evidence questions, word provenance, bounds, and generate nine visual checkpoints in test-results/. Review screenshots before approving; passing geometry alone cannot establish excellent motion design.
Do not claim tests were run until command outputs and inspection are available.

## Next implementation gates
1. Add external shot-manifest JSON parser/schema; prevent unsupported extractions.
2. Use font loading and text measurement, advanced path morph and individual token continuity.
3. Add actual caption overlay and source-card scene with two-line caption collision QA.
4. Lock a canonical layered Border Collie asset, then add micro-animation without identity regeneration.
5. Render numbered frames with headless Chromium, encode with FFmpeg, align real VO and SRT.
6. Benchmark at least ten different text lengths and report verified pass rate.

Status: prototype committed; local runtime/render acceptance NOT_RUN unless separately demonstrated.
