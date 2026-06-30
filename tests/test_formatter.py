from models.schemas import PipelineResult, SkillResult
from utils.formatter import MarkdownFormatter


def test_format_skill_result_normal_content() -> None:
    result = SkillResult(content="contenido", is_mock=False, skill_name="qa")
    output = MarkdownFormatter.format_skill_result(result, "QA")
    assert "## QA" in output
    assert "contenido" in output
    assert "modo mock" not in output


def test_format_skill_result_mock_banner() -> None:
    result = SkillResult(content="contenido", is_mock=True, skill_name="qa")
    output = MarkdownFormatter.format_skill_result(result, "QA")
    assert "Generado en modo mock" in output


def test_format_skill_result_error_mode() -> None:
    result = SkillResult(content="contenido", is_mock=True, skill_name="qa", error="fallo")
    output = MarkdownFormatter.format_skill_result(result, "QA")
    assert "> Error: fallo" in output
    assert output.strip().startswith("## QA")


def test_format_pipeline_result_joins_three_sections() -> None:
    pipeline_result = PipelineResult(
        requirement="req",
        user_story=SkillResult(content="po", is_mock=True, skill_name="product_owner"),
        qa_cases=SkillResult(content="qa", is_mock=True, skill_name="qa"),
        architecture=SkillResult(content="arch", is_mock=True, skill_name="architecture"),
    )
    output = MarkdownFormatter.format_pipeline_result(pipeline_result)

    assert "Historia de Usuario" in output
    assert "Casos de Prueba" in output
    assert "Recomendacion Arquitectonica" in output
    assert output.count("---") == 2
