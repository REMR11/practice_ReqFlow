from __future__ import annotations

from dataclasses import dataclass

import pytest

from core.ai_proxy_client import AIProxyError


@dataclass
class FakePromptLoader:
    prompt_text: str = "Prompt de prueba"

    def load(self, prompt_filename: str) -> str:
        return f"{self.prompt_text}: {prompt_filename}"


class FakeAIClient:
    def __init__(
        self,
        available: bool = True,
        response_text: str = "respuesta IA",
        raise_ai_error: bool = False,
        raise_generic_error: bool = False,
    ) -> None:
        self.is_available = available
        self.response_text = response_text
        self.raise_ai_error = raise_ai_error
        self.raise_generic_error = raise_generic_error
        self.last_system_prompt = None
        self.last_user_message = None
        self.last_max_tokens = None

    def complete(
        self, system_prompt: str, user_message: str, max_tokens: int = 1000
    ) -> str:
        self.last_system_prompt = system_prompt
        self.last_user_message = user_message
        self.last_max_tokens = max_tokens

        if self.raise_ai_error:
            raise AIProxyError("fallo simulado")
        if self.raise_generic_error:
            raise RuntimeError("fallo inesperado")
        return self.response_text


@pytest.fixture
def fake_prompt_loader() -> FakePromptLoader:
    return FakePromptLoader()
