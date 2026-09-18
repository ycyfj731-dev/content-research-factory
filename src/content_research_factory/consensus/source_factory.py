from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

from ..adapters.crawl4ai import Crawl4AIAdapter
from ..adapters.mcp_stdio import MCPStdioConfig
from ..adapters.reddit_mcp import RedditMCPAdapter, RedditMCPConfig
from ..adapters.tikhub import TikHubAdapter, TikHubConfig
from ..adapters.trendscope import TrendScopeAdapter, TrendScopeConfig
from ..clients import SupplementalSearchClient, WebCrawlerClient


@dataclass(frozen=True)
class SourceExpansion:
    supplemental_sources: tuple[tuple[str, SupplementalSearchClient], ...]
    web_crawler: WebCrawlerClient | None
    enabled_sources: tuple[str, ...]


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def build_source_expansion(
    env: Mapping[str, str] | None = None,
) -> SourceExpansion:
    values = dict(os.environ if env is None else env)
    supplemental: list[tuple[str, SupplementalSearchClient]] = []
    enabled: list[str] = []

    trendscope_url = values.get("TRENDSCOPE_URL")
    if trendscope_url:
        supplemental.append(
            (
                "TrendScope",
                TrendScopeAdapter(
                    TrendScopeConfig(
                        base_url=trendscope_url,
                        api_key=values.get("TRENDSCOPE_API_KEY"),
                    )
                ),
            )
        )
        enabled.append("TrendScope")

    reddit_key = values.get("REDDITAPIS_KEY") or values.get("REDDIT_APIS_KEY")
    if reddit_key:
        reddit_env = dict(values)
        reddit_env["REDDITAPIS_KEY"] = reddit_key
        supplemental.append(
            (
                "RedditMCP",
                RedditMCPAdapter(
                    RedditMCPConfig(
                        stdio=MCPStdioConfig(
                            command=values.get("REDDIT_MCP_COMMAND", "npx"),
                            args=(
                                "-y",
                                values.get(
                                    "REDDIT_MCP_PACKAGE",
                                    "redditapis-mcp@latest",
                                ),
                            ),
                            env=reddit_env,
                        )
                    )
                ),
            )
        )
        enabled.append("RedditMCP")

    tikhub_key = values.get("TIKHUB_API_KEY")
    if tikhub_key:
        supplemental.append(
            (
                "TikHub",
                TikHubAdapter(
                    TikHubConfig(
                        api_key=tikhub_key,
                    )
                ),
            )
        )
        enabled.append("TikHub")

    web_crawler = None
    if _truthy(values.get("CRF_ENABLE_CRAWL4AI")):
        web_crawler = Crawl4AIAdapter()
        enabled.append("Crawl4AI")

    return SourceExpansion(
        supplemental_sources=tuple(supplemental),
        web_crawler=web_crawler,
        enabled_sources=tuple(enabled),
    )
