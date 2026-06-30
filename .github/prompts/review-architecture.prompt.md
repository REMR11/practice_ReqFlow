---
name: review-architecture
description: Audita el código existente contra las capas, el grafo de dependencias y el diagrama UML documentados.
argument-hint: "Opcional: archivo o módulo a auditar"
agent: plan
tools: ['search/codebase']
---

# Auditoría de arquitectura

## Objetivo
Verificar que el código respeta la arquitectura en capas, los contratos y los
patrones documentados, sin modificar nada todavía.

## Entrada esperada
- Opcionalmente, el archivo o módulo a auditar. Si no, auditar todo el proyecto.

## Contexto del repositorio
- #file:../../docs/00_overview.md
- #file:../../docs/01_architecture.md
- #file:../../docs/02_patterns.md
- #file:../../docs/07_interfaces.md
- #file:../../docs/05_pipeline.md
- #file:../../docs/06_skills.md
- #file:../../.github/instructions/copilot.instructions.md

## Pasos obligatorios
1. Verificar el flujo de dependencias `main -> pipeline -> skills -> (base_skill, ai_proxy_client, prompt_loader) -> models` y detectar cualquier importación "hacia arriba".
2. Confirmar que las skills devuelven siempre `SkillResult` y que `run()` nunca propaga excepciones.
3. Confirmar que `RequirementPipeline.execute()` acumula el `context` correctamente.
4. Confirmar que `AIProxyClient` es el único punto de salida a la IA y que aplica degradación elegante.
5. Comparar la estructura real contra el diagrama UML de `docs/07_interfaces.md`.

## Criterios de salida
- Un informe en Markdown con: cumplimientos, incumplimientos (con archivo y línea) y recomendaciones priorizadas.

## Restricciones
- Modo solo lectura: no editar código.
- Señalar dependencias circulares como bloqueantes.
