from content_research_factory.consensus.classifier import HeuristicLCClassifier


CLASSIFIER = HeuristicLCClassifier()


def classify(text, **overrides):
    row = {
        "captured_at": "2026-09-18T12:00:00+00:00",
        "published_at": "2026-09-18T11:00:00+00:00",
        "platform": "weibo",
        "source_id": "s1",
        "author": "tester",
        "content_type": "post",
        "text": text,
        "raw_hash": "hash-1",
        "origin_tool": "Agent-Reach",
    }
    row.update(overrides)
    return CLASSIFIER.classify(
        row,
        asset_id="GFEX_LC",
        model_version="test",
    )[0]


def test_factual_supply_news_is_neutral():
    result = classify("9月碳酸锂排产增加10%，津巴布韦锂矿陆续到港")
    assert result.direction == 0
    assert "production_growth" in result.reason_tags
    assert "zimbabwe_supply" in result.reason_tags


def test_explicit_bearish_view_is_classified_bearish():
    result = classify("9月排产增加10%，所以我继续看空2701")
    assert result.direction < 0


def test_reported_third_party_view_is_not_authors_own_view():
    result = classify("某期货公司认为碳酸锂会跌到11万")
    assert result.direction == 0
    assert "quoted_view" in result.classification_flags
    assert result.target_price == 110000


def test_conditional_short_plan_is_not_current_position():
    result = classify("如果跌破12万我就做空")
    assert result.direction < 0
    assert "conditional" in result.classification_flags
    assert result.position_disclosed is False


def test_explicit_short_position_is_preserved():
    result = classify("我已经加空，11万见")
    assert result.direction < 0
    assert result.position_disclosed is True
    assert result.disclosed_position == "short"
    assert "explicit_position" in result.classification_flags
    assert result.target_price == 110000


def test_historical_view_does_not_become_current_view():
    result = classify("去年这个位置我就看多")
    assert result.direction == 0
    assert "historical_only" in result.classification_flags


def test_sarcasm_is_neutralized_without_explicit_position():
    result = classify("对对对，矿一到港就直接跌到5万了（笑）")
    assert result.direction == 0
    assert "sarcasm_or_irony" in result.classification_flags


def test_comment_source_defaults_to_crowd():
    result = classify("涨", content_type="comment", platform="xhs")
    assert result.source_group == "crowd"
    assert result.direction > 0
    assert "low_information" in result.classification_flags
