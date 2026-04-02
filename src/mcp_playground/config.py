from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "mcp-playground"
    debug: bool = False
    notes_dir: Path = Field(default=Path("data/notes"))
    allowed_root: Path = Field(default=Path("data"))
    openrouter_api_key: str | None = None
    openrouter_model: str = "openai/gpt-4.1-nano"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_site_url: str | None = None
    openrouter_app_name: str = "mcp-playground"

    def ensure_paths(self) -> None:
        self.allowed_root.mkdir(parents=True, exist_ok=True)
        self.notes_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
