---
name: write-tests
description: Genera la suite pytest con dobles de prueba e inyección de dependencias, cubriendo el contrato de cada componente.
argument-hint: "Opcional: componente a testear, ej. 'pipeline' o 'ai_proxy_client'"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit', 'run/terminal']
---

# Generar la suite de pruebas (`tests/`)

## Objetivo
Crear pruebas con `pytest` que aprovechen la inyección de dependencias y la
degradación elegante, sin depender de red real.

## Entrada esperada
- Opcionalmente, el componente concreto a testear. Si no, generar la suite completa.

## Contexto del repositorio
- #file:../../docs/08_testing.md
- #file:../../docs/02_patterns.md
- #file:../../docs/04_models.md
- #file:../../docs/07_interfaces.md
- #file:../../docs/06_skills.md
- #file:../../docs/05_pipeline.md
- #file:../../docs/01_architecture.md

## Pasos obligatorios
1. Crear `tests/` con `conftest.py` y los archivos por componente (`test_models.py`, `test_ai_proxy_client.py`, `test_prompt_loader.py`, `test_base_skill.py`, `test_skills.py`, `test_pipeline.py`, `test_formatter.py`).
2. Implementar dobles `FakeAIClient` y `FixedSkill` como en la documentación.
3. Cubrir como mínimo:
   - `AIProxyClient`: sin credenciales -> `is_available is False`; `complete()` con HTTP simulado; `AIProxyError` en fallo.
   - `PromptLoader`: resolución con `Path(__file__)`, `PromptNotFoundError`.
   - `BaseSkill`/skills: fallback a mock, `run()` nunca propaga excepción.
   - `RequirementPipeline`: orden y acumulación de `context`.
   - `MarkdownFormatter`: salida normal, mock y error.
4. Aislar variables de entorno con `monkeypatch`.
5. Ejecutar `pytest` y dejar la suite en verde.

## Criterios de salida
- Pruebas deterministas, sin red real.
- Todos los casos clave del doc de testing quedan cubiertos.

## Restricciones
- Usar solo `pytest`, `monkeypatch` y `unittest.mock`.
- No alterar el código de producción salvo que un test revele un incumplimiento del contrato.
