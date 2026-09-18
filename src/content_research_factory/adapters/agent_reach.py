from __future__ import annotations

from typing import Any, Mapping, Sequence

from .jsonrpc_stdio import JSONRPCStdioClient, JSONRPCStdioConfig


class AgentReachAdapter:
    def __init__(
        self,
        config: JSONRPCStdioConfig,
        *,
        verify_method: str = "verify",
    ) -> None:
        self.rpc = JSONRPCStdioClient(config)
        self.verify_method = verify_method

    def verify(
        self,
        query: str,
        *,
        candidates: list[dict[str, Any]],
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        result = self.rpc.call(
            self.verify_method,
            {
                "query": query,
                "candidates": candidates,
                "limit": limit,
            },
        )
        return self._normalize(result)

    @staticmethod
    def _normalize(result: Any) -> list[dict[str, Any]]:
        if isinstance(result, Mapping):
            items = result.get("items") or result.get("data") or [result]
        elif isinstance(result, Sequence) and not isinstance(result, (str, bytes)):
            items = result
        else:
            raise ValueError("Agent-Reach result must contain item objects")

        normalized = []
        for item in items:
            if not isinstance(item, Mapping):
                raise ValueError("Agent-Reach item must be an object")
            normalized.append(dict(item))
        return normalized
