from mcp.server.fastmcp import FastMCP

from src.mcp_playground.config import settings
from src.mcp_playground.http_routes import register_http_routes
from src.mcp_playground.resources.project_resources import register_project_resources
from src.mcp_playground.services.file_service import FileService
from src.mcp_playground.services.llm_service import LlmService
from src.mcp_playground.tools.file_tools import register_file_tools
from src.mcp_playground.tools.llm_tools import register_llm_tools
from src.mcp_playground.tools.math_tools import register_math_tools
from src.mcp_playground.tools.system_tools import register_system_tools


def create_server() -> FastMCP:
    settings.ensure_paths()

    mcp = FastMCP(settings.app_name)
    file_service = FileService(settings.allowed_root)
    llm_service = LlmService(
        api_key=settings.openrouter_api_key,
        model=settings.openrouter_model,
        base_url=settings.openrouter_base_url,
        site_url=settings.openrouter_site_url,
        app_name=settings.openrouter_app_name,
    )

    register_system_tools(mcp)
    register_math_tools(mcp)
    register_file_tools(mcp, file_service)
    register_llm_tools(mcp, llm_service)
    register_project_resources(mcp, settings)
    register_http_routes(mcp, settings, file_service, llm_service)

    return mcp
