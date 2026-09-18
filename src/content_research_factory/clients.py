from __future__ import annotations

from typing import Any, Protocol


class TrendRadarClient(Protocol):
    def discover(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        ...


class AgentReachClient(Protocol):
    def verify(
        self,
        query: str,
        *,
        candidates: list[dict[str, Any]],
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        ...


class MediaCrawlerClient(Protocol):
    def search(
        self,
        query: str,
        *,
        platform: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        ...

    def detail(
        self,
        source_id: str,
        *,
        platform: str | None = None,
    ) -> dict[str, Any]:
        ...

    def comments(
        self,
        source_id: str,
        *,
        platform: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        ...


class MoneyPrinterTurboClient(Protocol):
    def produce(self, research_package: dict[str, Any]) -> dict[str, Any]:
        ...
