# Episode 001 · V6.1 — Verified Chapter Audio Timeline

**Status:** Six Runway text-to-speech generation jobs confirmed successful and returned audio assets. **Voice:** Leslie, English, eleven_multilingual_v2, 1×. **Script:** exactly the locked V6.1 (Markdown emphasis stripped, otherwise narration preserved). This timeline is the measured duration of each chapter's exported MP3 **before** adding chapter breaks or music. Files remain on the connected Runway workspace; merged local MP3, waveform QC and forced-aligned phrase/SRT timings are **NOT yet produced**.

| Chapter | Master-track start | Master-track end | Audio length | Runway task ID |
|---|---|---|---|---|
| 1 | 00:00.000 | 01:31.394 | 01:31.394 | `db47a96b-0976-474d-aa3a-e02df93de6f4` |
| 2 | 01:31.394 | 04:32.370 | 03:00.976 | `517229c6-ff72-46ff-9e9f-52bf183ae829` |
| 3 | 04:32.370 | 07:26.613 | 02:54.243 | `859bc061-c009-42f3-b5b1-fefbfc56ee6e` |
| 4 | 07:26.613 | 10:40.453 | 03:13.840 | `af757e4b-04a2-48d4-b4d6-271f23e45b3c` |
| 5 | 10:40.453 | 12:39.710 | 01:59.258 | `094c63a7-9475-418b-bb22-a191800219c3` |
| 6 | 12:39.710 | 14:20.346 | 01:40.635 | `e2e360fc-158d-4988-8772-60d1f45fa396` |

**Total measured audio:** 14:20.346 (with six chapters appended with zero extra gaps; actual assembled export may differ by encoder boundaries). Each chapter link resolves through the connected Runway asset viewer; URLs are signed/expiring and intentionally not placed in GitHub.

## Next execution gate
1. Listen to each MP3 and confirm pronunciation of Iacob, Uban, Caldwell-Harvey, Isern-Mas, Brady, Merriam-Webster, Ginapp, *Vanderpump Rules*, and technical figures, plus chapter-end pauses and consistent voice.
2. Retrieve or export all six MP3 assets to the production workspace, verify duration and decode; join them in original chapter order using audio-aware concatenation (resample/normalize if necessary).
3. Run word/sentence alignment on the **final assembled audio** against the canonical 150 narration paragraphs. Do not fabricate SRT cue times from chapter length or character counts.
4. Bind 34 VC units to actual earliest/latest speech, build English SRT and captions-safe positioning, then animate.
