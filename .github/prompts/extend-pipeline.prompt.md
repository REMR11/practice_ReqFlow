---
name: extend-pipeline
description: Añade una skill nueva al pipeline (modelo, skill, orquestador y tests) sin romper los contratos existentes.
argument-hint: "Nombre y propósito de la nueva skill, ej. 'SecuritySkill: analiza riesgos de seguridad'"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit', 'run/terminal']
---

# Extender el pipeline con una skill nueva

## Objetivo
Insertar una skill adicional en la cadena PO -> QA -> Arquitectura, decidiendo su
posición y el `context` que recibe, sin alterar el contrato base.

## Entrada esperada
- Nombre y propósito de la nueva skill tras `/extend-pipeline`.

## Contexto del repositorio
- #file:../../docs/05_pipeline.md
- #file:../../docs/06_skills.md
- #file:../../docs/04_models.md
- #file:../../docs/02_patterns.md
- #file:../../docs/08_testing.md
- #file:../../docs/03_folder_structure.md

## Pasos obligatorios
1. Crear `NuevaSkill(BaseSkill)` siguiendo el patrón de las skills concretas (prompt propio + `_mock_response`).
2. Crear su prompt de runtime en `prompts/`.
3. Decidir en qué punto del pipeline se inserta y qué `context` acumulado recibe.
4. Agregar el campo correspondiente a `PipelineResult` y la línea en `RequirementPipeline.execute()`.
5. Actualizar la presentación (`MarkdownFormatter` / `main.py`) si debe mostrarse.
6. Agregar pruebas para la nueva skill y para la acumulación de `context` actualizada.

## Criterios de salida
- La nueva skill respeta la firma `run(requirement, context="")` y devuelve `SkillResult`.
- No se modifican `BaseSkill`, `AIProxyClient` ni `PromptLoader`.

## Restricciones
- No romper los contratos `SkillResult` / `PipelineResult` existentes.
- Mantener el orden de dependencias y la degradación elegante.
