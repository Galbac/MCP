from mcp.server.fastmcp import FastMCP

from src.mcp_playground.services.clock import ClockService


def register_system_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def ping() -> str:
        """Health check tool for testing client-to-server communication."""
        return "pong"

    @mcp.tool()
    def get_time() -> str:
        """Return current UTC time in ISO 8601 format."""
        return ClockService.now_iso()