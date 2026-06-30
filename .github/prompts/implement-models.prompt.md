---
name: implement-models
description: Implementa models/schemas.py con las dataclasses SkillResult y PipelineResult según el contrato documentado.
argument-hint: "Sin argumentos; opcionalmente matices sobre los campos"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit']
---

# Implementar la capa de datos (`models/schemas.py`)

## Objetivo
Crear las estructuras de datos puras que viajan por todo el sistema, sin lógica de
negocio.

## Entrada esperada
- Ninguna obligatoria. Es el paso 1 del orden de implementación.

## Contexto del repositorio
- #file:../../docs/04_models.md
- #file:../../docs/01_architecture.md
- #file:../../docs/02_patterns.md
- #file:../../docs/03_folder_structure.md

## Pasos obligatorios
1. Definir `SkillResult` con: `content: str`, `is_mock: bool`, `skill_name: str`, `error: str | None = None`.
2. Definir `PipelineResult` con: `requirement: str`, `user_story: SkillResult`, `qa_cases: SkillResult`, `architecture: SkillResult`.
3. Usar `@dataclass` y type hints completos.
4. No agregar métodos con lógica de negocio ni dependencias hacia otras capas.

## Criterios de salida
- `models/schemas.py` define exactamente esas dos dataclasses con esos campos y tipos.
- `error` tiene valor por defecto `None`.

## Restricciones
- La capa `models/` no debe importar nada de `core/`, `skills/`, `utils/` ni `main.py`.
- Respetar el contrato: ninguna skill debe devolver estructuras ad hoc fuera de `SkillResult`.
