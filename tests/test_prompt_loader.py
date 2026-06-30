from pathlib import Path

import pytest

from core.prompt_loader import PromptLoader, PromptNotFoundError


def test_prompt_loader_resolves_default_prompts_dir() -> None:
    loader = PromptLoader()
    assert loader.prompts_dir.name == "prompts"
    assert loader.prompts_dir.is_absolute()


def test_prompt_loader_load_reads_file(tmp_path: Path) -> None:
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir(parents=True)
    prompt_file = prompts_dir / "sample.md"
    prompt_file.write_text("contenido prompt", encoding="utf-8")

    loader = PromptLoader(prompts_dir=prompts_dir)
    assert loader.load("sample.md") == "contenido prompt"


def test_prompt_loader_load_raises_when_missing(tmp_path: Path) -> None:
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir(parents=True)
    loader = PromptLoader(prompts_dir=prompts_dir)

    with pytest.raises(PromptNotFoundError):
        loader.load("missing.md")


def test_prompt_loader_default_path_independent_from_cwd(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    loader = PromptLoader()
    monkeypatch.chdir(tmp_path)
    text = loader.load("product_owner.md")
    assert "Product Owner" in text
