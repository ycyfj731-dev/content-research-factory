# Design provenance (inspected 2026-09-24)

This skill's wording, gate decisions, artifact contracts and regression specification were written for this repository. No upstream source files, code, prompts or phrase banks are vendored. References below document design ideas, not dependencies or endorsements of all upstream claims.

| Inspected upstream file | Idea absorbed | Deliberate departure |
|---|---|---|
| [roeea2/faceless-youtube-video-creation — faceless-video](https://github.com/roeea2/faceless-youtube-video-creation/blob/main/skills/faceless-video/SKILL.md) | Explicit handoffs from script through real audio, alignment and assembly | Reject one generated image per phrase; do not inherit cloned voice, provider setup or upload defaults |
| [social-media-skills — youtube-long-form](https://github.com/social-media-skills/skills/blob/main/skills/youtube-long-form/SKILL.md) | Decide the title/thumbnail promise before scripting; distinguish packaging from viewing experience | No claimed algorithm dominance, guaranteed metrics, cadence penalty or mandatory external service |
| [social-media-skills — scripting-and-storyboarding](https://github.com/social-media-skills/skills/blob/main/skills/scripting-and-storyboarding/SKILL.md) | Plan synchronized audio and visuals and estimate duration before production | Visual changes follow reasoning, not fixed cutting frequency; faceless research footage rather than shoot-day logistics |
| [mohitagw15856/pm-claude-skills — youtube-script-writer](https://github.com/mohitagw15856/pm-claude-skills/blob/main/plugins/pm-writers/skills/youtube-script-writer/SKILL.md) | Compare packaging and opening alternatives; specify visual cues with spoken writing | No mandatory hero/villain framing, sound-effect interruptions or algorithm guarantees |
| [social-media-skills — youtube-publishing-and-metadata](https://github.com/social-media-skills/skills/blob/main/skills/youtube-publishing-and-metadata/SKILL.md) | Treat metadata and upload configuration as a distinct handoff | Use real final-cut timestamps; no publishing dependency, keyword formula or automatic upload |

MIT license files were inspected for [roeea2](https://github.com/roeea2/faceless-youtube-video-creation/blob/main/LICENSE) and [social-media-skills](https://github.com/social-media-skills/skills/blob/main/LICENSE). The pm-claude-skills license was not verified; only general workflow ideas were considered and no text/code was copied. Any future vendoring must check the exact revision's license and preserve required notices.

Other names in the earlier conversation (including ffmpeg-skill and thumbnail/competitor skills) were not uniquely pinned and inspected in this implementation; they are not claimed as reviewed dependencies. Thumbnail and competitor instructions here are original task-specific guidance. All numerical gate thresholds, visual proportions and production targets are V0.1 house heuristics, not empirical guarantees or platform requirements.
