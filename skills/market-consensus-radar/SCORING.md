# MARKET-CONSENSUS-RADAR scoring v0.1

## 1. Observation direction

Each observation has:

`direction ∈ {-2,-1,0,+1,+2}`

Normalize:

`x = direction / 2`

Therefore:

- strong bearish = -1.0
- bearish = -0.5
- neutral = 0
- bullish = +0.5
- strong bullish = +1.0

## 2. Effective observation weight

For observation i:

`w_i = source_weight × classifier_confidence × conviction_factor × freshness × uniqueness_factor × position_factor`

Where:

### source_weight

Stable panel weight from config. V0.1 defaults to 1.0 unless explicitly configured.

### classifier_confidence

Range [0,1].

Low-confidence model classifications contribute less.

### conviction_factor

`0.25 + 0.75 × conviction`

This prevents a valid low-conviction observation from receiving zero weight while still rewarding explicit certainty.

### freshness

`freshness = 0.5 ^ (age_days / half_life_days)`

Half-life depends on the stated horizon.

Default LC half-lives:

- intraday: 0.5 day
- 1-5d: 2 days
- 6-20d: 7 days
- 21-60d: 21 days
- longer: 60 days
- unspecified: 7 days

### uniqueness_factor

Range [0,1].

- original independent analysis ≈ 1.0
- close paraphrase / derivative ≈ 0.3-0.6
- near-copy / repost ≈ 0.05-0.2

### position_factor

Default:

- explicit disclosed long/short consistent with the stated direction: 1.25
- otherwise: 1.0

This is capped. "满仓" language does not create unlimited weight.

## 3. Group directional score

Compute Institution, KOL, and Crowd separately.

For one group:

`m = Σ(w_i × x_i) / Σ(w_i)`

Then:

`group_score = 50 × (1 + m)`

Range: [0,100].

## 4. Overall consensus score

Do not pool all raw observations.

First calculate group scores, then combine available groups:

`overall = Σ(group_weight_g × group_score_g) / Σ(group_weight_g for available groups)`

Default LC group weights:

- institution: 0.45
- kol: 0.30
- crowd: 0.25

If one group is missing, renormalize only across available groups and emit a coverage warning.

## 5. Crowding score

Crowding is direction-agnostic.

Let:

`one_sidedness = |Σ(w_i × x_i) / Σ(w_i)|`

`participation = Σ(w_i × |x_i|) / Σ(w_i)`

Then:

`crowding = 100 × sqrt(one_sidedness × participation)`

Properties:

- all strong bulls => 100
- all strong bears => 100
- equal strong bulls and bears => 0
- mostly neutral content => low crowding

This is intentionally not a contrarian signal by itself.

## 6. Effective sample size

Raw comment count is misleading when a few sources dominate.

Use Kish effective sample size:

`N_eff = (Σw_i)^2 / Σ(w_i^2)`

Always report:

- raw sample count
- unique-author count
- effective sample size

## 7. Narrative saturation

V0.1 schema reserves narrative saturation but does not yet implement the clustering engine.

Intended concept for narrative n:

- independent originators
- unique spreaders
- cross-group adoption
- share of active authors discussing the narrative
- freshness

Do not estimate saturation from duplicate post count alone.

## 8. Historical-accuracy weighting

Not enabled in V0.1.

Reason: naive "accuracy weight" can introduce look-ahead leakage and reward permanently bullish/bearish accounts during one regime.

When added, accuracy must be computed only from information available before the scoring date and must be bounded.

## 9. Divergence

Consensus is not a trading instruction.

A future divergence engine may compare consensus with market/fundamental reality.

For example:

- extreme bearish consensus
- positive basis
- falling warehouse receipts
- falling social inventory

may be labeled `BEARISH_CONSENSUS_BULLISH_REALITY`.

The label describes a state. It does not guarantee reversal.
