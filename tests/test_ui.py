from models.schemas import SkillResult
from utils.ui import badge_label, badge_status


def test_badge_status_success_when_ai_generated() -> None:
    result = SkillResult(content="ok", is_mock=False, skill_name="qa")
    assert badge_status(result) == "success"


def test_badge_status_warning_when_mock() -> None:
    result = SkillResult(content="ok", is_mock=True, skill_name="qa")
    assert badge_status(result) == "warning"


def test_badge_status_error_when_error_present() -> None:
    result = SkillResult(content="ok", is_mock=False, skill_name="qa", error="fallo")
    assert badge_status(result) == "error"


def test_badge_label_matches_status() -> None:
    assert badge_label(SkillResult(content="x", is_mock=False, skill_name="qa")) == "Generado con IA"
    assert badge_label(SkillResult(content="x", is_mock=True, skill_name="qa")) == "Modo mock"
    assert (
        badge_label(SkillResult(content="x", is_mock=True, skill_name="qa", error="e"))
        == "Error en generacion"
    )
