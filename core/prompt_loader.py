from pathlib import Path


class PromptNotFoundError(Exception):
    """Raised when the prompt file cannot be found."""


class PromptLoader:
    def __init__(self, prompts_dir: str | Path | None = None) -> None:
        if prompts_dir is None:
            self.prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
        else:
            self.prompts_dir = Path(prompts_dir)

    def load(self, prompt_filename: str) -> str:
        prompt_path = self.prompts_dir / prompt_filename
        if not prompt_path.exists():
            raise PromptNotFoundError(f"Prompt not found: {prompt_filename}")
        return prompt_path.read_text(encoding="utf-8")
