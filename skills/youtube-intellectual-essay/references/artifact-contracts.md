# Episode artifact contracts

Use Markdown tables, CSV or JSON according to the task; these fields are the interoperability contract, not a required software stack. IDs are stable within the episode: `S01` source, `C01` claim, `B01` beat, `A01` asset. An ID alone is not a citation.

## Packet header and status

Record episode ID, working title, audience, target duration, format, version/date, requested scope, assumptions, available tools, authorized spending/actions and dependency versions. Keep a stage status table with artifact path, state, reason and next action. Never infer permission from a copied template.

## Source ledger

`source_id | author/creator | title | year | edition/translation or study identity | URL/DOI | accessed_date | access_level | locator | relevant finding/passage | limitations/corrections`

## Claim ledger

`claim_id | exact proposed wording | type | script/packaging locations | source_ids | precise locator | support rationale | scope and counterevidence | decision | repair/review version`

The support rationale says how the inspected passage supports this wording; it cannot just say “has citation.” For interpretation/modern application include the inferential step. For illustrations record that no observation or prevalence is asserted. Keep withdrawn claims in a separate rejected-claims section.

## Topic scorecard

`dimension | score (0–4 or UNKNOWN) | reason | observed input/editorial judgment | unresolved gap`

Include total only when all dimensions are scored, hard-failure checks and the gate decision. A partial sum may be shown only as “known dimensions,” never a normalized PASS score.

## AV storyboard

`beat_id | start_s | end_s | timing_basis | audio/script span | claim_ids | visual action and purpose | primary_family | asset_ids | AI_visible | sound/transition`

Split at changes in AI visibility or dominant visual family to calculate duration shares. A shot can reference several claims or assets. All spoken script spans must map to a beat; all beats must resolve assets before final rendering.

## Asset ledger

`asset_id | beat_ids | family | creator | item URL or creation method | license/rights basis and evidence | attribution | restrictions | acquisition status | local file | fallback`

An original diagram records its data/source basis; a conceptual schematic records that it is illustrative. Generated assets record provider/model/prompt and actual output path only when generated. No API keys or tokens belong in the packet.

## Review report

`gate/check | artifact/version | PASS/REVISE/BLOCKED/NOT_RUN | evidence location | reasoning | repair and downstream invalidation`

Separate planned versus rendered visual review, estimated versus measured timing, and structural validation versus behavioral evaluation. Report a test as executed only when someone actually performed the listed procedure and saved the observations.
