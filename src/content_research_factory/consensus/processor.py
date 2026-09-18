from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .classifier import HeuristicLCClassifier, classify_records
from .external_classifier import ExternalJSONClassifier
from .narratives import cluster_observations, narrative_summary
from .semantic import BERTopicEngine, SentenceTransformerSimilarity


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            rows.append(value)
    return rows


def process_raw_evidence(
    input_path: str | Path,
    *,
    config_path: str | Path,
    output_path: str | Path,
    narratives_path: str | Path | None = None,
    model_version: str = "heuristic-lc-v0.1",
    similarity_threshold: float = 0.52,
    classifier_command: str | None = None,
    classifier_timeout_seconds: int = 60,
    semantic_model: str | None = None,
    semantic_threshold: float = 0.72,
    enable_bertopic: bool = False,
) -> dict[str, Any]:
    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    asset_id = str(config["asset"]["id"])
    raw_rows = read_jsonl(input_path)

    classifier = (
        ExternalJSONClassifier(
            classifier_command,
            timeout_seconds=classifier_timeout_seconds,
        )
        if classifier_command
        else HeuristicLCClassifier()
    )
    classified = classify_records(
        raw_rows,
        classifier=classifier,
        asset_id=asset_id,
        model_version=model_version,
    )

    semantic_matrix = None
    semantic_mode = "lexical"
    if semantic_model and classified:
        engine = SentenceTransformerSimilarity(semantic_model)
        semantic_matrix = engine.similarity_matrix(
            [str(row.get("raw_text") or "") for row in classified]
        )
        semantic_mode = semantic_model

    clustered, clusters = cluster_observations(
        classified,
        similarity_threshold=similarity_threshold,
        semantic_matrix=semantic_matrix,
        semantic_threshold=semantic_threshold,
    )
    narratives = narrative_summary(clustered, clusters)

    discovered_topics: dict[str, Any] | None = None
    if enable_bertopic and classified:
        topic_result = BERTopicEngine(language="multilingual").fit(
            [str(row.get("raw_text") or "") for row in classified]
        )
        discovered_topics = {
            "labels": topic_result.labels,
            "probabilities": topic_result.probabilities,
            "topic_info": topic_result.topic_info,
        }

    output = {
        "asset_id": asset_id,
        "model_version": model_version,
        "classifier_mode": "external_json" if classifier_command else "heuristic",
        "input_record_count": len(raw_rows),
        "observation_count": len(clustered),
        "observations": clustered,
    }

    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    narrative_target = (
        Path(narratives_path)
        if narratives_path is not None
        else target.with_name(target.stem + ".narratives.json")
    )
    narrative_target.parent.mkdir(parents=True, exist_ok=True)
    narrative_target.write_text(
        json.dumps(
            {
                "asset_id": asset_id,
                "semantic_mode": semantic_mode,
                "narratives": narratives,
                "discovered_topics": discovered_topics,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    return {
        "input": str(input_path),
        "output": str(target),
        "narratives_output": str(narrative_target),
        "raw_records": len(raw_rows),
        "observations": len(clustered),
        "narratives": len(narratives),
        "semantic_mode": semantic_mode,
        "bertopic_enabled": enable_bertopic,
    }
