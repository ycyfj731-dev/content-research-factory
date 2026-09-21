# MARKET-CONSENSUS-RADAR classification contract v0.1

## Objective

Convert raw public evidence into structured directional observations without inventing stance.

Classification must distinguish:

- the author's own market view;
- quoted/reported third-party views;
- conditional scenarios;
- factual news without a directional opinion;
- explicit positions;
- irony/sarcasm;
- historical statements.

## Primary output

Each eligible observation maps to the fields in:

`schemas/consensus_observation.schema.json`

Key fields:

- direction: -2, -1, 0, +1, +2
- horizon
- classifier_confidence
- conviction
- position_disclosed
- disclosed_position
- reason_tags
- target_price
- narrative_ids
- classification_flags

## Hard rules

### 1. Do not infer stance from facts alone

Examples:

"9月碳酸锂排产增加10%"

This is factual information. Direction = 0 unless the author explicitly connects it to a price view.

"9月排产增加10%，所以我继续看空2701"

Direction = bearish.

### 2. Quoted views are not automatically the author's view

"某期货公司认为碳酸锂将跌到11万"

If the post merely reports this, classify the post author's direction as neutral and flag `quoted_view`.

If the author says "我同意，11万见", classify bearish.

### 3. Conditional plans are not current positions

"跌破12万我就做空"

This is a conditional bearish plan, not an explicit current short.

- direction may be bearish if the sentence expresses a directional expectation;
- position_disclosed = false unless the author says the short is already open;
- flag `conditional`.

### 4. Position disclosure must be explicit

Valid examples:

- "我已经加多"
- "空单还在"
- "今天平空了"
- "多单止损"

Do not infer position from emotional language alone.

### 5. Separate conviction from strength

"我偏多，但也可能震荡"

May be direction +1 with low conviction.

"15万以下都是送钱，闭眼多"

May be direction +2 with high conviction.

### 6. Horizon should follow the author's own time frame

Examples:

- "今天看反弹" -> intraday
- "这周偏多" -> 1_5d
- "国庆后会累库" -> 6_20d or 21_60d depending on date
- no stated horizon -> unspecified

Do not infer long horizon just because a fundamental reason is long term.

### 7. Historical claims are not current views

"去年这个位置我就看多"

Direction = 0 unless the author also expresses a current view.

Flag `historical_only`.

### 8. Sarcasm and irony require caution

"对对对，矿一到港就直接跌到5万了（笑）"

Do not classify from surface keywords alone.

If sarcasm is likely but the intended direction is uncertain:

- direction = 0
- lower classifier_confidence
- flag `sarcasm_or_irony`.

### 9. Mixed/hedged views

"短期可能反弹，但中期仍看空"

This should produce two observations if the pipeline supports multi-horizon extraction:

- short-term bullish
- medium-term bearish

Do not force a single blended direction when horizons conflict.

### 10. Comments that only cheer/taunt are directional only when clearly market-referential

"涨！"
under an LC post can be bullish but low-information.

"空狗今晚睡不着了"
can be bullish sentiment but should carry lower source/conviction quality than an explicit price thesis.

## Classification flags

Allowed flags include:

- quoted_view
- conditional
- historical_only
- sarcasm_or_irony
- mixed_horizon
- low_information
- copied_news
- ambiguous_asset_reference
- explicit_position
- explicit_target

## Reason tags

Reason tags should describe the stated argument, not model inference.

LC examples:

- production_growth
- production_cut
- zimbabwe_supply
- jiangxi_restart
- warehouse_receipt_decline
- warehouse_receipt_growth
- social_inventory_draw
- social_inventory_build
- spot_strength
- spot_weakness
- basis_strength
- basis_weakness
- holiday_restocking
- demand_strength
- demand_weakness
- policy
- technical
- positioning
- squeeze
- valuation
- unknown

## Confidence

Classifier confidence reflects confidence in the **classification**, not confidence in the market call.

Examples:

- clear "我已经做空2701，目标11万" -> high classifier_confidence
- ambiguous meme or irony -> low classifier_confidence

## Multi-observation rule

One post may emit more than one observation only when it clearly contains different horizons or explicitly distinct instruments/contracts.

Each emitted observation must retain the same raw source provenance.

## No hindsight

Classification must use only the text and context available at capture time.

Never alter direction after observing subsequent price action.
