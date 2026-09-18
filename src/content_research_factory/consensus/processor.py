from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .classifier import HeuristicLCClassifier, classify_records
from .narratives import cluster_observations, narrative_summary


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
) -> dict[str, Any]:
    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    asset_id = str(config["asset"]["id"])
    raw_rows = read_jsonl(input_path)

    classifier = HeuristicLCClassifier()
    classified = classify_records(
        raw_rows,
        classifier=classifier,
        asset_id=asset_id,
        model_version=model_version,
    )

    clustered, clusters = cluster_observations(
        classified,
        similarity_threshold=similarity_threshold,
    )
    narratives = narrative_summary(clustered, clusters)

    output = {
        "asset_id": asset_id,
        "model_version": model_version,
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
                "narratives": narratives,
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
    }
