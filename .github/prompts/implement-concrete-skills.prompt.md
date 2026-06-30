---
name: implement-concrete-skills
description: Implementa ProductOwnerSkill, QASkill y ArchitectureSkill con sus prompts y respuestas mock siguiendo el patrón Strategy.
argument-hint: "Opcional: nombre de una sola skill a implementar"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit']
---

# Implementar las tres skills concretas (`skills/`)

## Objetivo
Crear las tres estaciones del pipeline, cada una con su prompt y su `_mock_response`,
respetando la misma firma `run(requirement, context)`.

## Entrada esperada
- Opcionalmente, el nombre de una sola skill. Si no, implementar las tres.

## Contexto del repositorio
- #file:../../docs/06_skills.md
- #file:../../docs/05_pipeline.md
- #file:../../docs/02_patterns.md
- #file:../../docs/03_folder_structure.md
- #file:../../docs/04_models.md

## Pasos obligatorios
1. `ProductOwnerSkill` (`skill_name="product_owner"`, `prompt_filename="product_owner.md"`): ignora `context`; produce una historia de usuario con criterios de aceptación.
2. `QASkill` (`skill_name="qa"`, `prompt_filename="qa.md"`): usa `context` = historia de usuario; produce casos de prueba críticos.
3. `ArchitectureSkill` (`skill_name="architecture"`, `prompt_filename="architecture.md"`): usa `context` = historia + casos; produce recomendación arquitectónica.
4. Cada una llama a `super().__init__(...)`, implementa `run()` (con `try/except AIProxyError` -> mock) y `_mock_response()` (`is_mock=True`).
5. Crear/completar los prompts de runtime correspondientes en `prompts/`.

## Criterios de salida
- Las tres heredan de `BaseSkill` y devuelven siempre `SkillResult`.
- Cada `run()` respeta el contrato de no propagar excepciones.

## Restricciones
- No llamar a la red directamente: siempre vía `self.ai_client`.
- Mantener idéntica la firma `run(requirement, context="")` en las tres.
