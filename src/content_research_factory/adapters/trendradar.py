from __future__ import annotations

from typing import Any, Mapping, Sequence

from .jsonrpc_stdio import JSONRPCStdioClient, JSONRPCStdioConfig


class TrendRadarAdapter:
    def __init__(
        self,
        config: JSONRPCStdioConfig,
        *,
        discover_method: str = "discover",
    ) -> None:
        self.rpc = JSONRPCStdioClient(config)
        self.discover_method = discover_method

    def discover(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        result = self.rpc.call(
            self.discover_method,
            {"query": query, "limit": limit},
        )
        return self._normalize(result)

    @staticmethod
    def _normalize(result: Any) -> list[dict[str, Any]]:
        if isinstance(result, Mapping):
            items = result.get("items") or result.get("data") or [result]
        elif isinstance(result, Sequence) and not isinstance(result, (str, bytes)):
            items = result
        else:
            raise ValueError("TrendRadar result must contain item objects")

        normalized = []
        for item in items:
            if not isinstance(item, Mapping):
                raise ValueError("TrendRadar item must be an object")
            normalized.append(dict(item))
        return normalized
