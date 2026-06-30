---
name: scaffold-project
description: Crea el árbol de carpetas, los __init__.py y archivos stub del proyecto según la estructura objetivo documentada.
argument-hint: "Opcional: ruta raíz donde generar el scaffold (por defecto la raíz del repo)"
agent: agent
tools: ['search/codebase', 'edit/createFile']
---

# Scaffolding inicial del proyecto

## Objetivo
Crear la estructura de carpetas y archivos vacíos (stubs) del proyecto, lista para
empezar a implementar en el orden recomendado.

## Entrada esperada
- Opcionalmente, la ruta raíz. Si no se indica, usar la raíz del repositorio.

## Contexto del repositorio
- #file:../../docs/03_folder_structure.md
- #file:../../docs/00_overview.md
- #file:../../docs/01_architecture.md

## Pasos obligatorios
1. Crear las carpetas `skills/`, `core/`, `models/`, `prompts/`, `utils/`.
2. Crear los `__init__.py` en cada paquete Python (`skills/`, `core/`, `models/`, `utils/`).
3. Crear los stubs de módulos: `main.py`, `models/schemas.py`, `core/ai_proxy_client.py`, `core/prompt_loader.py`, `core/pipeline.py`, `skills/base_skill.py`, `skills/product_owner_skill.py`, `skills/qa_skill.py`, `skills/architecture_skill.py`, `utils/formatter.py`.
4. Crear los prompts de runtime vacíos: `prompts/product_owner.md`, `prompts/qa.md`, `prompts/architecture.md`.
5. Añadir en cada stub un docstring con su responsabilidad y un `TODO` que enlace al doc correspondiente.

## Criterios de salida
- El árbol coincide exactamente con el descrito en `docs/03_folder_structure.md`.
- No hay lógica todavía; solo stubs con docstrings y `TODO`.

## Restricciones
- No mezclar responsabilidades entre capas.
- Mantener la separación entre `.github/prompts/` (workflow) y `prompts/` (system prompts de runtime).
