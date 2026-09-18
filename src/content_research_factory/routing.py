from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import yaml


EXPECTED_ROUTING = {
    "trend_discovery": ("TrendRadar", "热点发现"),
    "cross_platform_verification": ("Agent-Reach", "跨平台验证"),
    "chinese_social_deep_research": ("MediaCrawler", "中文社媒深抓和评论"),
    "video_production": ("MoneyPrinterTurbo", "视频生产"),
}


@dataclass(frozen=True)
class Route:
    stage: str
    tool: str
    responsibility: str


def load_routing(path: str | Path) -> dict[str, Route]:
    config_path = Path(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    routes = {
        stage: Route(
            stage=stage,
            tool=value["tool"],
            responsibility=value["responsibility"],
        )
        for stage, value in raw["routing"].items()
    }
    validate_fixed_routing(routes)
    return routes


def validate_fixed_routing(routes: Mapping[str, Route]) -> None:
    for stage, (expected_tool, expected_responsibility) in EXPECTED_ROUTING.items():
        if stage not in routes:
            raise ValueError(f"Missing required route: {stage}")
        route = routes[stage]
        if route.tool != expected_tool:
            raise ValueError(
                f"{stage} must use {expected_tool}, got {route.tool}"
            )
        if route.responsibility != expected_responsibility:
            raise ValueError(
                f"{stage} responsibility must be {expected_responsibility}, "
                f"got {route.responsibility}"
            )
