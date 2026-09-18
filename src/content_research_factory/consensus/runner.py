from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .scoring import ConsensusObservation, build_daily_scores


def _parse_datetime(value: str) -> datetime:
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"datetime must include timezone: {value}")
    return parsed


def observation_from_mapping(row: dict[str, Any]) -> ConsensusObservation:
    return ConsensusObservation(
        source_group=str(row["source_group"]),
        direction=int(row["direction"]),
        published_at=_parse_datetime(str(row["published_at"])),
        horizon=str(row.get("horizon", "unspecified")),
        source_weight=float(row.get("source_weight", 1.0)),
        classifier_confidence=float(row.get("classifier_confidence", 1.0)),
        conviction=float(row.get("conviction", 0.5)),
        uniqueness_factor=float(row.get("uniqueness_factor", 1.0)),
        position_disclosed=bool(row.get("position_disclosed", False)),
        disclosed_position=row.get("disclosed_position"),
        author_id_hash=row.get("author_id_hash"),
    )


def score_observation_file(
    input_path: str | Path,
    *,
    config_path: str | Path,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")

    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        rows = payload.get("observations")
    else:
        rows = payload
    if not isinstance(rows, list):
        raise ValueError("input must be a JSON array or an object with an observations array")

    config = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    observations = [observation_from_mapping(dict(row)) for row in rows]

    group_weights = {
        name: float(settings["overall_weight"])
        for name, settings in config["source_groups"].items()
    }
    half_lives = {
        str(name): float(value)
        for name, value in config["freshness_half_life_days"].items()
    }
    weighting = config.get("weighting", {})

    scores = build_daily_scores(
        observations,
        now=now,
        group_weights=group_weights,
        half_life_days=half_lives,
        explicit_position_factor=float(weighting.get("explicit_position_factor", 1.25)),
        conviction_floor=float(weighting.get("conviction_floor", 0.25)),
        conviction_scale=float(weighting.get("conviction_scale", 0.75)),
    )

    return {
        "asset_id": config["asset"]["id"],
        "scored_at": now.isoformat(),
        "group_scores": scores.group_scores,
        "overall_consensus_score": scores.overall_consensus_score,
        "crowding_score": scores.crowding_score,
        "sample_sizes": {
            "raw": scores.raw_sample_size,
            "unique_authors": scores.unique_author_count,
            "effective": scores.effective_sample_size,
        },
    }
