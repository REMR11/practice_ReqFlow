from core.ai_proxy_client import AIProxyClient
from core.prompt_loader import PromptLoader
from models.schemas import SkillResult
from skills.base_skill import BaseSkill


class ProductOwnerSkill(BaseSkill):
    def __init__(
        self,
        ai_client: AIProxyClient | None = None,
        prompt_loader: PromptLoader | None = None,
    ) -> None:
        super().__init__(
            skill_name="product_owner",
            prompt_filename="product_owner.md",
            ai_client=ai_client,
            prompt_loader=prompt_loader,
        )

    def _mock_response(self, requirement: str) -> SkillResult:
        content = (
            "### Historia de Usuario\n\n"
            f"Como usuario, quiero {requirement}, para cumplir el objetivo del negocio.\n\n"
            "### Criterios de Aceptacion\n\n"
            "- Dado el requerimiento definido, cuando el usuario ejecuta el flujo, entonces obtiene el resultado esperado.\n"
            "- El comportamiento principal queda documentado y validable.\n"
            "- Se contemplan mensajes claros para escenarios de error."
        )
        return SkillResult(
            content=content,
            is_mock=True,
            skill_name=self.skill_name,
            error=None,
        )
