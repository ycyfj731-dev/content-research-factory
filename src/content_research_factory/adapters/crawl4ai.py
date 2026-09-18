from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any


class Crawl4AIUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class Crawl4AIConfig:
    word_count_threshold: int = 20


class Crawl4AIAdapter:
    def __init__(self, config: Crawl4AIConfig | None = None) -> None:
        self.config = config or Crawl4AIConfig()

    def crawl(self, url: str) -> dict[str, Any]:
        return asyncio.run(self._crawl(url))

    async def _crawl(self, url: str) -> dict[str, Any]:
        try:
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
        except ImportError as exc:
            raise Crawl4AIUnavailable(
                "crawl4ai is not installed; install the 'sources' extra"
            ) from exc

        run_config = CrawlerRunConfig(
            word_count_threshold=self.config.word_count_threshold,
        )
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)

        markdown = getattr(result, "markdown", None)
        if hasattr(markdown, "raw_markdown"):
            markdown = markdown.raw_markdown

        metadata = getattr(result, "metadata", None) or {}
        return {
            "platform": "web",
            "source_id": url,
            "url": url,
            "title": metadata.get("title"),
            "text": str(markdown or ""),
            "published_at": metadata.get("published_time")
            or metadata.get("date")
            or metadata.get("article:published_time"),
            "origin_tool": "Crawl4AI",
            "raw": {
                "success": bool(getattr(result, "success", True)),
                "metadata": metadata,
            },
        }
