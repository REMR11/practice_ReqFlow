from __future__ import annotations

from core.ai_proxy_client import AIProxyError
from core.prompt_loader import PromptNotFoundError
from models.schemas import SkillResult
from skills.base_skill import BaseSkill
from tests.conftest import FakeAIClient


class BrokenPromptLoader:
    def load(self, prompt_filename: str) -> str:
        raise PromptNotFoundError(prompt_filename)


class DummySkill(BaseSkill):
    def __init__(self, ai_client, prompt_loader) -> None:
        super().__init__(
            skill_name="dummy",
            prompt_filename="dummy.md",
            ai_client=ai_client,
            prompt_loader=prompt_loader,
        )

    def _mock_response(self, requirement: str) -> SkillResult:
        return SkillResult(
            content=f"mock for {requirement}",
            is_mock=True,
            skill_name=self.skill_name,
            error=None,
        )


class StaticPromptLoader:
    def load(self, prompt_filename: str) -> str:
        return "prompt fijo"


def test_run_returns_mock_when_ai_unavailable() -> None:
    skill = DummySkill(
        ai_client=FakeAIClient(available=False),
        prompt_loader=StaticPromptLoader(),
    )
    result = skill.run("req")
    assert result.is_mock is True
    assert result.content == "mock for req"
    assert result.error is None


def test_run_returns_real_content_when_ai_available() -> None:
    client = FakeAIClient(available=True, response_text="resultado real")
    skill = DummySkill(ai_client=client, prompt_loader=StaticPromptLoader())

    result = skill.run("req", context="ctx")
    assert result.is_mock is False
    assert result.content == "resultado real"
    assert result.error is None
    assert client.last_system_prompt == "prompt fijo"
    assert "Contexto previo" in client.last_user_message


def test_run_falls_back_to_mock_on_ai_proxy_error() -> None:
    client = FakeAIClient(available=True, raise_ai_error=True)
    skill = DummySkill(ai_client=client, prompt_loader=StaticPromptLoader())

    result = skill.run("req")
    assert result.is_mock is True
    assert result.content == "mock for req"
    assert result.error is None


def test_run_returns_error_result_on_unexpected_exception() -> None:
    client = FakeAIClient(available=True, raise_generic_error=True)
    skill = DummySkill(ai_client=client, prompt_loader=StaticPromptLoader())

    result = skill.run("req")
    assert result.is_mock is True
    assert result.content == "mock for req"
    assert "fallo inesperado" in (result.error or "")


def test_build_user_message_without_context() -> None:
    skill = DummySkill(ai_client=FakeAIClient(), prompt_loader=StaticPromptLoader())
    assert skill._build_user_message("req", "") == "req"


def test_build_user_message_with_context() -> None:
    skill = DummySkill(ai_client=FakeAIClient(), prompt_loader=StaticPromptLoader())
    built = skill._build_user_message("req", "ctx")
    assert "Requerimiento original" in built
    assert "Contexto previo" in built
    assert "req" in built and "ctx" in built


def test_missing_prompt_uses_default_prompt() -> None:
    skill = DummySkill(ai_client=FakeAIClient(), prompt_loader=BrokenPromptLoader())
    assert "dummy" in skill.system_prompt
