# 05 - El orquestador (`core/pipeline.py`)

| Anterior | Siguiente |
|----------|-----------|
| [04_models](04_models.md) | [06_skills](06_skills.md) |

---

## `class RequirementPipeline`

Coordina la ejecución secuencial de las 3 skills. Esta clase materializa la regla
"PO -> QA -> Arquitectura, cada una depende del output previo".

**Atributos de instancia:**

| Atributo | Tipo | Descripción |
|---|---|---|
| `product_owner_skill` | `ProductOwnerSkill` | Instancia inyectada o creada por defecto |
| `qa_skill` | `QASkill` | Instancia inyectada o creada por defecto |
| `architecture_skill` | `ArchitectureSkill` | Instancia inyectada o creada por defecto |

### `__init__(self, product_owner_skill=None, qa_skill=None, architecture_skill=None) -> None`

- Si cualquiera es `None`, instancia la clase concreta por defecto (cada una creará su propio `AIProxyClient` y `PromptLoader` si tampoco se le pasan).
- Esto permite tanto uso simple (`RequirementPipeline()`) como inyección de dependencias para tests (ver [08_testing](08_testing.md)).

### `execute(self, requirement: str) -> PipelineResult`

Lógica interna, en cuatro pasos:

```python
user_story_result = self.product_owner_skill.run(requirement, context="")
qa_result = self.qa_skill.run(requirement, context=user_story_result.content)
combined_context = f"{user_story_result.content}\n\n{qa_result.content}"
architecture_result = self.architecture_skill.run(requirement, context=combined_context)
return PipelineResult(
    requirement=requirement,
    user_story=user_story_result,
    qa_cases=qa_result,
    architecture=architecture_result,
)
```

Fíjate que esta función **no sabe nada** sobre cómo funciona internamente cada
skill (no sabe si usan IA real o mock, no sabe cómo manejan errores). Solo sabe
que puede llamar a `.run()` en cualquiera de las tres y va a recibir un
`SkillResult` confiable. Esa ignorancia deliberada es justamente lo que hace que
el orquestador sea simple: apenas 5 líneas de lógica real.

**Importante:** ninguna llamada aquí está envuelta en `try/except` porque, por
contrato, `BaseSkill.run()` **nunca** lanza excepciones — siempre retorna un
`SkillResult`, incluso en caso de error (ver [06_skills](06_skills.md)). La
responsabilidad de manejar errores está concentrada en un solo lugar.

---

## Extender el pipeline en el futuro

Si quisieras agregar una cuarta skill (ej. `SecuritySkill` que analiza riesgos de
seguridad después de Arquitectura), el cambio sería:

1. Crear `SecuritySkill(BaseSkill)` siguiendo el mismo patrón de [06_skills](06_skills.md).
2. Agregar una línea más en `execute()`: `security_result = self.security_skill.run(requirement, context=combined_context_actualizado)`.
3. Agregar el campo correspondiente a `PipelineResult` (ver [04_models](04_models.md)).

No tocas nada de `BaseSkill`, `AIProxyClient` ni `PromptLoader` — esa es la ventaja
real de haber invertido en el patrón desde el inicio.
