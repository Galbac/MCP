from mcp.server.fastmcp import FastMCP

from src.mcp_playground.config import Settings


def register_project_resources(mcp: FastMCP, settings: Settings) -> None:
    @mcp.resource("info://server")
    def server_info() -> str:
        """Basic metadata about this MCP server."""
        return (
            f"name={settings.app_name}\n"
            f"allowed_root={settings.allowed_root.resolve()}\n"
            f"notes_dir={settings.notes_dir.resolve()}\n"
        )