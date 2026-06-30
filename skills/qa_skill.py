from core.ai_proxy_client import AIProxyClient
from core.prompt_loader import PromptLoader
from models.schemas import SkillResult
from skills.base_skill import BaseSkill


class QASkill(BaseSkill):
    def __init__(
        self,
        ai_client: AIProxyClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        super().__init__(
            skill_name="qa",
            prompt_filename="qa.md",
            ai_client=ai_client,
            prompt_loader=prompt_loader,
        )

    def _mock_response(self, requirement: str) -> SkillResult:
        content = (
            "### Casos de Prueba\n\n"
            f"#### Caso 1: Flujo principal de '{requirement}'\n"
            "- **Precondicion:** Usuario con acceso al sistema.\n"
            "- **Pasos:** Ejecutar el flujo principal segun la historia de usuario.\n"
            "- **Resultado esperado:** El sistema completa la accion sin errores.\n\n"
            "#### Caso 2: Datos invalidos o incompletos\n"
            "- **Precondicion:** Entrada con datos faltantes.\n"
            "- **Pasos:** Intentar completar el flujo con informacion invalida.\n"
            "- **Resultado esperado:** Se muestra mensaje de validacion claro.\n\n"
            "#### Caso 3: Manejo de fallos externos\n"
            "- **Precondicion:** Servicio externo no disponible.\n"
            "- **Pasos:** Ejecutar accion dependiente del servicio externo.\n"
            "- **Resultado esperado:** Degradacion controlada y mensaje de error util."
        )
        return SkillResult(
            content=content,
            is_mock=True,
            skill_name=self.skill_name,
            error=None,
        )
