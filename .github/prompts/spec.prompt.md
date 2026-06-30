---
name: spec
description: Genera una especificación técnica de una funcionalidad alineada con la arquitectura del pipeline PO -> QA -> Arquitectura antes de programar.
argument-hint: "Funcionalidad o cambio a especificar, ej. 'agregar SecuritySkill'"
agent: plan
tools: ['search/codebase']
---

# Especificación técnica previa a implementar

## Objetivo
Producir una especificación breve y accionable de la funcionalidad pedida,
respetando la arquitectura en capas y los contratos ya documentados, **sin
escribir código todavía**.

## Entrada esperada
- La funcionalidad o cambio descrito por el usuario tras `/spec`.

## Contexto del repositorio
Lee y respeta estos documentos antes de especificar:
- #file:../../docs/00_overview.md
- #file:../../docs/01_architecture.md
- #file:../../docs/02_patterns.md
- #file:../../.github/instructions/copilot.instructions.md

## Pasos obligatorios
1. Resume el objetivo de la funcionalidad en 1-2 frases.
2. Identifica qué capas y archivos se ven afectados (`models/`, `core/`, `skills/`, `utils/`, `main.py`).
3. Define el impacto sobre los contratos `SkillResult` / `PipelineResult` si lo hay.
4. Enumera riesgos: dependencias circulares, ruptura de la degradación elegante, fuga de excepciones.
5. Propón un plan de pasos ordenado según el flujo `main -> pipeline -> skills -> core -> models`.

## Criterios de salida
- Una especificación en Markdown con secciones: Objetivo, Archivos afectados, Contratos, Riesgos, Plan de pasos.
- Sin código de implementación (solo firmas/pseudocódigo si es imprescindible).

## Restricciones
- Preservar los patrones Pipeline, Strategy, Template Method y Proxy.
- No introducir dependencias "hacia arriba" en la jerarquía de capas.
