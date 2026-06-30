from models.schemas import PipelineResult, SkillResult


def test_skill_result_defaults_error_to_none() -> None:
    result = SkillResult(content="ok", is_mock=False, skill_name="qa")
    assert result.content == "ok"
    assert result.is_mock is False
    assert result.skill_name == "qa"
    assert result.error is None


def test_pipeline_result_stores_three_skill_results() -> None:
    po = SkillResult(content="po", is_mock=True, skill_name="product_owner")
    qa = SkillResult(content="qa", is_mock=True, skill_name="qa")
    arch = SkillResult(content="arch", is_mock=True, skill_name="architecture")

    result = PipelineResult(
        requirement="login con google",
        user_story=po,
        qa_cases=qa,
        architecture=arch,
    )

    assert result.requirement == "login con google"
    assert result.user_story is po
    assert result.qa_cases is qa
    assert result.architecture is arch
