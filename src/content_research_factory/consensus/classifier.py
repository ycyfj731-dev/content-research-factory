from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Protocol


BULLISH_PATTERNS = (
    r"看多",
    r"偏多",
    r"继续多",
    r"做多",
    r"加多",
    r"多单",
    r"买多",
    r"反弹",
    r"上涨",
    r"走强",
    r"突破",
    r"逼空",
    r"挤空",
    r"空头要小心",
    r"空头.*难受",
)

BEARISH_PATTERNS = (
    r"看空",
    r"偏空",
    r"继续空",
    r"做空",
    r"加空",
    r"空单",
    r"卖空",
    r"下跌",
    r"走弱",
    r"跌破",
    r"补跌",
    r"过剩",
    r"多头要小心",
    r"多头.*难受",
)

STRONG_BULLISH_PATTERNS = (
    r"闭眼多",
    r"必涨",
    r"肯定涨",
    r"一定涨",
    r"涨停",
    r"满仓多",
    r"重仓多",
)

STRONG_BEARISH_PATTERNS = (
    r"闭眼空",
    r"必跌",
    r"肯定跌",
    r"一定跌",
    r"跌停",
    r"满仓空",
    r"重仓空",
)

LONG_POSITION_PATTERNS = (
    r"已经.*(?:做多|加多|买多)",
    r"多单.*(?:还在|持有|继续|加仓)",
    r"(?:持有|拿着).*多单",
    r"满仓多",
    r"重仓多",
)

SHORT_POSITION_PATTERNS = (
    r"已经.*(?:做空|加空|卖空)",
    r"空单.*(?:还在|持有|继续|加仓)",
    r"(?:持有|拿着).*空单",
    r"满仓空",
    r"重仓空",
)

CONDITIONAL_PATTERNS = (
    r"如果",
    r"若",
    r"一旦",
    r"只要",
    r"等.*再",
)

HISTORICAL_PATTERNS = (
    r"去年",
    r"上次",
    r"之前",
    r"当时",
    r"曾经",
)

SARCASTIC_MARKERS = (
    "呵呵",
    "笑死",
    "（笑）",
    "(笑)",
    "对对对",
    "可太",
)

QUOTE_PATTERNS = (
    r".{1,20}(?:认为|表示|指出|预计|称).*?(?:上涨|下跌|看多|看空|偏多|偏空)",
)

INTRADAY_TERMS = ("今天", "日内", "尾盘", "今晚", "上午", "下午")
SHORT_TERMS = ("这周", "本周", "几天", "短期", "节前")
MEDIUM_TERMS = ("下周", "国庆后", "月底", "10月", "十一后", "一个月")
LONG_TERMS = ("年底", "四季度", "明年", "中长期", "长期")


@dataclass(frozen=True)
class ClassifiedObservation:
    observation_id: str
    asset_id: str
    captured_at: str
    published_at: str
    platform: str
    source_group: str
    source_id: str | None
    author_id_hash: str | None
    author_display_name: str | None
    content_type: str
    parent_source_id: str | None
    source_url: str | None
    raw_text: str
    direction: int
    horizon: str
    classifier_confidence: float
    conviction: float
    position_disclosed: bool
    disclosed_position: str | None
    reason_tags: list[str]
    target_price: float | None
    narrative_ids: list[str]
    uniqueness_factor: float
    source_weight: float
    raw_hash: str
    classification_flags: list[str]
    classification_evidence: str | None
    discovery_lane: str | None
    search_term: str | None
    engagement: dict[str, Any]
    provenance: dict[str, Any]


class ObservationClassifier(Protocol):
    def classify(
        self,
        record: dict[str, Any],
        *,
        asset_id: str,
        model_version: str,
    ) -> list[ClassifiedObservation]:
        ...


def _has(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _count(patterns: Iterable[str], text: str) -> int:
    return sum(
        len(re.findall(pattern, text, flags=re.IGNORECASE))
        for pattern in patterns
    )


def _author_hash(author: str | None, platform: str) -> str | None:
    if not author:
        return None
    return hashlib.sha256(f"{platform}\n{author}".encode("utf-8")).hexdigest()


def _infer_group(record: dict[str, Any]) -> str:
    explicit = record.get("source_group")
    if explicit in {"institution", "kol", "crowd"}:
        return str(explicit)
    if record.get("content_type") in {"comment", "reply"}:
        return "crowd"
    platform = str(record.get("platform") or "")
    if platform in {"institution_web", "research", "broker"}:
        return "institution"
    origin_tool = str(record.get("origin_tool") or "")
    if origin_tool == "TrendRadar" and not platform:
        return "institution"
    return "kol"


def _infer_horizon(text: str) -> str:
    if any(term in text for term in INTRADAY_TERMS):
        return "intraday"
    if any(term in text for term in SHORT_TERMS):
        return "1_5d"
    if any(term in text for term in MEDIUM_TERMS):
        return "6_20d"
    if any(term in text for term in LONG_TERMS):
        return "21_60d"
    return "unspecified"


def _extract_target_price(text: str) -> float | None:
    candidates = re.findall(
        r"(?<!\d)(\d{1,2}(?:\.\d+)?)\s*万(?:元)?(?:/吨)?",
        text,
    )
    if candidates:
        value = float(candidates[-1]) * 10000.0
        if 30000 <= value <= 500000:
            return value

    candidates = re.findall(
        r"(?<!\d)(\d{5,6})(?!\d)",
        text,
    )
    if candidates:
        value = float(candidates[-1])
        if 30000 <= value <= 500000:
            return value
    return None


def _reason_tags(text: str) -> list[str]:
    mapping: tuple[tuple[str, tuple[str, ...]], ...] = (
        ("production_growth", ("增产", "排产增加", "产量增加")),
        ("production_cut", ("减产", "停产", "检修")),
        ("zimbabwe_supply", ("津巴布韦", "津巴矿")),
        ("jiangxi_restart", ("宜春复产", "江西复产", "枧下窝")),
        ("warehouse_receipt_decline", ("仓单注销", "仓单减少", "仓单下降")),
        ("warehouse_receipt_growth", ("仓单增加", "仓单注册", "新增仓单")),
        ("social_inventory_draw", ("去库", "库存下降", "库存减少")),
        ("social_inventory_build", ("累库", "库存增加")),
        ("spot_strength", ("现货上涨", "现货坚挺", "现货强")),
        ("spot_weakness", ("现货下跌", "现货弱")),
        ("basis_strength", ("基差扩大", "基差走强", "升水扩大")),
        ("basis_weakness", ("基差收窄", "基差走弱")),
        ("holiday_restocking", ("节前补库", "国庆补库", "补库")),
        ("demand_strength", ("需求强", "需求好", "旺季")),
        ("demand_weakness", ("需求弱", "需求差", "淡季")),
        ("squeeze", ("逼仓", "挤仓", "逼空", "挤空")),
        ("technical", ("破位", "均线", "支撑", "压力位", "技术面")),
        ("positioning", ("持仓", "增仓", "减仓", "多空")),
    )
    tags = [
        tag
        for tag, terms in mapping
        if any(term in text for term in terms)
    ]
    return tags or ["unknown"]


class HeuristicLCClassifier:
    """Deterministic baseline classifier.

    This is intentionally conservative. It is designed to produce a reproducible
    first-pass dataset and to provide a fallback when an LLM classifier is
    unavailable. Ambiguous/quoted/sarcastic text is down-weighted or neutralized.
    """

    def classify(
        self,
        record: dict[str, Any],
        *,
        asset_id: str,
        model_version: str = "heuristic-lc-v0.1",
    ) -> list[ClassifiedObservation]:
        text = str(record.get("text") or record.get("title") or "").strip()
        if not text:
            return []

        flags: list[str] = []
        conditional = _has(CONDITIONAL_PATTERNS, text)
        historical = _has(HISTORICAL_PATTERNS, text)
        sarcastic = any(marker in text for marker in SARCASTIC_MARKERS)
        quoted = _has(QUOTE_PATTERNS, text)

        if conditional:
            flags.append("conditional")
        if historical:
            flags.append("historical_only")
        if sarcastic:
            flags.append("sarcasm_or_irony")
        if quoted:
            flags.append("quoted_view")

        long_position = _has(LONG_POSITION_PATTERNS, text)
        short_position = _has(SHORT_POSITION_PATTERNS, text)
        if long_position or short_position:
            flags.append("explicit_position")

        target_price = _extract_target_price(text)
        if target_price is not None:
            flags.append("explicit_target")

        bull = _count(BULLISH_PATTERNS, text)
        bear = _count(BEARISH_PATTERNS, text)
        strong_bull = _count(STRONG_BULLISH_PATTERNS, text)
        strong_bear = _count(STRONG_BEARISH_PATTERNS, text)

        # Explicit position is strong evidence of own stance.
        if long_position and not short_position:
            bull += 3
        if short_position and not long_position:
            bear += 3

        direction = 0
        if strong_bull > strong_bear and bull >= bear:
            direction = 2
        elif strong_bear > strong_bull and bear >= bull:
            direction = -2
        elif bull > bear:
            direction = 1
        elif bear > bull:
            direction = -1

        # Pure quoted/historical text is not the author's current directional view.
        if (quoted or historical) and not (long_position or short_position):
            direction = 0

        # Sarcasm without an explicit position is too fragile for deterministic parsing.
        if sarcastic and not (long_position or short_position):
            direction = 0

        confidence = 0.86 if direction != 0 else 0.72
        if conditional:
            confidence *= 0.86
        if quoted or historical:
            confidence *= 0.78
        if sarcastic:
            confidence *= 0.55
        if len(text) < 8:
            flags.append("low_information")
            confidence *= 0.75

        conviction = 0.35
        if direction != 0:
            conviction = 0.55
        if abs(direction) == 2:
            conviction = 0.9
        if conditional:
            conviction *= 0.75
        if any(term in text for term in ("可能", "也许", "倾向", "感觉", "不确定")):
            conviction *= 0.65

        disclosed_position: str | None = None
        if long_position and not short_position:
            disclosed_position = "long"
        elif short_position and not long_position:
            disclosed_position = "short"

        platform = str(record.get("platform") or "unknown")
        source_group = _infer_group(record)
        published_at = str(
            record.get("published_at")
            or record.get("captured_at")
        )
        captured_at = str(record.get("captured_at") or published_at)
        raw_hash = str(
            record.get("raw_hash")
            or hashlib.sha256(text.encode("utf-8")).hexdigest()
        )
        observation_id = hashlib.sha256(
            f"{raw_hash}\n{direction}\n{_infer_horizon(text)}".encode("utf-8")
        ).hexdigest()

        evidence = text[:240]

        return [
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
                author_id_hash=_author_hash(
                    str(record.get("author")) if record.get("author") else None,
                    platform,
                ),
                author_display_name=(
                    str(record.get("author")) if record.get("author") else None
                ),
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
                direction=direction,
                horizon=_infer_horizon(text),
                classifier_confidence=max(0.0, min(1.0, confidence)),
                conviction=max(0.0, min(1.0, conviction)),
                position_disclosed=disclosed_position is not None,
                disclosed_position=disclosed_position,
                reason_tags=_reason_tags(text),
                target_price=target_price,
                narrative_ids=[],
                uniqueness_factor=1.0,
                source_weight=1.0,
                raw_hash=raw_hash,
                classification_flags=sorted(set(flags)),
                classification_evidence=evidence,
                discovery_lane=record.get("discovery_lane"),
                search_term=record.get("query"),
                engagement=dict(record.get("raw", {}).get("engagement") or {}),
                provenance={
                    "tool": "HeuristicLCClassifier",
                    "model_version": model_version,
                    "retrieval_run_id": None,
                    "classification_run_id": None,
                },
            )
        ]


def classify_records(
    records: Iterable[dict[str, Any]],
    *,
    classifier: ObservationClassifier,
    asset_id: str,
    model_version: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        rows.extend(
            asdict(item)
            for item in classifier.classify(
                record,
                asset_id=asset_id,
                model_version=model_version,
            )
        )
    return rows
