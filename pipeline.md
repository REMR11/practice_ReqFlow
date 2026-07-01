# Guía de comentarios para core/pipeline.py

## Dónde implementar

| Campo | Valor |
|-------|-------|
| **Archivo a completar** | [`core/pipeline.py`](core/pipeline.py) |
| **Capa** | Infraestructura / Orquestador (`core/`) |
| **Orden sugerido** | 5 — después de las tres skills concretas |
| **Depende de** | [`skills/product_owner_skill.py`](skills/product_owner_skill.py), [`skills/qa_skill.py`](skills/qa_skill.py), [`skills/architecture_skill.py`](skills/architecture_skill.py) |
| **Retorna** | [`models/schemas.py`](models/schemas.py) → `PipelineResult` |
| **Usado por** | [`main.py`](main.py) |
| **Documentación de referencia** | [`docs/05_pipeline.md`](docs/05_pipeline.md) |

Los archivos `.py` **no fueron eliminados**. Abre `core/pipeline.py` en el editor, pega los comentarios de abajo encima de cada método y completa el código con autocompletado.

Esta clase **orquesta** el flujo PO → QA → Arquitectura y acumula el `context` en cada paso.

```python
# Método utilizado para inicializar el pipeline con las tres skills (Product Owner, QA, Arquitectura).
# Debe guardar cada skill en un atributo de instancia: product_owner_skill, qa_skill, architecture_skill.
# Parametro product_owner_skill: instancia inyectada; si es None, crear ProductOwnerSkill().
# Parametro qa_skill: instancia inyectada; si es None, crear QASkill().
# Parametro architecture_skill: instancia inyectada; si es None, crear ArchitectureSkill().
# Esto permite usar RequirementPipeline() en producción o inyectar skills falsas en tests.
def __init__(
    self,
    product_owner_skill: ProductOwnerSkill | None = None,
    qa_skill: QASkill | None = None,
    architecture_skill: ArchitectureSkill | None = None,
) -> None:
    pass
```

```python
# Método utilizado para ejecutar el pipeline completo sobre un requerimiento de texto.
# Debe llamar a las tres skills en orden y pasar el contexto acumulado de cada paso al siguiente.
# Parametro requirement: texto que escribió el usuario.
# Paso 1: product_owner_skill.run(requirement, context="") — primera skill, sin contexto previo.
# Paso 2: qa_skill.run(requirement, context=user_story_result.content) — QA recibe la historia de usuario.
# Paso 3: combinar user_story + qa en combined_context (separados por "\\n\\n").
# Paso 4: architecture_skill.run(requirement, context=combined_context) — Arquitectura recibe ambos outputs.
# Debe retornar PipelineResult con requirement, user_story, qa_cases y architecture.
# No usar try/except: BaseSkill.run() nunca lanza excepciones, siempre retorna SkillResult.
# Retorna: PipelineResult con los tres SkillResult y el requirement original.
def execute(self, requirement: str) -> PipelineResult:
    pass
```

## Versión corta para usar como comentario

```python
# Método utilizado para inicializar el pipeline con las tres skills (Product Owner, QA, Arquitectura).
# Debe guardar cada skill en un atributo; usar instancias por defecto si se recibe None.

# Método utilizado para ejecutar el pipeline completo sobre un requerimiento de texto.
# Debe llamar PO → QA → Arquitectura acumulando context y retornar PipelineResult.
```
