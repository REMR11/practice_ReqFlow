from models.schemas import SkillResult
from core.pipeline import RequirementPipeline


class FixedSkill:
    def __init__(self, name: str) -> None:
        self.name = name
        self.calls: list[tuple[str, str]] = []

    def run(self, requirement: str, context: str = "") -> SkillResult:
        self.calls.append((requirement, context))
        return SkillResult(
            content=f"{self.name}-out",
            is_mock=True,
            skill_name=self.name,
            error=None,
        )


def test_pipeline_executes_in_sequence_and_accumulates_context() -> None:
    po = FixedSkill("po")
    qa = FixedSkill("qa")
    arch = FixedSkill("arch")
    pipeline = RequirementPipeline(po, qa, arch)

    result = pipeline.execute("mi requerimiento")

    assert po.calls == [("mi requerimiento", "")]
    assert qa.calls == [("mi requerimiento", "po-out")]
    assert arch.calls == [("mi requerimiento", "po-out\n\nqa-out")]
    assert result.requirement == "mi requerimiento"
    assert result.user_story.content == "po-out"
    assert result.qa_cases.content == "qa-out"
    assert result.architecture.content == "arch-out"
