from __future__ import annotations

import hashlib
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable


SEED_NARRATIVES: dict[str, tuple[str, ...]] = {
    "zimbabwe_supply": ("津巴布韦", "津巴矿", "到港"),
    "jiangxi_restart": ("宜春", "江西", "枧下窝", "复产"),
    "warehouse_receipts": ("仓单", "注销", "注册"),
    "holiday_restocking": ("节前补库", "国庆补库", "补库"),
    "social_inventory": ("社会库存", "贸易库存", "去库", "累库"),
    "spot_futures_basis": ("现货", "期货", "基差", "升水", "贴水"),
    "production_growth": ("排产", "增产", "产量"),
    "deliverable_supply_squeeze": ("逼仓", "挤仓", "逼空", "可交割"),
}


@dataclass(frozen=True)
class NarrativeCluster:
    narrative_id: str
    label: str
    member_indices: list[int]
    representative_text: str
    unique_authors: int
    source_groups: list[str]


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[@#￥$%^&*_+=<>《》【】\[\]{}()（）,，。.!！?？:：;；'\"“”‘’/\\|-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _char_ngrams(text: str, n: int = 3) -> set[str]:
    compact = re.sub(r"\s+", "", _normalize(text))
    if len(compact) < n:
        return {compact} if compact else set()
    return {compact[i : i + n] for i in range(len(compact) - n + 1)}


def jaccard_similarity(a: str, b: str) -> float:
    aa = _char_ngrams(a)
    bb = _char_ngrams(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def _seed_label(text: str) -> str | None:
    scores = {
        key: sum(1 for term in terms if term in text)
        for key, terms in SEED_NARRATIVES.items()
    }
    key, score = max(scores.items(), key=lambda item: item[1])
    return key if score > 0 else None


def cluster_observations(
    observations: Iterable[dict[str, Any]],
    *,
    similarity_threshold: float = 0.52,
    semantic_matrix: list[list[float]] | None = None,
    semantic_threshold: float = 0.72,
) -> tuple[list[dict[str, Any]], list[NarrativeCluster]]:
    rows = [dict(row) for row in observations]
    clusters: list[list[int]] = []
    representatives: list[str] = []
    representative_indices: list[int] = []

    for index, row in enumerate(rows):
        text = str(row.get("raw_text") or "")
        seed = _seed_label(text)

        best_cluster: int | None = None
        best_score = 0.0
        best_qualifies = False
        for cluster_index, representative in enumerate(representatives):
            rep_seed = _seed_label(representative)
            lexical = jaccard_similarity(text, representative)
            seed_bonus = 0.35 if seed and rep_seed and seed == rep_seed else 0.0
            lexical_score = min(1.0, lexical + seed_bonus)

            semantic_score = 0.0
            if semantic_matrix is not None:
                rep_index = representative_indices[cluster_index]
                try:
                    semantic_score = float(semantic_matrix[index][rep_index])
                except (IndexError, TypeError, ValueError):
                    semantic_score = 0.0

            qualifies = (
                lexical_score >= similarity_threshold
                or (
                    semantic_matrix is not None
                    and semantic_score >= semantic_threshold
                )
            )
            score = max(lexical_score, semantic_score)
            if score > best_score:
                best_score = score
                best_cluster = cluster_index
                best_qualifies = qualifies

        if best_cluster is not None and best_qualifies:
            clusters[best_cluster].append(index)
            # Keep the longer text as a more informative representative.
            current = representatives[best_cluster]
            if len(text) > len(current):
                representatives[best_cluster] = text
                representative_indices[best_cluster] = index
        else:
            clusters.append([index])
            representatives.append(text)
            representative_indices.append(index)

    cluster_objects: list[NarrativeCluster] = []

    for cluster_index, members in enumerate(clusters):
        representative = representatives[cluster_index]
        seed = _seed_label(representative)
        narrative_id = seed or (
            "narrative_" + hashlib.sha256(
                _normalize(representative).encode("utf-8")
            ).hexdigest()[:12]
        )
        authors = {
            rows[i].get("author_id_hash")
            for i in members
            if rows[i].get("author_id_hash")
        }
        groups = sorted(
            {
                str(rows[i].get("source_group"))
                for i in members
                if rows[i].get("source_group")
            }
        )

        # Discount replicated narratives. Independent authors and cross-group
        # adoption raise uniqueness, while many copies of one narrative lower it.
        independent = max(1, len(authors))
        group_bonus = 1.0 + 0.15 * max(0, len(groups) - 1)
        cluster_size = len(members)
        base_uniqueness = min(
            1.0,
            group_bonus * math.sqrt(independent / max(1, cluster_size)),
        )

        for position, member_index in enumerate(members):
            row = rows[member_index]
            row["narrative_ids"] = sorted(
                set([*row.get("narrative_ids", []), narrative_id])
            )
            # First/independent source retains more weight than later copies.
            copy_decay = 1.0 / math.sqrt(position + 1)
            row["uniqueness_factor"] = max(
                0.05,
                min(
                    float(row.get("uniqueness_factor", 1.0)),
                    base_uniqueness * copy_decay,
                ),
            )

        cluster_objects.append(
            NarrativeCluster(
                narrative_id=narrative_id,
                label=seed or representative[:80],
                member_indices=list(members),
                representative_text=representative,
                unique_authors=len(authors),
                source_groups=groups,
            )
        )

    return rows, cluster_objects


def narrative_summary(
    observations: Iterable[dict[str, Any]],
    clusters: Iterable[NarrativeCluster],
) -> list[dict[str, Any]]:
    rows = list(observations)
    output: list[dict[str, Any]] = []
    total_authors = {
        row.get("author_id_hash")
        for row in rows
        if row.get("author_id_hash")
    }

    for cluster in clusters:
        members = [rows[i] for i in cluster.member_indices]
        directional = [
            float(row.get("direction", 0)) / 2.0
            for row in members
        ]
        direction = sum(directional) / len(directional) if directional else 0.0

        # Saturation is a transparent V0.1 proxy using author share, cross-group
        # adoption, and raw member share. It is not yet embedding-based.
        author_share = (
            cluster.unique_authors / len(total_authors)
            if total_authors
            else 0.0
        )
        member_share = len(members) / max(1, len(rows))
        group_share = len(cluster.source_groups) / 3.0
        saturation = 100.0 * min(
            1.0,
            0.45 * author_share + 0.35 * member_share + 0.20 * group_share,
        )

        output.append(
            {
                "narrative_id": cluster.narrative_id,
                "label": cluster.label,
                "direction": direction,
                "saturation": saturation,
                "unique_originators": cluster.unique_authors,
                "unique_spreaders": len(members),
            }
        )

    output.sort(key=lambda row: row["saturation"], reverse=True)
    return output
