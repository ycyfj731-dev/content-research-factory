# Artifact Modes

## video-frame
A single frame or short visual state for a video beat.
Return: purpose, composition, text, evidence constraints, motion continuation if relevant.

## diagram
Explain a relation or mechanism.
Prefer sparse relation-first layouts over infographic completeness.
Return: nodes, relation logic, reveal order, qualifiers, source footer.

## source-card
Present a real source clearly.
Return: source identity, crop/highlight plan, extracted phrase, footer and rights note if known.

## editorial-poster
A standalone visual artifact.
May be more compositionally complete than a video frame, but must retain the core evidence/annotation grammar.
Do not let poster aesthetics become the default for video.

## thumbnail
Compress the episode promise into one visual relation.
Use fewer elements than an editorial poster.
Do not reproduce a full diagram or paper page.

## storyboard
Plan a sequence of visual states across time.
Use WORLD / SOURCE / MODEL / BACK TO WORLD when appropriate.
Each panel must advance action, evidence or reasoning.

## motion-prompt
Compile the visual grammar into instructions for a video/image model or motion renderer.
Include:
- scene purpose
- visual mode
- composition
- continuity
- motion
- text handling
- evidence constraints
- negative constraints

Do not ask a generation model to render factual text-heavy evidence if a deterministic graphic/source crop would be safer.
