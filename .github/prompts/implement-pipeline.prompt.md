---
name: implement-pipeline
description: Implementa RequirementPipeline.execute() orquestando PO -> QA -> Arquitectura con acumulación explícita de contexto.
argument-hint: "Sin argumentos"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit']
---

# Implementar el orquestador (`core/pipeline.py`)

## Objetivo
Crear la clase que ejecuta las tres skills en orden, acumulando el `context` y
devolviendo un `PipelineResult`.

## Entrada esperada
- Ninguna obligatoria. Es el paso 5 del orden de implementación.

## Contexto del repositorio
- #file:../../docs/05_pipeline.md
- #file:../../docs/04_models.md
- #file:../../docs/01_architecture.md
- #file:../../docs/06_skills.md
- #file:../../docs/02_patterns.md

## Pasos obligatorios
1. `RequirementPipeline.__init__(product_owner_skill=None, qa_skill=None, architecture_skill=None)` instanciando las concretas por defecto si no se inyectan.
2. `execute(requirement) -> PipelineResult` en este orden exacto:
   - `user_story = product_owner_skill.run(requirement, context="")`
   - `qa = qa_skill.run(requirement, context=user_story.content)`
   - `combined = f"{user_story.content}\n\n{qa.content}"`
   - `architecture = architecture_skill.run(requirement, context=combined)`
   - retornar `PipelineResult(requirement, user_story, qa, architecture)`.

## Criterios de salida
- El contexto crece según lo documentado (QA recibe historia; Arquitectura recibe historia + casos).
- No hay `try/except` alrededor de las llamadas a `.run()`.

## Restricciones
- El pipeline no debe conocer detalles internos de las skills (mock vs IA real).
- `core/pipeline.py` depende de `skills/` y `models/`, nunca de `main.py`.
