# Episode 001 — Diagram & Motion Visual System

- Version: 0.1
- State: PRODUCTION_SPEC_READY
- Basis: 07-av.md V0.2 + 08-assets.md V0.2
- Output frame: 1920×1080, 16:9
- Safe title area: 120 px left/right, 90 px top/bottom
- Visual mode: editorial / documentary / restrained
- Primary rule: diagrams explain relationships; they do not decorate narration.

## 1. Core visual language

### Composition
- One dominant idea per frame.
- Prefer asymmetry over centered infographic layouts.
- Keep 25–40% negative space whenever the frame is not data-dense.
- Maximum three major semantic groups in one frame.
- No icon clouds, card grids, gradient dashboards, glassmorphism, pseudo-app UI or generic “AI infographic” styling.

### Typography
Use at most two type families in the final production.
- Display / concept labels: high-contrast editorial serif or restrained grotesk.
- Body / source / qualifiers: neutral sans serif.
- Concept labels may use ALL CAPS sparingly.
- Sentence case for explanatory text.
- Avoid bolding more than one phrase per screen.

Recommended hierarchy at 1080p:
- H1 concept: 86–116 px
- H2 comparison label: 52–70 px
- Body: 34–44 px
- Source / qualifier: 24–30 px

### Lines / shapes
- Thin rules and arrows; avoid thick “presentation” arrows.
- Nodes are text-first, not icon-first.
- Rounded rectangles only when they represent an interface or classification boundary.
- Use underlines, brackets, circles and subtle boxes as editorial annotation tools.
- No 3D objects.

### Color
Final palette to be frozen at edit stage.
Until then:
- one neutral background system;
- one text color;
- one accent color for the currently active relation;
- a second accent only when comparison requires it.
Do not assign a permanent “ADHD color,” “narcissism color,” etc.

### Texture
Allow subtle print / paper / scan texture only in historical sections.
Modern diagrams remain clean.
Noise must never reduce source readability.

## 2. Motion grammar

### Default entrance
Elements appear because the argument reaches them:
1. base statement;
2. relation line;
3. second node;
4. qualifier / complication.

Do not animate everything at once.

### Preferred movement
- reveal
- underline
- bracket
- crop / pan across source
- line grows between nodes
- word physically moves between contexts
- dense material compresses into a label
- one layer fades while another remains

### Avoid
- bouncing cards
- spinning icons
- elastic overshoot
- constant parallax
- floating particles
- generic zoom-in on every keyword
- faux cinematic camera moves inside 2D diagrams

### Timing
- semantic reveal: 400–900 ms
- relation line: 500–900 ms
- source crop hold: minimum 2.5 sec
- data/qualifier hold: minimum 3 sec
- major conceptual frame: 6–18 sec depending on narration

## 3. Reusable channel motifs

### M01 — Annotation
A phrase from a document is underlined, circled or bracketed, then re-typeset outside the document as the idea enters the essay.

### M02 — Reclassification
A sentence starts as behavior/action language, then a bracket moves around the subject and converts it into a person/category label.

### M03 — Compression
A long paragraph or scattered events collapse into one portable term. On re-expansion, omitted context becomes visible.

### M04 — Search branching
A single term becomes a branching vocabulary ecosystem. Branches are limited to 4–6 visible terms at once.

### M05 — Loop
A category travels to a person/community and returns altered. Used only for Hacking / circulation feedback.

### M06 — Temporal reset
Modern clean UI collapses into archival print texture. Used for the Moscovici transition.

### M07 — Lens / attention
The same source scene remains fixed while annotation moves, causing different details to become salient. Used for “concept tells you what to notice.”

## 4. Asset production specs

---

## A05 — B03
### Behavior / mechanism — action / type — event / structure

Purpose:
Show that newer concepts are attractive partly because they operate at a different explanatory level.

Layout:
- Three horizontal rows.
- Left side: ordinary description.
- Right side: concept.
- Center: thin arrow with a small verb phrase.

Rows:
1. LAZY → possible mechanism → ADHD
2. SELFISH ACTION → person/type → NARCISSIST
3. SEXIST INCIDENT → wider structure → PATRIARCHY

Animation:
- Reveal left column first.
- Right terms enter only as their narration arrives.
- Do not imply strict equivalence; place “possible mechanism,” “person/type,” “wider structure” directly on arrows.
- Final hold 2 sec.

Source dependency:
None; this is the essay’s analytical framing.

---

## A06 — B04 / light reuse B22
### SELF / OTHER / SYSTEM

Purpose:
Orientation, not theory.

Layout:
Three words positioned across frame with wide spacing:
SELF        OTHER        SYSTEM

Under each, one small case label:
ADHD / NARCISSIST / PATRIARCHY

Animation:
- Cases enter first, then shrink into smaller type.
- SELF / OTHER / SYSTEM become dominant.
- Hold briefly and disappear.
- In B22, reuse only as a faint organizing spine behind prior scenes.

Do not:
Keep this motif on screen as permanent navigation.

---

## A09 — B06
### Vocabulary organizes scattered experience

Starting state:
Scattered phrases at irregular positions:
missed deadline
couldn’t start
lost track of time
worked for six hours straight

Middle state:
Search terms appear one by one:
executive dysfunction
time blindness
hyperfocus
ADHD paralysis

End state:
Thin lines connect specific experiences to terms.
A subtle bracket groups the field without claiming diagnosis.

Animation:
- No search-engine logo.
- Interface must read as editorial reconstruction.
- The final frame includes small label: “examples of terms encountered online.”

---

## A11 — B08
### Medicalization

Layout:
Two large text fields, not a medical infographic.

LEFT
character / morality / ordinary expectation

RIGHT
medical / psychological category

Center:
EXPERIENCE → INTERPRETATION

Animation:
One everyday phrase crosses the frame:
“I’m lazy”
It does not transform into “I have ADHD.”
Instead it moves to:
“Could there be another explanation?”

This prevents causal/diagnostic overstatement.

---

## A12 — B09
### Recognition ≠ diagnosis

Layout:
One starting node: “I recognize myself in this.”
Two diverging paths.

Path A:
read / compare / reflect

Path B:
clinical evaluation
→ multiple sources of information
→ rule out alternatives
→ diagnosis if criteria are met

Top line:
RECOGNITION IS A STARTING POINT, NOT A DIAGNOSIS

Animation:
Build Path A quickly.
Slow down on the clinical path.
Keep the inequality visible for the final 3 sec.

Source footer:
CDC ADHD diagnosis page.

---

## A13 — B10
### ADHD TikTok comment study

Data:
n = 600 sampled comments

Primary visual:
100-dot or 600-unit abstract field is optional.
Preferred cleaner design:
large “600” at left;
two numeric findings at right.

36.7%
identified with ADHD-related behaviors

5.3%
explicitly attributed ADHD to themselves

Critical qualifier:
“sampled comments on popular ADHD TikTok videos; not population prevalence”

Do not show:
42% as “self-diagnosed.”
Do not imply causal effect of TikTok.

Source footer:
Study title + year + PMC short citation.

---

## A17 — B13 / B25
### Search chain / vocabulary ecosystem

B13 state:
NARCISSIST
  ↓
narcissistic abuse
  ↓
trauma bond
  ↓
no contact

Visual behavior:
Each term behaves like a query chip / entered phrase, not a real Google screenshot.

B25 expansion:
Same NARCISSIST node branches outward:
covert narcissism
grey rock
trauma bond
no contact
narcissistic abuse

Animation:
B13 is linear.
B25 reveals branching.
This reuse visually proves “a word becomes an entrance.”

---

## A18 — B14 / B15
### Relationship retrospective timeline

Starting state:
6–8 neutral event markers on a timeline:
charm
argument
withdrawal
apology
contempt
affection
manipulation?
silence

B14:
A bracket labeled “NARCISSIST?” appears over several events.
Events snap into apparent pattern.

B15:
The bracket loosens.
Contradictory events reappear.
Some markers move outside the pattern.
Small text: “real relationships rarely align this cleanly.”

Do not:
Depict abuse graphically or diagnose a real person.

---

## A19 — B16
### Everyday label / traits / NPD

Layout:
Not concentric circles.

Use three adjacent zones with deliberately unequal borders:

EVERYDAY LABEL
“narcissist”

TRAITS / DIMENSION
narcissistic traits

CLINICAL DIAGNOSIS
NPD

Key visual:
No arrows saying one becomes the next.
A dashed line separates everyday usage from clinical category.

Footer:
APA Dictionary / MedlinePlus.

---

## A23 — B20
### Structural field

Purpose:
Show how a structural concept links domains.

Center, small:
ONE EXPERIENCE

Around it, four concrete systems:
HOME / CARE
WORK / PAY
LAW / POLICY
SOCIAL EXPECTATION

Narrative flow:
A single domestic scene expands outward into multiple institutional nodes.

Avoid:
generic feminism icons, Venus symbols, protest fists.

---

## A26 — B23
### Compression

Frame 1:
A dense but readable 3–4 line description of a relationship pattern.

Frame 2:
Text begins collapsing spatially.

Frame 3:
NARCISSIST

Frame 4:
The word remains; ghosted fragments of lost context appear behind it:
history
contradictions
motives
uncertainty
specific acts

Purpose:
Make “portable” and “context cost” visible simultaneously.

---

## A28 — B25
### Searchability as entrance

Start:
one search term

Then reveal four destinations:
definitions
personal stories
coping strategies
communities

Secondary terms appear only afterward.

End line:
A TERM BECOMES AN ENTRANCE.

No platform logo required.

---

## A33 — B29
### Internet acceleration path

Horizontal sequence:
specialist source
→ explainer / creator
→ comments
→ search
→ everyday conversation

Important:
This is not a one-way pipeline.

After first pass, faint reverse arrows appear:
comments → creator
community use → search language
everyday use → term meaning

Caption:
FASTER CIRCULATION, NOT A SINGLE CAUSE

---

## A34 — B30
### Hacking looping effect

Nodes:
CLASSIFICATION
↓
PERSON LEARNS / RESPONDS
↓
SELF-UNDERSTANDING / BEHAVIOR
↓
PUBLIC / INSTITUTIONAL RESPONSE
↺ back to CLASSIFICATION

Opening visual contrast:
ROCK — label has no social response
PERSON — can respond to classification

Then discard the rock/person comparison and leave the loop.

Footer:
Ian Hacking, “Making Up People.”

---

## A36 — B31
### PUA semantic shift

Timeline:
PICK-UP ARTIST
English-language dating subculture

→ BORROWED TERM

→ Chinese online use
emotional manipulation / coercive control

→ WORKPLACE PUA
dating context largely absent

Critical wording:
“broadened in Chinese discourse”
Never: “PUA means gaslighting in Chinese.”

Visual treatment:
English node on left, Chinese node on right.
The letters “PUA” remain fixed while the explanatory subtitle changes underneath.

This is the visual proof of:
THE LETTERS SURVIVED.
THE CONCEPT WAS REPURPOSED.

---

## A40 — B33
### No single pipeline

Four origin nodes:
MEDICINE
SOCIAL THEORY
POPULAR CULTURE
SUBCULTURE / LANGUAGE TRANSFER

All flow into:
EVERYDAY INTERPRETIVE LANGUAGE

Then routes split again.

Purpose:
Undo any impression that all concepts came from academia.

---

## A41 — B34
### Full essay synthesis

Three large verbs:
ADOPT
SPREAD
RESHAPE

Under them:
ADOPT — seems to explain more
SPREAD — compression / recognition / search
RESHAPE — ordinary users change meaning

Animation:
Use visual fragments already introduced.
No new icons or metaphors at this stage.

This should feel like recognition, not another lesson.

---

## A42 — B35
### Meaning changes while travelling

Use one neutral concept token, not a real clinical term.

Sequence:
specialist definition
→ explainer wording
→ comment shorthand
→ self-description
→ everyday phrase

At each stage, only 1–3 words subtly change.
Keep original definition ghosted in the background.

Purpose:
Show semantic drift without falsely asserting exact historical wording.

## 5. Historical source treatment

For B27–B32:
- source screenshots stay source-identifying;
- do not crop away author/title/source context;
- use slow pans/highlights, not Ken Burns on portraits;
- typography may borrow print-era rhythm but must not fabricate newspaper quotations;
- archival texture ends once returning to the modern synthesis.

## 6. Source footer system

Every evidence frame uses one consistent footer:
AUTHOR / SOURCE · YEAR

Optional second line:
sample / limitation / page context

Do not display raw URLs in the main frame.
URLs belong in description/source notes unless needed for authenticity.

## 7. Anti-Slop visual test

A diagram fails if:
- it could be used in an unrelated productivity or startup video without changes;
- icons carry more meaning than text/relations;
- motion exists without argumentative purpose;
- everything enters with the same animation;
- every spoken noun gets an image;
- clinical categories look like personality quizzes;
- citations are decorative rather than tied to a claim;
- generated visual polish makes evidence look more certain than it is.

## 8. Production order

Build in this order:
1. A05 — explanatory-level comparison
2. A13 — ADHD study graphic
3. A19 — narcissist / traits / NPD distinction
4. A17 — search ecosystem
5. A26 — compression
6. A34 — Hacking loop
7. A36 — PUA semantic shift
8. A41 — adopt / spread / reshape
9. A12 — recognition vs diagnosis
10. A33 — circulation acceleration
11. A23 — structural field
12. A40 — no single pipeline

These twelve establish the episode’s reusable graphic grammar. Remaining motion assets should be derived from them rather than designed independently.
