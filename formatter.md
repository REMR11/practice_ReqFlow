# Guía de comentarios para utils/formatter.py

## Dónde implementar

| Campo | Valor |
|-------|-------|
| **Archivo a completar** | [`utils/formatter.py`](utils/formatter.py) |
| **Capa** | Presentación (`utils/`) |
| **Orden sugerido** | 4 — después de `models/schemas.py` (puede hacerse en paralelo con el pipeline) |
| **Depende de** | [`models/schemas.py`](models/schemas.py) (`SkillResult`, `PipelineResult`) |
| **Usado por** | [`utils/ui.py`](utils/ui.py), [`main.py`](main.py) |
| **Documentación de referencia** | [`docs/07_interfaces.md`](docs/07_interfaces.md) |

Los archivos `.py` **no fueron eliminados**. Abre `utils/formatter.py` en el editor, pega los comentarios de abajo encima de cada método y completa el código con autocompletado.

Esta guía está pensada para pegarse justo encima de los métodos principales, de forma que el editor pueda inferir mejor la intención. Esta clase convierte resultados del pipeline en texto Markdown para mostrar en Streamlit.

```python
# Método estático utilizado para convertir un SkillResult en un bloque Markdown con encabezado.
# Debe crear una lista de líneas empezando con "## {title}" y una línea vacía.
# Parametro result: SkillResult con content, is_mock y error.
# Parametro title: título de la sección, ej. "Historia de Usuario".
# Si result.error no es None: retornar solo el encabezado y un bloque "> Error: {mensaje}".
# Si result.is_mock es True: agregar la línea "> Generado en modo mock." antes del contenido.
# Debe agregar result.content al final y unir todas las líneas con "\\n".
# Retorna: str listo para pasar a st.markdown().
@staticmethod
def format_skill_result(result: SkillResult, title: str) -> str:
    pass
```

```python
# Método estático utilizado para formatear el PipelineResult completo (las tres secciones juntas).
# Debe llamar a format_skill_result tres veces, una por cada skill del pipeline.
# Sección 1: pipeline_result.user_story con título "Historia de Usuario".
# Sección 2: pipeline_result.qa_cases con título "Casos de Prueba".
# Sección 3: pipeline_result.architecture con título "Recomendacion Arquitectonica".
# Debe unir las tres secciones con el separador "\\n\\n---\\n\\n" entre cada una.
# Retorna: str con todo el informe concatenado (útil para descargar como .md).
@staticmethod
def format_pipeline_result(pipeline_result: PipelineResult) -> str:
    pass
```

## Versión corta para usar como comentario

```python
# Método estático utilizado para convertir un SkillResult en un bloque Markdown con encabezado.
# Debe manejar error, banner de mock y contenido; retornar str para st.markdown().

# Método estático utilizado para formatear el PipelineResult completo (las tres secciones juntas).
# Debe llamar format_skill_result tres veces y unir con separador ---.
```
