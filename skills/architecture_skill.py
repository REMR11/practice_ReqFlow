from core.ai_proxy_client import AIProxyClient
from core.prompt_loader import PromptLoader
from models.schemas import SkillResult
from skills.base_skill import BaseSkill


class ArchitectureSkill(BaseSkill):
    def __init__(
        self,
        ai_client: AIProxyClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        super().__init__(
            skill_name="architecture",
            prompt_filename="architecture.md",
            ai_client=ai_client,
            prompt_loader=prompt_loader,
        )

    def _mock_response(self, requirement: str) -> SkillResult:
        content = (
            "### Recomendacion Arquitectonica\n\n"
            f"Para implementar '{requirement}' se recomienda una arquitectura por capas:\n\n"
            "1. **Presentacion (Streamlit):** captura el requerimiento y muestra resultados.\n"
            "2. **Orquestacion (Pipeline):** coordina PO -> QA -> Arquitectura.\n"
            "3. **Skills especializadas:** encapsulan la logica de cada etapa.\n"
            "4. **Infraestructura compartida:** cliente de IA y carga de prompts.\n\n"
            "### Consideraciones tecnicas\n\n"
            "- Mantener contratos estables con `SkillResult` y `PipelineResult`.\n"
            "- Aplicar degradacion elegante con respuestas mock cuando no haya IA.\n"
            "- Aislar integraciones externas en `AIProxyClient` para facilitar pruebas."
        )
        return SkillResult(
            content=content,
            is_mock=True,
            skill_name=self.skill_name,
            error=None,
        )
