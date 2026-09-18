from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
from dataclasses import asdict
from typing import Any

from .classifier import ClassifiedObservation, _author_hash, _infer_group


ALLOWED_HORIZONS = {
    "intraday",
    "1_5d",
    "6_20d",
    "21_60d",
    "longer",
    "unspecified",
}

ALLOWED_POSITIONS = {None, "long", "short", "flat", "unknown"}

ALLOWED_FLAGS = {
    "quoted_view",
    "conditional",
    "historical_only",
    "sarcasm_or_irony",
    "mixed_horizon",
    "low_information",
    "copied_news",
    "ambiguous_asset_reference",
    "explicit_position",
    "explicit_target",
}


CLASSIFICATION_INSTRUCTION = """
Classify the author's own lithium-carbonate market view.
Do not infer direction from facts alone.
Quoted third-party views are not the author's view unless explicitly endorsed.
Conditional future trades are not current positions.
Historical views are not current views.
Separate direction, conviction, and explicit position.
For mixed horizons, return multiple observations.
Return JSON only.
""".strip()


class ExternalClassifierError(RuntimeError):
    pass


def _clamp(value: Any, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


def _validate_result_row(row: dict[str, Any]) -> dict[str, Any]:
    direction = int(row.get("direction", 0))
    if direction not in {-2, -1, 0, 1, 2}:
        raise ExternalClassifierError("direction must be one of -2,-1,0,1,2")

    horizon = str(row.get("horizon", "unspecified"))
    if horizon not in ALLOWED_HORIZONS:
        raise ExternalClassifierError(f"unsupported horizon: {horizon}")

    position = row.get("disclosed_position")
    if position not in ALLOWED_POSITIONS:
        raise ExternalClassifierError(f"unsupported disclosed_position: {position}")

    flags = [str(item) for item in row.get("classification_flags", [])]
    unknown_flags = set(flags) - ALLOWED_FLAGS
    if unknown_flags:
        raise ExternalClassifierError(
            f"unsupported classification flags: {sorted(unknown_flags)}"
        )

    target_price = row.get("target_price")
    if target_price is not None:
        target_price = float(target_price)
        if not 30000 <= target_price <= 500000:
            target_price = None

    return {
        "direction": direction,
        "horizon": horizon,
        "classifier_confidence": _clamp(
            row.get("classifier_confidence", 0.5), 0.0, 1.0
        ),
        "conviction": _clamp(row.get("conviction", 0.5), 0.0, 1.0),
        "position_disclosed": bool(row.get("position_disclosed", False)),
        "disclosed_position": position,
        "reason_tags": [str(item) for item in row.get("reason_tags", ["unknown"])],
        "target_price": target_price,
        "classification_flags": sorted(set(flags)),
        "classification_evidence": (
            str(row["classification_evidence"])[:500]
            if row.get("classification_evidence") is not None
            else None
        ),
    }


class ExternalJSONClassifier:
    """Provider-agnostic LLM/ML classification adapter.

    The configured command receives one JSON object on stdin and must emit JSON:
      {"observations": [{...classification fields...}]}

    The adapter never sends repository credentials. It preserves source
    provenance locally and only accepts a bounded classification schema.
    """

    def __init__(self, command: str, *, timeout_seconds: int = 60) -> None:
        parsed = shlex.split(command)
        if not parsed:
            raise ValueError("classifier command must not be empty")
        self.command = parsed
        self.timeout_seconds = timeout_seconds

    def classify(
        self,
        record: dict[str, Any],
        *,
        asset_id: str,
        model_version: str,
    ) -> list[ClassifiedObservation]:
        text = str(record.get("text") or record.get("title") or "").strip()
        if not text:
            return []

        payload = {
            "task": "market_consensus_stance_classification",
            "asset_id": asset_id,
            "instruction": CLASSIFICATION_INSTRUCTION,
            "record": {
                "text": text,
                "title": record.get("title"),
                "content_type": record.get("content_type"),
                "platform": record.get("platform"),
                "published_at": record.get("published_at"),
                "query_category": record.get("query_category"),
                "search_term": record.get("query"),
            },
            "output_contract": {
                "direction": [-2, -1, 0, 1, 2],
                "horizon": sorted(ALLOWED_HORIZONS),
                "classifier_confidence": "[0,1]",
                "conviction": "[0,1]",
                "position_disclosed": "boolean",
                "disclosed_position": ["long", "short", "flat", "unknown", None],
                "reason_tags": "string[]",
                "target_price": "number|null",
                "classification_flags": sorted(ALLOWED_FLAGS),
                "classification_evidence": "string|null",
            },
        }

        proc = subprocess.run(
            self.command,
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        if proc.returncode != 0:
            raise ExternalClassifierError(
                f"classifier command failed with exit {proc.returncode}: "
                f"{proc.stderr[-500:]}"
            )

        try:
            output = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise ExternalClassifierError("classifier returned invalid JSON") from exc

        if isinstance(output, dict) and isinstance(output.get("observations"), list):
            result_rows = output["observations"]
        elif isinstance(output, list):
            result_rows = output
        elif isinstance(output, dict):
            result_rows = [output]
        else:
            raise ExternalClassifierError("classifier output must be object or array")

        platform = str(record.get("platform") or "unknown")
        author = str(record.get("author")) if record.get("author") else None
        source_group = _infer_group(record)
        published_at = str(record.get("published_at") or record.get("captured_at"))
        captured_at = str(record.get("captured_at") or published_at)
        raw_hash = str(
            record.get("raw_hash")
            or hashlib.sha256(text.encode("utf-8")).hexdigest()
        )

        observations: list[ClassifiedObservation] = []
        for index, raw_result in enumerate(result_rows):
            if not isinstance(raw_result, dict):
                raise ExternalClassifierError("each observation must be an object")
            result = _validate_result_row(raw_result)
            observation_id = hashlib.sha256(
                f"{raw_hash}\n{index}\n{result['direction']}\n{result['horizon']}".encode(
                    "utf-8"
                )
            ).hexdigest()

            observations.append(
                ClassifiedObservation(
                    observation_id=observation_id,
                    asset_id=asset_id,
                    captured_at=captured_at,
                    published_at=published_at,
                    platform=platform,
                    source_group=source_group,
                    source_id=(
                        str(record["source_id"])
                        if record.get("source_id") is not None
                        else None
                    ),
                    author_id_hash=_author_hash(author, platform),
                    author_display_name=author,
                    content_type=str(record.get("content_type") or "other"),
                    parent_source_id=(
                        str(record["parent_source_id"])
                        if record.get("parent_source_id") is not None
                        else None
                    ),
                    source_url=(
                        str(record["url"])
                        if record.get("url") is not None
                        else None
                    ),
                    raw_text=text,
                    direction=result["direction"],
                    horizon=result["horizon"],
                    classifier_confidence=result["classifier_confidence"],
                    conviction=result["conviction"],
                    position_disclosed=result["position_disclosed"],
                    disclosed_position=result["disclosed_position"],
                    reason_tags=result["reason_tags"],
                    target_price=result["target_price"],
                    narrative_ids=[],
                    uniqueness_factor=1.0,
                    source_weight=1.0,
                    raw_hash=raw_hash,
                    classification_flags=result["classification_flags"],
                    classification_evidence=result["classification_evidence"],
                    discovery_lane=record.get("discovery_lane"),
                    search_term=record.get("query"),
                    engagement=dict(record.get("raw", {}).get("engagement") or {}),
                    provenance={
                        "tool": "ExternalJSONClassifier",
                        "model_version": model_version,
                        "retrieval_run_id": None,
                        "classification_run_id": None,
                    },
                )
            )

        return observations
