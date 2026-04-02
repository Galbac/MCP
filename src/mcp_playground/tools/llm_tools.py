from mcp.server.fastmcp import FastMCP

from src.mcp_playground.services.llm_service import LlmService


def register_llm_tools(mcp: FastMCP, llm_service: LlmService) -> None:
    @mcp.tool()
    def ask_llm(prompt: str) -> str:
        """Send a prompt to OpenAI via the Responses API and return the text response."""
        return llm_service.ask(prompt)
