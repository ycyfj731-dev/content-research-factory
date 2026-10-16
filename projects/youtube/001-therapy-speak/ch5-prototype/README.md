# Episode 001 · Chapter 5 · VC-27–VC-30 audiovisual prototype

**State: RENDERED_REVIEW_PROTOTYPE.** This folder contains an actual contiguous cut using the real V6.1 release narration, original black-and-white line artwork and the four-shot edit candidate already in PR #4. Start with [the captioned MP4](review/chapter5-review.mp4), [the clean MP4](review/chapter5-clean.mp4), or the [decoded-frame contact sheet](review/encoded-review-contact-sheet.jpg). [QA.md](QA.md) records checks and remaining review.

The user's request authorizes this prototype and its PR commit. It does not upgrade the existing `visual-batch-v1/contracts.json` or provider-generation approvals. No paid model, image-generation, TTS, voice clone, upload to YouTube, PR merge, or invented source media was used. The original V6.1 script, traceability, speech map, candidate and contracts are unchanged.

## What is in the cut

| Shot | Master audio interval | Output interval | Picture |
|---|---|---|---|
| VC-27 | 640.546–657.488 | 0.000–16.942 | Neutral desk, then the illustrative worker; the narrated 60-hour working week and weekend phone appear after their measured sentence |
| VC-28 | 657.488–678.720 | 16.942–38.174 | Same worker and schedule; one personal boundary moves the phone outward while the schedule stays fixed |
| VC-29 | 678.720–695.227 | 38.174–54.681 | WHO attribution and original source-summary typography; classification and qualification appear only after supporting speech |
| VC-30 | 695.227–721.556 | 54.681–81.010 | Return to the same scene; one restrained gesture changes the individual side, with the stated work conditions remaining visible |

The first 8.014 seconds intentionally hold a sparse desk before the measured worker sentence begins. This is a conservative context hold, not an invented earlier anecdote. Shot boundaries reproduce the candidate's editorial proposals; inherited speech boundaries remain distinguished from those cuts. At the start of VC-29, the previous scene holds through the 190 ms silent lead-in until the WHO sentence begins at master 678.910 / output 38.364. Display times round up to the next frame, by less than 41.667 ms at 24 fps.

The MP4s are 1920×1080, 24 fps, H.264/AAC. The single original narration interval is 81.010 s; the picture is 1,945 frames / 81.041667 s. AAC decoded padding adds about 4.42 ms, and the picture has about 31.67 ms of final frame rounding. The captioned MP4 is an inspection copy with burned-in English captions. The clean MP4 plus [the separate SRT](review/chapter5.en.srt) preserves the separate narration/picture/caption tracks.

## Actual sources and rights treatment

**Narration:** [Episode 001 — Voiceover Master release](https://github.com/ycyfj731-dev/content-research-factory/releases/tag/episode001-audio-v1), asset `639097451`, `Episode_001_V6_1_full_narration_master.mp3`, 11,109,892 bytes. Downloaded asset SHA-256:

`415fe806af8f9f7a14222520629b0941b0a28d603c39c593c20b933c8605c175`

This is the existing project narration reused at the user's request. The original voice-provider licensing contract has not been independently audited. No narration wording, speed, sequence or level was changed; the only edit is one continuous trim. The measured output is quiet at approximately −24.9 LUFS integrated, with true peak around −4.4 dBFS. Final loudness treatment and listening approval remain pending.

**Alignment:** [successful WhisperX Actions run 38517068375](https://github.com/ycyfj731-dev/content-research-factory/actions/runs/38517068375), artifact `11872935346`. The recovered local ZIP's SHA-256 exactly matches GitHub's live artifact digest:

`adb8faa6183d357eba5a2699486d7d914faaf68377d511af79a84ee2f29af639`

The CI download log identifies the same release URL, 11,109,892 bytes and decoded duration 860.345750 s. The old local `master.mp3` is truncated and was rejected; it is not used in this render. The inherited alignment is not a newly performed acoustic alignment. The old job did not record the audio checksum, so that historical link is supported by URL, size and job output rather than an old audio hash. [timing.json](timing.json) preserves the 19 original sentence records and all 203 word records for P110–P125, including null timing for `sixty` and `understaffing,`. Caption text is checked against the locked script. No missing word time was interpolated.

**WHO-2019-BURNOUT:** World Health Organization. *Burn-out an “occupational phenomenon”: International Classification of Diseases.* Departmental update, 28 May 2019. [Original WHO article](https://www.who.int/news/item/28-05-2019-burn-out-an-occupational-phenomenon-international-classification-of-diseases), accessed 16 October 2026. The opening paragraphs and ICD-11 definition support the occupational classification, the distinction from a medical condition and the explicit workplace context. They do not establish a clinical diagnosis of the illustrative worker, or independently prove the essay's broader argument about popular advice.

The WHO shot uses our own layout and concise source-linked summary, with publisher, date and domain visible. It contains no WHO logo, screenshot, copied artwork, fake webpage, simulated archive or implied WHO endorsement. Attribution does not establish blanket screenshot or commercial reproduction clearance; none is claimed. Full source identification is preserved here and in [provenance.json](provenance.json).

**Artwork:** original deterministic line drawing for this prototype. One neutral illustrative human, no identifiable employer, fake message text, invented testimony or claimed research participant. The human is explicitly permitted by the four-shot candidate; no unapproved mascot reference is approximated. The hypothetical scene is labeled “Illustrative example.”

**Fonts:** Liberation Sans Regular and Bold, unmodified, from the bundled `pdfjs-dist/standard_fonts` package. The full [SIL Open Font License 1.1 and copyright notices](fonts/LICENSE_LIBERATION) accompany the files. No external image or music licenses are needed for this original-art prototype.

## Reproduce

From the repository root, with Python 3.11+:

```sh
python -m pip install -r projects/youtube/001-therapy-speak/ch5-prototype/requirements.txt
python -m unittest discover -s tests -p 'test_ch5_prototype.py' -v
python projects/youtube/001-therapy-speak/ch5-prototype/render.py --audio work/narration.mp3 --download-audio --outdir outputs/ch5-prototype
python projects/youtube/001-therapy-speak/ch5-prototype/inspect_export.py --outdir outputs/ch5-prototype
```

If the release has already been downloaded, pass its path with `--audio` and omit `--download-audio`. A missing file or checksum mismatch blocks rendering. No replacement/silent audio is generated. `--frames-only` produces actual stills and SRT for layout review; it explicitly reports MP4 NOT_RUN.

FFmpeg is selected from PATH when installed, otherwise from the pinned `imageio-ffmpeg` package. Exact font bytes are included. Reproduction means the same content, timing and deterministic frames; encoded bytes can differ across operating systems/FFmpeg builds. [The local render report](review/render-report.json) records the actual encoder version, renderer digest, font hashes and MP4 hashes. [Export checks](review/export-checks.json) record whole-file decoding, zero-shift waveform agreement and sampled encoded frames. Neither script manufactures a human listening review.

[The dedicated GitHub Actions workflow](../../../../.github/workflows/episode001-ch5-prototype.yml) runs these checks and produces downloadable review artifacts on matching PR updates or manual dispatch. It only reads repository contents and public source audio; it does not publish or approve the cut.

## Review packet

- [timeline.json](timeline.json): four shots, original/output coordinates, exact supporting phrases and reveal times.
- [provenance.json](provenance.json): acquisition, checksums, source locators, rights basis and limitations.
- [QA.md](QA.md): what was actually checked, and the remaining listening/editorial/mix review.
- [review/](review/): both real MP4s, SRT, decoded-frame sheets and measured reports.

The production gate remains **review required**, not READY. This prototype demonstrates an executable audiovisual sequence; it does not certify the full episode or replace the existing semantic approvals.
