from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.mcp_playground.config import Settings
from src.mcp_playground.services.clock import ClockService
from src.mcp_playground.services.file_service import FileService, UnsafePathError
from src.mcp_playground.services.llm_service import (
    EmptyPromptError,
    LlmService,
    MissingAPIKeyError,
    ProviderRequestError,
)


def _json_error(status_code: int, detail: str) -> JSONResponse:
    return JSONResponse({"error": detail}, status_code=status_code)


def register_http_routes(
    mcp,
    settings: Settings,
    file_service: FileService,
    llm_service: LlmService,
) -> None:
    @mcp.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> Response:
        return JSONResponse(
            {
                "status": "ok",
                "app_name": settings.app_name,
            }
        )

    @mcp.custom_route("/api/ping", methods=["GET"])
    async def ping(_: Request) -> Response:
        return JSONResponse({"result": "pong"})

    @mcp.custom_route("/api/time", methods=["GET"])
    async def get_time(_: Request) -> Response:
        return JSONResponse({"result": ClockService.now_iso()})

    @mcp.custom_route("/api/add", methods=["GET"])
    async def add(request: Request) -> Response:
        try:
            a = int(request.query_params["a"])
            b = int(request.query_params["b"])
        except KeyError as exc:
            return _json_error(400, f"Missing query parameter: {exc.args[0]}")
        except ValueError:
            return _json_error(400, "Query parameters 'a' and 'b' must be integers")

        return JSONResponse({"result": a + b})

    @mcp.custom_route("/api/files", methods=["GET"])
    async def list_files(request: Request) -> Response:
        path = request.query_params.get("path", ".")

        try:
            result = file_service.list_files(path)
        except UnsafePathError as exc:
            return _json_error(400, str(exc))
        except FileNotFoundError as exc:
            return _json_error(404, str(exc))
        except NotADirectoryError as exc:
            return _json_error(400, str(exc))

        return JSONResponse({"path": path, "result": result})

    @mcp.custom_route("/api/files/content", methods=["GET"])
    async def read_text_file(request: Request) -> Response:
        path = request.query_params.get("path")
        if not path:
            return _json_error(400, "Missing query parameter: path")

        try:
            result = file_service.read_text_file(path)
        except UnsafePathError as exc:
            return _json_error(400, str(exc))
        except FileNotFoundError as exc:
            return _json_error(404, str(exc))
        except IsADirectoryError as exc:
            return _json_error(400, str(exc))

        return JSONResponse({"path": path, "result": result})

    @mcp.custom_route("/api/resources/server-info", methods=["GET"])
    async def server_info(_: Request) -> Response:
        return JSONResponse(
            {
                "name": settings.app_name,
                "allowed_root": str(settings.allowed_root.resolve()),
                "notes_dir": str(settings.notes_dir.resolve()),
            }
        )

    @mcp.custom_route("/api/llm", methods=["POST"])
    async def ask_llm(request: Request) -> Response:
        try:
            payload = await request.json()
        except Exception:
            return _json_error(400, "Request body must be valid JSON")

        prompt = payload.get("prompt") if isinstance(payload, dict) else None
        if not isinstance(prompt, str):
            return _json_error(400, "Field 'prompt' must be a string")

        try:
            result = llm_service.ask(prompt)
        except EmptyPromptError as exc:
            return _json_error(400, str(exc))
        except MissingAPIKeyError as exc:
            return _json_error(500, str(exc))
        except ProviderRequestError as exc:
            return _json_error(502, str(exc))

        return JSONResponse(
            {
                "model": settings.openrouter_model,
                "result": result,
            }
        )
