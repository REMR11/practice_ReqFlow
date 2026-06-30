---
description: Instrucciones globales para el repositorio schema y su arquitectura de pipeline de requisitos.
applyTo: "**/*.{py,md}"
---

<!-- Tip: Use /create-instructions in chat to generate content with agent assistance -->

# Instrucciones del proyecto schema

## Contexto general del sistema
- El proyecto recibe un requisito en texto libre y lo convierte en tres artefactos secuenciales:
  1. historia de usuario,
  2. casos de prueba,
  3. recomendación arquitectónica.
- La orquestación principal debe seguir el flujo PO -> QA -> Arquitectura, donde cada etapa recibe el contexto acumulado de las anteriores.

## Arquitectura y patrones que deben preservarse
- Mantener una arquitectura en capas con dirección clara:
  - `main.py` -> `core/pipeline.py` -> `skills/` -> `core/ai_proxy_client.py`, `core/prompt_loader.py` -> `models/schemas.py`.
- Respetar los patrones documentados:
  - **Pipeline**: `RequirementPipeline` coordina una secuencia de steps intercambiables.
  - **Strategy**: cada skill expone la misma interfaz `run(requirement, context)`.
  - **Template Method**: `BaseSkill` define el esqueleto común y las subclases completan los detalles.
  - **Proxy**: `AIProxyClient` encapsula el acceso a la IA y evita filtrar dependencias externas.
- Evitar dependencias circulares. Si una modificación introduce una importación "hacia arriba", revisar el diseño antes de continuar.

## Contratos de datos obligatorios
- `SkillResult` debe seguir el contrato definido en `models/schemas.py`:
  - `content: str`
  - `is_mock: bool`
  - `skill_name: str`
  - `error: str | None`
- `PipelineResult` debe reunir:
  - `requirement`
  - `user_story`
  - `qa_cases`
  - `architecture`
- Las skills no deben devolver estructuras ad hoc; deben respetar `SkillResult` como salida estándar.

## Reglas de implementación
- `BaseSkill` debe actuar como contrato seguro para el pipeline:
  - si la IA no está disponible, usar respuesta mock;
  - si `AIProxyClient` falla, caer a mock;
  - no propagar excepciones hacia `main.py` ni hacia `RequirementPipeline`.
- `RequirementPipeline.execute()` debe orquestar en orden y acumular el contexto de forma explícita:
  - `user_story` para QA,
  - `user_story + qa_cases` para Arquitectura.
- `AIProxyClient` es el único punto de salida hacia el proveedor de IA; las skills no deben llamar directamente a la red.
- `PromptLoader` debe resolver rutas relativas al archivo del proyecto y cargar prompts desde `prompts/`.
- `MarkdownFormatter` debe manejar solo presentación; no mezclar lógica de negocio en `main.py` o en las skills.

## Convenciones de código y calidad
- Preferir inyección de dependencias por constructor para `AIProxyClient`, `PromptLoader`, y las skills, facilitando pruebas y reemplazo por doubles.
- Mantener el código DRY: compartir lógica común en `core/` y no duplicarla en cada skill.
- Cuando una skill falle, debe degradar elegantemente y seguir funcionando con un resultado mock bien definido.
- Las modificaciones deben respetar el orden de implementación recomendado y no romper el flujo de dependencias.

## Expectativas de pruebas
- Usar `pytest` y dobles de prueba por inyección de dependencias.
- Probar especialmente:
  - fallback a mock cuando no hay IA disponible,
  - manejo de `AIProxyError`,
  - acumulación correcta del `context`,
  - formato de `MarkdownFormatter`,
  - resolución de prompts y carga de variables de entorno.
- No depender de red real en pruebas; aislar entorno con `monkeypatch` cuando sea necesario.

## Criterio de aceptación para cambios
- Un cambio es correcto si mantiene el patrón de arquitectura, preserva el contrato de `SkillResult`, no introduce dependencias circulares, y conserva la capacidad de degradación elegante del sistema.
- Si una tarea requiere ampliar el pipeline, preferir agregar una skill nueva siguiendo el mismo patrón, en lugar de alterar el contrato base sin necesidad.