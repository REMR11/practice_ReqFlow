from skills.architecture_skill import ArchitectureSkill
from skills.base_skill import BaseSkill
from skills.product_owner_skill import ProductOwnerSkill
from skills.qa_skill import QASkill
from tests.conftest import FakeAIClient, FakePromptLoader


def test_concrete_skills_reuse_base_run() -> None:
    assert ProductOwnerSkill.run is BaseSkill.run
    assert QASkill.run is BaseSkill.run
    assert ArchitectureSkill.run is BaseSkill.run


def test_product_owner_mock_response_shape() -> None:
    skill = ProductOwnerSkill(
        ai_client=FakeAIClient(available=False),
        prompt_loader=FakePromptLoader(),
    )
    result = skill.run("login con google")
    assert result.skill_name == "product_owner"
    assert result.is_mock is True
    assert "Historia de Usuario" in result.content


def test_qa_mock_response_shape() -> None:
    skill = QASkill(
        ai_client=FakeAIClient(available=False),
        prompt_loader=FakePromptLoader(),
    )
    result = skill.run("login con google", context="historia")
    assert result.skill_name == "qa"
    assert result.is_mock is True
    assert "Casos de Prueba" in result.content


def test_architecture_mock_response_shape() -> None:
    skill = ArchitectureSkill(
        ai_client=FakeAIClient(available=False),
        prompt_loader=FakePromptLoader(),
    )
    result = skill.run("login con google", context="historia + qa")
    assert result.skill_name == "architecture"
    assert result.is_mock is True
    assert "Recomendacion Arquitectonica" in result.content
