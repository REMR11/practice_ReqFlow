---
name: implement-base-skill
description: Implementa BaseSkill (Template Method) con el contrato de run() que nunca lanza excepciones y degrada a mock.
argument-hint: "Sin argumentos"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit']
---

# Implementar la clase base de skills (`skills/base_skill.py`)

## Objetivo
Crear el contrato abstracto del que heredan todas las skills, concentrando el
manejo de errores y el fallback a mock en un solo lugar.

## Entrada esperada
- Ninguna obligatoria. Es el paso 3 del orden de implementación.

## Contexto del repositorio
- #file:../../docs/06_skills.md
- #file:../../docs/02_patterns.md
- #file:../../docs/04_models.md
- #file:../../docs/07_interfaces.md
- #file:../../docs/05_pipeline.md

## Pasos obligatorios
1. Definir `BaseSkill(ABC)` con atributos `skill_name`, `prompt_filename`, `system_prompt`, `ai_client`.
2. `__init__(skill_name, prompt_filename, ai_client=None, prompt_loader=None)`:
   - crear `AIProxyClient()` / `PromptLoader()` por defecto si no se inyectan;
   - cargar `system_prompt`; ante `PromptNotFoundError`, usar un prompt de respaldo embebido.
3. Declarar `run(requirement, context="") -> SkillResult` como **abstracto**.
4. Declarar `_mock_response(requirement) -> SkillResult` como **abstracto**.
5. Implementar `_build_user_message(requirement, context) -> str` concreto y compartido.
6. Documentar el contrato de `run()`: IA no disponible -> mock; `AIProxyError` -> mock; nunca propagar excepciones (convertir a `SkillResult(error=...)`).

## Criterios de salida
- `BaseSkill` no es instanciable directamente.
- El contrato garantiza que `run()` nunca lanza, habilitando un pipeline sin `try/except`.

## Restricciones
- Usar inyección de dependencias por constructor.
- No duplicar lógica que ya vive en `core/`.
