from models.schemas import PipelineResult, SkillResult


class MarkdownFormatter:
    @staticmethod
    def format_skill_result(result: SkillResult, title: str) -> str:
        lines = [f"## {title}", ""]

        if result.error:
            lines.append(f"> Error: {result.error}")
            return "\n".join(lines)

        if result.is_mock:
            lines.extend(["> Generado en modo mock.", ""])

        lines.append(result.content)
        return "\n".join(lines)

    @staticmethod
    def format_pipeline_result(pipeline_result: PipelineResult) -> str:
        sections = [
            MarkdownFormatter.format_skill_result(
                pipeline_result.user_story, "Historia de Usuario"
            ),
            MarkdownFormatter.format_skill_result(
                pipeline_result.qa_cases, "Casos de Prueba"
            ),
            MarkdownFormatter.format_skill_result(
                pipeline_result.architecture, "Recomendacion Arquitectonica"
            ),
        ]
        return "\n\n---\n\n".join(sections)
