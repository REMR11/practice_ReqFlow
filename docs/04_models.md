# 04 - Modelos de datos (`models/schemas.py`)

| Anterior | Siguiente |
|----------|-----------|
| [03_folder_structure](03_folder_structure.md) | [05_pipeline](05_pipeline.md) |

---

Estas son las dos estructuras que viajan por todo el sistema. No tienen lógica,
solo guardan datos — son como "formularios" con campos fijos.

---

## `class SkillResult`

Es el formulario que **toda** skill debe llenar al terminar su trabajo, sin
excepción. Es el tipo de retorno estandarizado de `run()`.

| Atributo | Tipo | Descripción |
|---|---|---|
| `content` | `str` | Texto en Markdown, listo para renderizar |
| `is_mock` | `bool` | `True` si se generó sin IA real (respuesta de ejemplo) |
| `skill_name` | `str` | Identificador legible (`"product_owner"`, `"qa"`, `"architecture"`) |
| `error` | `str \| None` | Mensaje de error si algo falló de forma controlada, `None` si OK |

¿Por qué obligar a todas las skills a devolver exactamente esta forma, en vez de
dejar que cada una devuelva lo que quiera? Porque así el resto del sistema
(`main.py`, el formateador) puede tratar el resultado de cualquier skill de la
misma manera, sin necesidad de preguntarse "¿esto vino de QA o de Arquitectura?".
Esta idea —que cualquier pieza que cumpla el mismo contrato puede tratarse de
forma intercambiable— es la base de prácticamente todo el diseño orientado a
objetos.

- **Usado por**: `BaseSkill.run()` (tipo de retorno), `RequirementPipeline`, `main.py`, `MarkdownFormatter`.

---

## `class PipelineResult`

Es el "informe final" que junta los tres `SkillResult` (uno por skill) más el
`requirement` original. `main.py` solo necesita este único objeto para renderizar
las tres secciones en pantalla.

| Atributo | Tipo | Descripción |
|---|---|---|
| `requirement` | `str` | Requerimiento original ingresado por el usuario |
| `user_story` | `SkillResult` | Resultado de `ProductOwnerSkill` |
| `qa_cases` | `SkillResult` | Resultado de `QASkill` |
| `architecture` | `SkillResult` | Resultado de `ArchitectureSkill` |

- **Usado por**: `RequirementPipeline.execute()` (retorno), `main.py` (para renderizar las 3 secciones). Ver [05_pipeline](05_pipeline.md).
