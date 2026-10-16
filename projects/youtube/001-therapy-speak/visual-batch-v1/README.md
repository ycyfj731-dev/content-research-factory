# Episode 001: locked V6.1 / 34 visual units

Status: offline validation/compiler implemented; **zero production images generated or approved**. All 34 scene contracts are DRAFT. The original narration and traceability document are unchanged. No old `script-traced` flag constitutes visual approval.

## Free local execution (Python 3.11+, standard library only)

```sh
python -m unittest discover -s tests -p test_visual_pipeline.py -v
python projects/youtube/001-therapy-speak/visual-batch-v1/batch.py --mode validate
python projects/youtube/001-therapy-speak/visual-batch-v1/batch.py --mode dry-run
python projects/youtube/001-therapy-speak/visual-batch-v1/batch.py --shots VC-01
```

Dry-run writes `outputs/prompt_manifest.json`, not pictures. Exit 0 means mechanical validation succeeded, **not production readiness**. A draft has no prompt and reports BLOCKED_DRAFT. Unknown/duplicate IDs, broken source locks and invalid contracts exit 2. `--mode generate` exits 2 even after editorial approval: the legacy network adapter was removed; no credentials, secrets, model endpoint or paid calls are used. CI performs only offline tests and compilation.

## Source and sentence contract

`source-lock.json` pins the text bytes (only CRLF/LF checkout differences are normalized) of the V6.1 narration and 34-unit trace. The compiler independently compares all 150 verbatim paragraphs, chapter IDs, source line ranges and ordered unit coverage. It derives 184 sentence spans with stable paragraph/sentence IDs, exact quotations and character offsets; concatenation is lossless. Sentence segmentation is conservative punctuation-based, not a linguistic or forced-alignment claim. Review boundaries when editing contracts; never rewrite the narration to fit images. No arbitrary timestamps are generated.

`contracts.json` contains every unit and every sentence. Fill each unit's `elements` and set READY_FOR_REVIEW. Each object, action, person, metaphor or hold requires:

```json
{"kind":"object","description":"Concrete visible object and its purpose","sentence_id":"P001-S01","quote":"Apparently, everyone's ex is a narcissist these days.","appears_at":"P001-S01"}
```

This is a schema example, **not an approved scene**. Every sentence requires explicit treatment (including a hold if nothing changes). A matching quotation is necessary but cannot establish semantic relevance: an editor must check every depicted claim and action. No dinner before P029, invented partner transcript, boss confrontation, company reform, fake archive, random portrait or additional anecdote. Holds must identify the approved prior frame they retain. Authentic source material needs separate provenance/rights clearance and cannot be fabricated with an image model.

## Style and approval gates

The only active style constant is in `batch.py`: black ink on white, one continuous 16:9 editorial line drawing; no color, photo collage, panel grids, contact sheets, PPT, slide layouts, readable text or random people. `border_collie` is absent or optional. A dog is not required and any proposed appearance still needs a relevant approved task. A unit may need successive frames at sentence boundaries; do not pack those changes into one multi-panel image. Before a future provider adapter is enabled, frame-specific approved prompts and audio alignment must be resolved; this compiler produces review candidates only.

`approvals.json` deliberately contains no approvals. Only a real editorial decision may populate it. Record top-level `compiler_sha256` (text_digest(batch.py), with CRLF normalized to LF) and `style_sha256` (digest(STYLE)); per unit record `decision: APPROVED`, reviewer, reviewed_at, semantic_review: PASS, and the exact contract_sha256/prompt_sha256 from the manifest. Hashes use the module's `digest()` (canonical JSON for non-bytes). Compiler, style, task or prompt changes invalidate approval. Do not edit hashes to silence a failure; review the changed candidate. The source lock and approval ledger require trusted repository review: hashes detect drift, not malicious approval forgery by someone with write access. No auto-approval command is provided.

## Actual-image QA

After an independently reviewed future adapter exists, import actual PNG outputs and run:

```sh
python projects/youtube/001-therapy-speak/visual-batch-v1/batch.py --mode qa --shots VC-01 --qa-report path/to/reviews.json
```

The JSON is keyed by VC ID. Each review needs reviewer, reviewed_at, prompt_sha256, path relative to this folder (under outputs/), image_sha256 of actual bytes, and `gates`. ALL eight gates must be PASS: narration_fit, sentence_timing, style_match, single_frame, anti_ppt, no_unapproved_people, no_fabricated_evidence, video_usability. Missing, PENDING or FAIL blocks release; no 4/5 shortcut. The compiler verifies approval binding, artifact containment/hash, PNG chunks/checksums/pixel stream and 16:9 dimensions. Humans must inspect the full actual frame and aligned audio for semantic fit, palette, linework, panels, people, readability and reveal timing. A valid PNG or successful dry-run cannot prove these. QA for a selected subset does not approve the other 33 units and never marks the episode production-ready.

Example review shape (placeholders are intentionally not runnable approvals):

```json
{"VC-01":{"reviewer":"editor identity","reviewed_at":"review timestamp","prompt_sha256":"exact approved prompt digest","path":"outputs/VC-01.png","image_sha256":"actual PNG digest","gates":{"narration_fit":"PENDING","sentence_timing":"PENDING","style_match":"PENDING","single_frame":"PENDING","anti_ppt":"PENDING","no_unapproved_people":"PENDING","no_fabricated_evidence":"PENDING","video_usability":"PENDING"}}}
```

## Audit and remaining work

The prior pipeline compiled only 15 pilot shots in Chapters 1/2/5, accepted any nonempty narration anchor plus a self-declared script-traced flag, and did not read the locked source. Its cream/red/blue photographic collage prompt contradicted the requested style. CH1-03 attached invented conversation imagery to a vocabulary list; several shots broadened quoted content without a frame-specific claim review. The 4/5 QA rule could pass style/subject failures and was not enforced in code. The old workflow asserted 15 prompts and did not test safety failures. Provider results selected the first image without rejecting multiple images or validating image semantics. These are root causes, not evidence of successful images.

Old prompt/config/15-shot CSV/YAML are quarantined under `legacy/` for audit, never loaded. Separate `visual-dev/gaslight_styleframes.py` and archive-render workflow remain historical research experiments, not approved production paths; their beige photographic layouts do not pass this style lock. The locked historical trace's proposed PPT/typography language is also not current visual approval. No historical document was rewritten to hide that conflict.

Still pending: 34 concrete frame task designs and human semantic review; approval of this compiler and exact frame prompts; reviewed provider integration and explicit paid-run authorization; actual image generation; audio-aligned sentence timing; citation/rights clearance where relevant; all actual-frame QA, motion and final edit. No real image has been reviewed in this repair, and no image-generation cost was incurred.

## Repair validation record (2026-10-15)

- Python 3.12 / Windows: all 13 visual regression test methods passed (including eight contract-negative subcases).
- Offline full repository run with socket connections blocked: 69 passed, 1 failed, 8 subtests passed. The failure is the unchanged `test_external_json_classifier_accepts_strict_json_protocol`: existing POSIX `shlex.split` processing strips Windows path backslashes, so its child Python executable cannot be found. This repair does not change that unrelated classifier.
- `--mode validate` and `--mode dry-run`: 34 units; source coverage valid; all scenes explicitly BLOCKED_DRAFT; zero actual images.
- Git diff confirms locked narration and original traceability file unchanged.
- Linux CI is configured but not claimed as locally executed. Actual image/style/motion QA remains pending.
