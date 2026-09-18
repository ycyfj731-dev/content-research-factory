from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any


class MCPToolError(RuntimeError):
    pass


@dataclass(frozen=True)
class MCPStdioConfig:
    command: str
    args: tuple[str, ...] = ()
    env: dict[str, str] | None = None


class MCPStdioToolClient:
    """Real MCP stdio client using the official Python MCP SDK."""

    def __init__(self, config: MCPStdioConfig):
        self.config = config

    def call(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        return asyncio.run(self._call(tool_name, arguments))

    async def _call(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        server = StdioServerParameters(
            command=self.config.command,
            args=list(self.config.args),
            env=self.config.env,
        )
        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=arguments)

        if getattr(result, "isError", False):
            raise MCPToolError(f"{tool_name} returned an MCP error")

        chunks = []
        for item in getattr(result, "content", []):
            value = getattr(item, "text", None)
            if value is not None:
                chunks.append(value)

        if not chunks:
            structured = getattr(result, "structuredContent", None)
            return structured

        payload = "\n".join(chunks).strip()
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return payload
