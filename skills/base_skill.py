from abc import ABC, abstractmethod

from core.ai_proxy_client import AIProxyClient, AIProxyError
from core.prompt_loader import PromptLoader, PromptNotFoundError
from models.schemas import SkillResult


class BaseSkill(ABC):
    def __init__(
        self,
        skill_name: str,
        prompt_filename: str,
        ai_client: AIProxyClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        self.skill_name = skill_name
        self.prompt_filename = prompt_filename
        self.ai_client = ai_client or AIProxyClient()
        self.prompt_loader = prompt_loader or PromptLoader()

        try:
            self.system_prompt = self.prompt_loader.load(self.prompt_filename)
        except PromptNotFoundError:
            self.system_prompt = self._default_system_prompt()

    def run(self, requirement: str, context: str = "") -> SkillResult:
        if not self.ai_client.is_available:
            return self._mock_response(requirement)

        try:
            user_message = self._build_user_message(requirement=requirement, context=context)
            content = self.ai_client.complete(
                system_prompt=self.system_prompt,
                user_message=user_message,
                max_tokens=1000,
            )
            return SkillResult(
                content=content,
                is_mock=False,
                skill_name=self.skill_name,
                error=None,
            )
        except AIProxyError:
            return self._mock_response(requirement)
        except Exception as exc:
            fallback = self._mock_response(requirement)
            return SkillResult(
                content=fallback.content,
                is_mock=True,
                skill_name=self.skill_name,
                error=str(exc),
            )

    @abstractmethod
    def _mock_response(self, requirement: str) -> SkillResult:
        """Return a deterministic markdown response used in mock mode."""

    def _build_user_message(self, requirement: str, context: str) -> str:
        if not context.strip():
            return requirement
        return (
            f"Requerimiento original:\n{requirement}\n\n"
            f"Contexto previo:\n{context}"
        )

    def _default_system_prompt(self) -> str:
        return (
            "Eres un asistente experto en analisis de requerimientos. "
            f"Genera una respuesta para la skill '{self.skill_name}' en Markdown."
        )
