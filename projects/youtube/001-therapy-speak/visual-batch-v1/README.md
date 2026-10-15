# Episode 001 — Visual Batch v1

**Status: code/configuration committed, NOT yet generated or validated.**

A 15-scene proposed experimental collage pilot: five each for Chapters 1, 2 and 5. Based on proposed scene concepts, not yet bound to exact V6.1 quotations.

## Run
```bash
pip install pyyaml
python projects/youtube/001-therapy-speak/visual-batch-v1/batch.py --mode dry-run
```
This deterministically creates `outputs/prompt_manifest.json`. No model call or credential needed.

**Generation gate**: first verify each scene against the locked narration; enter exact quotation as `narration_anchor` and change status to `script-traced`. Unsupported concepts must be replaced, not invented.

Then set `GEMINI_API_KEY` privately in the shell or an Actions secret and run `--mode generate --shots CH5-01` for a single-image pilot. The model ID is pinned to the original Nano Image Generator implementation; availability, pricing, account access, and actual results have NOT been tested. Never commit secrets.

## QA
Review each actual image on: `style_match`, `anti_ppt`, `subject_clarity`, `narration_fit`, `video_usability`. Require at least 4/5 PASS with both anti_ppt and narration_fit passing. Store review in `pilot_15_qa.csv`. Do not assume 15 pictures are successful because code executes.

The style profile is **a candidate to test**, not a final approved channel style. Archival visuals require separately sourced, cleared originals; never fabricate documents or fake social posts.
