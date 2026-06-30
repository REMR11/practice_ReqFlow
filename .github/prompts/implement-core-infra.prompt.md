---
name: implement-core-infra
description: Implementa AIProxyClient, PromptLoader y sus excepciones en core/, con degradación elegante y resolución de rutas robusta.
argument-hint: "Sin argumentos"
agent: agent
tools: ['search/codebase', 'edit/createFile', 'edit']
---

# Implementar la infraestructura compartida (`core/`)

## Objetivo
Crear las piezas reutilizadas por todas las skills: el cliente del proxy de IA y el
cargador de prompts, junto con sus excepciones.

## Entrada esperada
- Ninguna obligatoria. Es el paso 2 del orden de implementación.

## Contexto del repositorio
- #file:../../docs/07_interfaces.md
- #file:../../docs/02_patterns.md
- #file:../../docs/01_architecture.md
- #file:../../docs/03_folder_structure.md

## Pasos obligatorios
1. `core/ai_proxy_client.py`:
   - `AIProxyClient.__init__(proxy_url=None, proxy_api_key=None, timeout=30.0)` que lee `AI_PROXY_URL` / `AI_PROXY_API_KEY` del entorno si faltan.
   - Calcular `is_available` y **no lanzar** si faltan credenciales (degradación elegante).
   - `complete(system_prompt, user_message, max_tokens=1000) -> str` que hace el POST HTTP, valida el status y extrae solo el texto.
   - Definir `AIProxyError(Exception)`.
2. `core/prompt_loader.py`:
   - `PromptLoader.__init__(prompts_dir=None)` resolviendo con `Path(__file__).resolve().parent.parent / "prompts"`.
   - `load(prompt_filename) -> str` con `encoding="utf-8"`.
   - Definir `PromptNotFoundError(Exception)` cuando el archivo no exista.

## Criterios de salida
- `AIProxyClient` nunca lanza en `__init__`; `complete()` lanza `AIProxyError` ante fallo HTTP/timeout.
- `PromptLoader` resuelve rutas relativas a su propio archivo, no al CWD.

## Restricciones
- `core/` solo puede depender de `models/` y librerías externas (`requests`, `pathlib`).
- `AIProxyClient` es el único punto de salida hacia la IA.
