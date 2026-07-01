from dotenv import load_dotenv
import streamlit as st

from core.pipeline import RequirementPipeline
from models.schemas import PipelineResult
from utils.ui import (
    inject_theme_css,
    render_header,
    render_metrics_row,
    render_proxy_status,
    render_results_tabs,
)

load_dotenv()


@st.cache_resource
def get_pipeline() -> RequirementPipeline:
    return RequirementPipeline()


def _init_session_state() -> None:
    if "pipeline_result" not in st.session_state:
        st.session_state.pipeline_result = None


def main() -> None:
    st.set_page_config(page_title="ReqFlow", page_icon="🧩", layout="wide")
    _init_session_state()

    inject_theme_css()
    render_header()

    pipeline = get_pipeline()
    render_proxy_status(pipeline.product_owner_skill.ai_client)

    with st.container(border=True):
        st.subheader("Requerimiento")
        requirement = st.text_area(
            "Escribe el requerimiento",
            placeholder="Ejemplo: Quiero login con Google en la pagina de inicio.",
            height=180,
            label_visibility="collapsed",
        )
        generate = st.button("Generar artefactos", type="primary")

    if generate:
        if not requirement.strip():
            st.warning("Ingresa un requerimiento antes de continuar.")
            return

        with st.spinner("Analizando requerimiento (PO → QA → Arquitectura)..."):
            st.session_state.pipeline_result = pipeline.execute(requirement.strip())

    pipeline_result: PipelineResult | None = st.session_state.pipeline_result
    if pipeline_result is None:
        st.info("Escribe un requerimiento y pulsa **Generar artefactos** para comenzar.")
        return

    st.subheader("Resultados")
    render_metrics_row(pipeline_result)
    render_results_tabs(pipeline_result)


if __name__ == "__main__":
    main()
