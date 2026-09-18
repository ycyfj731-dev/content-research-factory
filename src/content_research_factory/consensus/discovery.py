from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class DiscoveryQuery:
    query: str
    category: str
    priority: int
    lane: str = "web_wide"


def _dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = " ".join(value.split()).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def build_discovery_plan(
    config_path: str | Path,
    *,
    dynamic_terms: list[str] | None = None,
) -> list[DiscoveryQuery]:
    config: dict[str, Any] = yaml.safe_load(
        Path(config_path).read_text(encoding="utf-8")
    )
    discovery = config["discovery"]

    queries: list[DiscoveryQuery] = []

    # Tier 1: explicit asset/core queries. These are stable through time.
    for query in discovery.get("core_keywords", []):
        queries.append(
            DiscoveryQuery(
                query=str(query),
                category="core",
                priority=1,
            )
        )

    # Tier 2: systematic query families. The asset anchor prevents generic
    # terms such as "库存" or "反弹" from becoming unrelated full-web searches.
    anchor = str(config["asset"]["name"])
    for category, terms in discovery.get("query_families", {}).items():
        for term in terms:
            queries.append(
                DiscoveryQuery(
                    query=f"{anchor} {term}",
                    category=str(category),
                    priority=2,
                )
            )

    # Tier 3: same-day terms discovered by TrendRadar / Agent-Reach.
    for term in dynamic_terms or []:
        queries.append(
            DiscoveryQuery(
                query=f"{anchor} {term}",
                category="dynamic",
                priority=3,
            )
        )

    unique = _dedupe_keep_order([item.query for item in queries])
    by_query = {item.query: item for item in queries}
    return [by_query[query] for query in unique]


def plan_as_dicts(plan: list[DiscoveryQuery]) -> list[dict[str, Any]]:
    return [
        {
            "query": item.query,
            "category": item.category,
            "priority": item.priority,
            "lane": item.lane,
        }
        for item in plan
    ]
