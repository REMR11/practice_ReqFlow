import os
from typing import Any

import requests


class AIProxyError(Exception):
    """Raised when the AI proxy request fails or returns invalid data."""


class AIProxyClient:
    def __init__(
        self,
        proxy_url: str | None = None,
        proxy_api_key: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.proxy_url = proxy_url or os.getenv("AI_PROXY_URL", "")
        self.proxy_api_key = proxy_api_key or os.getenv("AI_PROXY_API_KEY", "")
        self.model = os.getenv("AI_PROXY_MODEL", "gpt-4o-mini")
        self.timeout = timeout
        self.is_available = bool(self.proxy_url and self.proxy_api_key)

    def complete(
        self, system_prompt: str, user_message: str, max_tokens: int = 1000
    ) -> str:
        if not self.is_available:
            raise AIProxyError("AI proxy is not configured.")

        url = f"{self.proxy_url.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.proxy_api_key}"}
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": max_tokens,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise AIProxyError(f"AI proxy request failed: {exc}") from exc

        try:
            response_payload = response.json()
        except ValueError as exc:
            raise AIProxyError("AI proxy returned invalid JSON.") from exc

        return self._extract_content(response_payload)

    def _extract_content(self, response_payload: dict[str, Any]) -> str:
        try:
            choices = response_payload.get("choices", [])
            if choices:
                first_choice = choices[0]
                message = first_choice.get("message", {})
                if isinstance(message, dict) and message.get("content"):
                    return str(message["content"])
                if first_choice.get("text"):
                    return str(first_choice["text"])

            content = response_payload.get("content")
            if isinstance(content, str) and content.strip():
                return content
        except (AttributeError, IndexError, KeyError, TypeError):
            pass

        raise AIProxyError("AI proxy response does not include textual content.")
