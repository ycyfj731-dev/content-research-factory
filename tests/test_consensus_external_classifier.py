import json
import sys

from content_research_factory.consensus.classifier import HeuristicLCClassifier
from content_research_factory.consensus.external_classifier import ExternalJSONClassifier


def base_record(**overrides):
    row = {
        "captured_at": "2026-09-18T12:00:00+00:00",
        "published_at": "2026-09-18T11:00:00+00:00",
        "platform": "weibo",
        "source_id": "s1",
        "author": "tester",
        "content_type": "post",
        "text": "我看空碳酸锂",
        "raw_hash": "hash-1",
        "origin_tool": "Agent-Reach",
    }
    row.update(overrides)
    return row


def test_external_json_classifier_accepts_strict_json_protocol(tmp_path):
    script = tmp_path / "classifier.py"
    script.write_text(
        """
import json, sys
payload = json.loads(sys.stdin.read())
print(json.dumps({
  "observations": [{
    "direction": -1,
    "horizon": "1_5d",
    "classifier_confidence": 0.93,
    "conviction": 0.8,
    "position_disclosed": True,
    "disclosed_position": "short",
    "reason_tags": ["production_growth"],
    "target_price": 110000,
    "classification_flags": ["explicit_position", "explicit_target"],
    "classification_evidence": "明确看空并持有空单"
  }]
}, ensure_ascii=False))
""".strip(),
        encoding="utf-8",
    )

    classifier = ExternalJSONClassifier(
        f"{sys.executable} {script}",
        timeout_seconds=10,
    )
    result = classifier.classify(
        base_record(),
        asset_id="GFEX_LC",
        model_version="fake-model",
    )

    assert len(result) == 1
    item = result[0]
    assert item.direction == -1
    assert item.disclosed_position == "short"
    assert item.position_disclosed is True
    assert item.target_price == 110000
    assert item.provenance["tool"] == "ExternalJSONClassifier"
    assert item.provenance["model_version"] == "fake-model"


def test_unix_millisecond_timestamp_is_normalized():
    classifier = HeuristicLCClassifier()
    item = classifier.classify(
        base_record(
            published_at=1789732800000,
            text="我继续看空2701",
        ),
        asset_id="GFEX_LC",
        model_version="test",
    )[0]

    assert "T" in item.published_at
    assert item.published_at.endswith("+00:00")


def test_trendradar_news_is_not_automatically_institution():
    classifier = HeuristicLCClassifier()
    item = classifier.classify(
        base_record(
            platform=None,
            origin_tool="TrendRadar",
            text="我继续看空2701",
        ),
        asset_id="GFEX_LC",
        model_version="test",
    )[0]

    assert item.source_group == "kol"
