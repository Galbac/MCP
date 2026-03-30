from mcp.server.fastmcp import FastMCP

from src.mcp_playground.services.file_service import FileService


def register_file_tools(mcp: FastMCP, file_service: FileService) -> None:
    @mcp.tool()
    def list_files(path: str = ".") -> list[str]:
        """List files and directories under the allowed project root."""
        return file_service.list_files(path)

    @mcp.tool()
    def read_text_file(path: str) -> str:
        """Read a UTF-8 text file from inside the allowed project root."""
        return file_service.read_text_file(path)