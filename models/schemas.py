from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillResult:
    content: str
    is_mock: bool
    skill_name: str
    error: Optional[str] = None


@dataclass
class PipelineResult:
    requirement: str
    user_story: SkillResult
    qa_cases: SkillResult
    architecture: SkillResult
