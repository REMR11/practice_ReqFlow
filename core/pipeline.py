from models.schemas import PipelineResult
from skills.architecture_skill import ArchitectureSkill
from skills.product_owner_skill import ProductOwnerSkill
from skills.qa_skill import QASkill


class RequirementPipeline:
    def __init__(
        self,
        product_owner_skill: ProductOwnerSkill | None = None,
        qa_skill: QASkill | None = None,
        architecture_skill: ArchitectureSkill | None = None,
    ) -> None:
        self.product_owner_skill = product_owner_skill or ProductOwnerSkill()
        self.qa_skill = qa_skill or QASkill()
        self.architecture_skill = architecture_skill or ArchitectureSkill()

    def execute(self, requirement: str) -> PipelineResult:
        user_story_result = self.product_owner_skill.run(requirement, context="")
        qa_result = self.qa_skill.run(requirement, context=user_story_result.content)
        combined_context = f"{user_story_result.content}\n\n{qa_result.content}"
        architecture_result = self.architecture_skill.run(
            requirement,
            context=combined_context,
        )

        return PipelineResult(
            requirement=requirement,
            user_story=user_story_result,
            qa_cases=qa_result,
            architecture=architecture_result,
        )
