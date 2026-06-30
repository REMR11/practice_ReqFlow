from dotenv import load_dotenv
import streamlit as st

from core.pipeline import RequirementPipeline
from models.schemas import PipelineResult
from utils.formatter import MarkdownFormatter

load_dotenv()


@st.cache_resource
def get_pipeline() -> RequirementPipeline:
    return RequirementPipeline()


def render_results(pipeline_result: PipelineResult) -> None:
    st.markdown(
        MarkdownFormatter.format_skill_result(
            pipeline_result.user_story, "Historia de Usuario"
        ),
        unsafe_allow_html=False,
    )
    st.markdown(
        MarkdownFormatter.format_skill_result(
            pipeline_result.qa_cases, "Casos de Prueba"
        ),
        unsafe_allow_html=False,
    )
    st.markdown(
        MarkdownFormatter.format_skill_result(
            pipeline_result.architecture, "Recomendacion Arquitectonica"
        ),
        unsafe_allow_html=False,
    )


def main() -> None:
    st.set_page_config(page_title="ReqFlow", page_icon="🧩", layout="wide")
    st.title("ReqFlow")
    st.caption("PO -> QA -> Arquitectura")

    requirement = st.text_area(
        "Escribe el requerimiento",
        placeholder="Ejemplo: Quiero login con Google en la pagina de inicio.",
        height=180,
    )

    if st.button("Generar artefactos", type="primary"):
        if not requirement.strip():
            st.warning("Ingresa un requerimiento antes de continuar.")
            return

        with st.spinner("Analizando requerimiento..."):
            pipeline_result = get_pipeline().execute(requirement.strip())

        render_results(pipeline_result)


if __name__ == "__main__":
    main()
