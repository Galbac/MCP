from collections.abc import Callable
from typing import Any

from openai import OpenAI


class LlmServiceError(RuntimeError):
    pass


class MissingAPIKeyError(LlmServiceError):
    pass


class EmptyPromptError(LlmServiceError):
    pass


class ProviderRequestError(LlmServiceError):
    pass


def _default_client_factory(
    api_key: str,
    base_url: str,
    default_headers: dict[str, str],
) -> OpenAI:
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers=default_headers,
    )


class LlmService:
    def __init__(
        self,
        api_key: str | None,
        model: str,
        base_url: str,
        site_url: str | None,
        app_name: str,
        client_factory: Callable[[str, str, dict[str, str]], Any] = _default_client_factory,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.site_url = site_url
        self.app_name = app_name
        self.client_factory = client_factory

    def ask(self, prompt: str) -> str:
        normalized_prompt = prompt.strip()
        if not normalized_prompt:
            raise EmptyPromptError("Prompt must not be empty")

        if not self.api_key:
            raise MissingAPIKeyError("OPENROUTER_API_KEY is not configured")

        headers = {"X-Title": self.app_name}
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url

        client = self.client_factory(self.api_key, self.base_url, headers)

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": normalized_prompt}],
            )
        except Exception as exc:
            raise ProviderRequestError(f"OpenRouter request failed: {exc}") from exc

        choices = getattr(response, "choices", None)
        if choices:
            message = getattr(choices[0], "message", None)
            content = getattr(message, "content", None)
            if content:
                return content

        raise ProviderRequestError("OpenRouter response did not include text output")
