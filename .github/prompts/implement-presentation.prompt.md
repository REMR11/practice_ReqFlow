---
name: implement-presentation
description: Implementa MarkdownFormatter y la app Streamlit (main.py) manteniendo la separación entre negocio y presentación.
argument-hint: "Sin argumentos"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit']
---

# Implementar la capa de presentación (`utils/formatter.py` y `main.py`)

## Objetivo
Crear el formateador a Markdown y la app Streamlit que orquesta la interacción del
usuario.

## Entrada esperada
- Ninguna obligatoria. Son los pasos 6-7 del orden de implementación.

## Contexto del repositorio
- #file:../../docs/07_interfaces.md
- #file:../../docs/02_patterns.md
- #file:../../docs/04_models.md
- #file:../../docs/01_architecture.md
- #file:../../docs/03_folder_structure.md

## Pasos obligatorios
1. `utils/formatter.py` con `MarkdownFormatter` y métodos `@staticmethod`:
   - `format_skill_result(result, title) -> str`: encabezado `## {title}`, banner si `is_mock`, bloque de error si `error` no es `None`, si no el `content`.
   - `format_pipeline_result(pipeline_result) -> str`: concatena las tres secciones separadas por `---`.
2. `main.py` con funciones de módulo (no clases):
   - `get_pipeline() -> RequirementPipeline` decorada con `@st.cache_resource`.
   - `render_results(pipeline_result) -> None` que usa `MarkdownFormatter` y `st.markdown(..., unsafe_allow_html=False)`.
   - `main() -> None` con `st.text_area`, botón de envío, llamada a `get_pipeline().execute(...)` y `render_results(...)`.

## Criterios de salida
- El formateador no contiene lógica de negocio.
- `main.py` solo consume `RequirementPipeline`, `MarkdownFormatter` y `PipelineResult`.

## Restricciones
- No mezclar lógica de negocio en la capa de presentación.
- Respetar el flujo de dependencias `main -> pipeline -> ...`.
