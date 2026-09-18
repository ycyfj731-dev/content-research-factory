---
name: editorial-visual-system
description: Convert long-form educational or intellectual writing into premium editorial social-media carousels with magazine-like restraint, strong typography, semantic pagination, and consistent visual identity.
---

# EDITORIAL-VISUAL-SYSTEM v1.0

## Purpose

Turn finished long-form writing into a high-end editorial visual system for social media without changing the meaning or rewriting the approved prose.

Core principle:

> The page is not a card. It is an editorial spread.

This skill is inspired by premium magazine design principles such as:
- strong editorial hierarchy;
- disciplined typography;
- generous whitespace;
- restrained color;
- selective imagery;
- controlled pacing;
- visual confidence through subtraction.

Do not imitate or reproduce any specific publication's logo, masthead, proprietary typeface, or exact page design.

# DEFAULT FORMAT

For Xiaohongshu carousel:

- Canvas: 1080 × 1440 px
- Ratio: 3:4
- Default length: 8–10 pages
- Reading mode: portrait carousel
- Body alignment: left
- Max text width: 70–78% of canvas
- Outer margins: 88–112 px
- Top/bottom breathing room: minimum 96 px
- Page number: small, unobtrusive
- Series label: small, persistent, editorial

# VISUAL CHARACTER

The design should feel:

- literary;
- intelligent;
- quiet;
- premium;
- contemporary;
- human-edited;
- not templated;
- not “knowledge-card” style.

Avoid:

- colored information boxes;
- stickers;
- gradients;
- decorative icons;
- excessive lines;
- fake paper textures;
- AI-generated philosopher portraits used as filler;
- oversized quotation marks;
- “viral quote” treatment on every page;
- more than one accent color;
- dense PPT-like layouts.

# TYPE SYSTEM

Use no more than two type families.

## Title family
High-contrast serif or refined editorial serif.

Purpose:
- cover title;
- major question;
- rare emphasis.

## Body family
Highly readable Chinese serif or clean contemporary text face.

Purpose:
- continuous reading;
- captions;
- explanatory prose.

## Micro text
May use a neutral sans or small serif for:
- PHILOSOPHY 300;
- 001 / ORIGINS;
- page numbers;
- source captions.

Do not mix more than:
- 2 main font families;
- 3 weights;
- 4 text sizes per page.

# COLOR SYSTEM

Default:
- warm white / ivory / paper-white background;
- near-black body text;
- one muted accent color only.

Accent options:
- deep burgundy;
- dark forest green;
- muted navy;
- warm graphite.

Accent is for:
- micro labels;
- one word or line of emphasis;
- rare graphic details.

Never use accent color as large background blocks unless a specific page archetype calls for it.

# PAGINATION RULE

Pagination is semantic, not mechanical.

Do not split by equal character count.

Each page must carry one reading function:
- establish;
- ask;
- explain;
- exemplify;
- pause;
- conclude;
- transition.

A page should end at:
- a completed thought;
- a deliberate question;
- a clean rhetorical turn.

Never:
- split a sentence across pages;
- separate a claim from the sentence that explains it;
- move a necessary qualifier to the next page.

If approved text does not fit:
1. split into an additional page;
2. reduce optional visual material;
3. slightly reduce size within readability limits.

Do not rewrite approved prose just to make it fit.

# CAROUSEL RHYTHM

A 9-page essay should not have 9 identical pages.

Use density rhythm.

Recommended sequence:

1. COVER — 10–20% density
2. OPENING / QUESTION — 45–60%
3. EXPLANATION — 55–70%
4. CONCRETE EXAMPLE — 25–45%
5. QUESTION / CONTRAST — 30–50%
6. EXPLANATION — 50–65%
7. PAUSE / CORE SENTENCE — 20–40%
8. CONCLUSION — 35–50%
9. NEXT QUESTION — 25–40%

The carousel should breathe:
dense -> light -> dense -> pause -> conclusion.

# PAGE ARCHETYPES

## A. Cover
- series label small;
- title large;
- issue number small;
- no summary paragraph;
- optional single visual cue only.

## B. Essay Page
- continuous prose;
- no card containers;
- 1–3 paragraphs;
- one emphasis treatment maximum.

## C. Question Page
- short setup;
- one large question;
- generous whitespace.

## D. Example Page
- one concrete example;
- optional single line drawing or archival image;
- visual must clarify the example.

## E. Editorial Pause
- one or two sentences;
- large whitespace;
- not used as inspirational quote filler.

## F. Conclusion
- complete the current lesson;
- visually calm;
- no new major concept.

## G. Next-Lesson Hook
- appears only after conclusion;
- clearly starts a new question;
- no “preview card” language unless the brand explicitly wants it.

# IMAGE RULE

Images are optional.

Use an image only if it does one of four things:
- locates a place;
- identifies an object or artwork;
- clarifies a structure;
- provides historically meaningful evidence.

Preferred:
- archival material;
- sculpture or artifact photography;
- maps;
- manuscripts;
- diagrams;
- restrained line drawings.

Avoid decorative AI imagery unless specifically requested.

If an image is not necessary for understanding, whitespace is better.

# EDITORIAL HIERARCHY

Every page must have a single dominant element.

Possible dominant elements:
- title;
- paragraph;
- question;
- image;
- one line of text.

If two elements compete for first attention, simplify.

# CONTENT LOCK

When the source article is marked FINAL or FROZEN:

Allowed:
- line breaks;
- paragraph grouping;
- pagination;
- emphasis;
- visual hierarchy;
- captions added outside the body if factual and sourced.

Not allowed:
- paraphrasing;
- shortening;
- adding rhetorical copy;
- rewriting to fit layout;
- changing the next-lesson hook.

# PREMIUM-EDITORIAL GATE

Before rendering, check:

1. ONE_DOMINANT_ELEMENT
2. WHITESPACE_SUFFICIENT
3. TEXT_WIDTH_READABLE
4. NO_CARD_UI
5. MAX_TWO_TYPE_FAMILIES
6. MAX_ONE_ACCENT_COLOR
7. SEMANTIC_PAGE_BREAK
8. CONTENT_LOCK_PRESERVED
9. IMAGE_HAS_FUNCTION
10. DENSITY_RHYTHM
11. CONCLUSION_BEFORE_HOOK
12. SERIES_IDENTITY_VISIBLE
13. NO_TEMPLATE_FEEL

Any FAIL requires layout revision.

# PHILOSOPHY-300 ADAPTER

For 《西方哲学300讲｜从0开始》:

Persistent micro-label:
PHILOSOPHY 300

Issue format:
001 / 300

Visual tone:
literary editorial, calm, restrained, high-information but never crowded.

Default cover:
- small series label top;
- large Chinese question title;
- issue number;
- no subtitle unless necessary.

Default closing:
- current lesson conclusion on penultimate page;
- next philosophical question on final page;
- no abrupt “第二讲预告” label.

# RENDERING LAYER

Preferred execution flow:

FINAL ARTICLE
-> semantic pagination
-> page archetype assignment
-> editorial hierarchy
-> visual asset decision
-> Canva or HTML renderer
-> visual review
-> PREMIUM-EDITORIAL GATE
-> export

Canva should be treated as the renderer and reusable template host, not as the source of editorial logic.
