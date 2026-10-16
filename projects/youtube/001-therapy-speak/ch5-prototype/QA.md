# Chapter 5 prototype QA · 16 October 2026

**Result: actual MP4 render and technical checks PASS; final editorial/audio sign-off pending.** Reviewer: Codex, using the exported media and automated measurements described below. This is a prototype review, not a human listening certificate or approval of the existing production contracts.

## Artifact identity

| File | SHA-256 | Size |
|---|---|---:|
| chapter5-review.mp4 | a796a1296a50459081b84645d5fcd0b564cd367ec61e68bfe882d52dfb69cc04 | 2,485,691 bytes |
| chapter5-clean.mp4 | 4af9b5f696b32762d7e6f6e367dd047d449fb1e279243e48691bce8b1566ae74 | 2,207,274 bytes |

Both decode fully without corrupt frames/packets. Picture: 1920×1080, 24 fps, 1,945 frames, H.264/yuv420p. Audio: AAC, mono/44.1 kHz, one unbroken source interval 640.546–721.556. Both audio streams correlate with the decoded source trim at **0.99991581 at zero shift**; source duration 81.010 s, decoded AAC 81.014422 s. There is no measured timing shift or inserted audio segment. The full-file decoder and ebur128 loudness log are retained in the review packet.

## Eight PR #4 check categories, applied to this prototype

| Check | Result and evidence |
|---|---|
| narration_fit | PASS for source/text/trim integrity: release checksum matches, all 19 caption sentences equal locked P110–P125, continuous original audio, no inserted claims. Subjective listening remains NOT_RUN. |
| sentence_timing | PASS for inherited measured boundaries: exact archived sentence edges, candidate cut intervals contiguous, no inferred missing word times. WHO classification/qualification appear only after their supported word/sentence ends. Frame quantization is under one frame. |
| style_match | PASS for inspected prototype frames: pure white, black/gray linework and type, negative space, one visual grammar. Illustration remains schematic prototype artwork. |
| single_frame | PASS: every delivered picture is a native 16:9 continuous composition; contact sheets are explicitly review aids, not frames in the video. |
| anti_ppt | PASS at prototype scope: the same worker/schedule/phone persists across VC-27/28/30, a single boundary relation moves, source context enters once and the scene returns. No card grid or sentence-per-slide montage. The sparse opening hold and long scene holds still need viewer judgment. |
| no_unapproved_people | PASS for this user-authorized candidate prototype: one neutral illustrative worker, no named employer or alleged real participant, no invented dialogue, no unapproved mascot asset. This does not approve other DRAFT scene contracts. |
| no_fabricated_evidence | PASS: actual release audio, digest-verified alignment artifact, independently opened WHO original, original source-summary typography with citation. No simulated WHO screenshot, false graph, message text or synthetic testimony. |
| video_usability | PASS technically: both complete MP4s decoded, all sampled frames nonblank and monochrome, caption bounds checked, source attribution visible. Human continuous watch/listen, final delivery mix and final cut approval remain pending. |

These judgments do not populate `visual-batch-v1/approvals.json`, promote its contracts, or claim that every one of 1,945 encoded frames received individual semantic review. Structural drawing constraints apply to all generated frames; actual encoded samples and whole-file decoding are separately documented.

## Visual inspection actually performed

Inspected both the captioned and clean decoded-frame contact sheets, including 27 output times: 0.000, 8.125, 15.333, 16.9167, 23.0417, 23.375, 23.750, 30.000, 38.125, 38.2084, 38.375, 38.4167, 42.5417, 42.8334, 43.1667, 46.5417, 50.750, 52.000, 54.6667, 54.7084, 62.9584, 63.2917, 63.6667, 70.000, 74.625, 75.000 and 80.9584 seconds. Also inspected full-resolution actual encoded source and ending frames at 52.000 and 80.950 seconds. These cover pre/post source cuts, movement starts/midpoints/ends, source reading holds and the ending. VC-27→28 is intentionally visually continuous during the gap. The previous scene also holds through VC-29's 190 ms silent lead-in; WHO source identity appears only once its measured sentence starts.

The first layout review found final condition labels colliding with the working-week display and a phone-label spacing issue. Both were repaired before the delivered encode. Final source text, phone labels, calendar total and ending annotations are separated. The bottom 20% is reserved for captions; the clean export is empty throughout that band at all sampled times. Actual one/two-line captions remain inside it. A separate two-line collision probe was also generated and checked. Character identity, desk, device and calendar remain consistent. Hand movement interpolates an existing arm; it does not add a new limb.

Source-only frames contain no character or fictional webpage elements. “Not classified as a medical condition” stays readable for approximately 3.97 seconds before the next cut. The workplace qualifier is preserved in the source type and unchanged narration. The full WHO reference accompanies the cut.

## Executed checks

- Five new prototype regression tests PASS: canonical captions/shot boundaries; modified-alignment rejection; phrase-supported reveal edges; two-line captions, safe area and deterministic direct seek; no premature WHO classification/qualification.
- Two existing candidate tests PASS.
- Thirteen existing visual pipeline tests PASS, including source lock and fail-closed approval/provider behavior.
- Full decode and measurements PASS on both MP4s. Captioned and clean waveform correlation is 0.99991581 against the real trim, with 4.42 ms AAC end padding.

The local Windows sandbox temp directory was inaccessible during the first test attempt. The same tests passed with temporary files rooted in the workspace. This was an environment setup issue, not a missing media asset.

## Remaining review, with precise limits

1. **Human listening / continuous playback review: NOT_RUN.** Measurements establish intact decoding, source identity and waveform/timing agreement; they do not establish pronunciation, prosody, pleasant pacing or unclipped phonemes by ear. The candidate starts at a recorded first-word edge and ends at a last-word edge, so the next listening pass should pay particular attention to entry/exit handles.
2. **Final mix: REVISE before publication.** The unchanged source interval measures approximately −24.9 LUFS integrated, LRA 2.7 LU, true peak −4.4 dBFS. It is quiet relative to the skill's −16 to −14 LUFS house starting range. This prototype preserves source level; final loudness processing has not been applied.
3. **Editorial approval: pending.** The 8.014-second sparse desk hold and restrained schematic worker are reviewable choices. The four-shot candidate remains an editorial proposal, not automatically APPROVED because it now renders.
4. **Rights scope:** WHO screenshot/logo reproduction was avoided; no blanket clearance or endorsement is claimed. Existing project narration is reused under the user's instruction; original provider licensing was not independently audited. Liberation font licensing is included. No external image/music licensing blocker remains for this prototype's original artwork.

The requested audiovisual prototype is no longer blocked by missing media. A public-ready full episode remains outside this delivered review cut.
