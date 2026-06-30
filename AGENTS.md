# AGENTS.md — Brief para agente cloud

Este repositorio contiene la **documentación y el plano** de ReqFlow: una app
Streamlit que convierte un requerimiento en texto libre en tres artefactos Markdown
(historia de usuario, casos de prueba, recomendación arquitectónica) mediante un
pipeline PO -> QA -> Arquitectura.

**Tu trabajo:** implementar el código Python completo en esta rama (`preview`),
siguiendo la documentación en `docs/` y las reglas de este archivo.

---

## Objetivo y alcance

- Construir el proyecto descrito en [docs/00_overview.md](docs/00_overview.md).
- La app debe **funcionar sin credenciales de IA** (modo mock con respuestas de
  ejemplo).
- Con `AI_PROXY_URL` y `AI_PROXY_API_KEY` configurados, debe usar el proxy real.
- Incluir suite de pruebas `pytest` según [docs/08_testing.md](docs/08_testing.md).

---

## Orden de implementación (obligatorio)

Sigue [docs/03_folder_structure.md](docs/03_folder_structure.md). Cada paso solo
depende de lo ya construido:

| Paso | Archivo(s) | Doc de referencia |
|------|------------|-------------------|
| 1 | `models/schemas.py` | [docs/04_models.md](docs/04_models.md) |
| 2 | `core/ai_proxy_client.py`, `core/prompt_loader.py` | [docs/07_interfaces.md](docs/07_interfaces.md) |
| 3 | `skills/base_skill.py` | [docs/06_skills.md](docs/06_skills.md) + decisión BaseSkill abajo |
| 4 | `skills/product_owner_skill.py`, `qa_skill.py`, `architecture_skill.py` | [docs/06_skills.md](docs/06_skills.md) |
| 5 | `core/pipeline.py` | [docs/05_pipeline.md](docs/05_pipeline.md) |
| 6 | `utils/formatter.py` | [docs/07_interfaces.md](docs/07_interfaces.md) |
| 7 | `main.py` | [docs/07_interfaces.md](docs/07_interfaces.md) |
| 8 | `tests/` | [docs/08_testing.md](docs/08_testing.md) |

Árbol objetivo:

```
Proyecto/
├── main.py
├── models/schemas.py
├── core/ai_proxy_client.py, prompt_loader.py, pipeline.py
├── skills/base_skill.py, product_owner_skill.py, qa_skill.py, architecture_skill.py
├── prompts/product_owner.md, qa.md, architecture.md
├── utils/formatter.py
└── tests/
```

---

## Reglas de arquitectura (no negociables)

Fuente: [.github/instructions/copilot.instructions.md](.github/instructions/copilot.instructions.md)
y [docs/01_architecture.md](docs/01_architecture.md).

1. **Flujo de dependencias** (nunca al revés):
   `main -> pipeline -> skills -> (base_skill, ai_proxy_client, prompt_loader) -> models`
2. **Patrones:** Pipeline, Strategy, Template Method, Proxy, degradación elegante, DRY.
3. **Contratos de datos:**
   - `SkillResult`: `content`, `is_mock`, `skill_name`, `error`
   - `PipelineResult`: `requirement`, `user_story`, `qa_cases`, `architecture`
4. **Pipeline:** PO -> QA -> Arquitectura; el `context` crece en cada paso (ver
   [docs/05_pipeline.md](docs/05_pipeline.md)).
5. **`AIProxyClient`** es el **único** punto de salida HTTP hacia la IA.
6. **`RequirementPipeline.execute()`** no usa `try/except` alrededor de `.run()`.

---

## Decisión explícita: `BaseSkill.run()` (Template Method)

La documentación en [docs/06_skills.md](docs/06_skills.md) puede leerse como si
cada skill reimplementara `run()`. **Implementa así:**

| Método | Tipo | Responsabilidad |
|--------|------|-----------------|
| `BaseSkill.run()` | **Concreto** | 1) Si `not ai_client.is_available` -> `_mock_response()`; 2) Si disponible, `try ai_client.complete(...)` -> `SkillResult(is_mock=False)`; 3) `except AIProxyError` -> mock; 4) `except Exception` -> `SkillResult(error=...)`; **nunca lanzar** |
| `_mock_response()` | **Abstracto** | Cada subclase devuelve Markdown de ejemplo con `is_mock=True` |
| `_build_user_message()` | **Concreto** | Combina `requirement` + `context` (compartido en base) |

Las subclases (`ProductOwnerSkill`, `QASkill`, `ArchitectureSkill`) **no**
reimplementan `run()`. Solo configuran `skill_name`, `prompt_filename` en
`__init__` e implementan `_mock_response()`.

---

## Configuración del proxy de IA

Variables de entorno (ver [.env.example](.env.example)):

```bash
AI_PROXY_URL=https://kodigo-gpt-proxy.lemonsky-81239ee8.eastus.azurecontainerapps.io/v1
AI_PROXY_API_KEY=<tu-clave>
```

### `AIProxyClient` (`core/ai_proxy_client.py`)

- `__init__`: lee env con `os.getenv`; si faltan credenciales, `is_available = False` (**no lanzar**).
- `complete(system_prompt, user_message, max_tokens=1000) -> str`:
  - `POST {AI_PROXY_URL}/chat`
  - Header: `Authorization: Bearer {AI_PROXY_API_KEY}`
  - Body (formato OpenAI-compatible, verificar con una prueba real):

```json
{
  "messages": [
    {"role": "system", "content": "<system_prompt>"},
    {"role": "user", "content": "<user_message>"}
  ],
  "max_tokens": 1000
}
```

- Parsear la respuesta extrayendo el texto (campo probable:
  `choices[0].message.content`; **ajustar** si el proxy devuelve otro esquema).
- Ante error HTTP/timeout: lanzar `AIProxyError` (las skills lo capturan vía
  `BaseSkill.run()`).

Carga opcional de `.env` en `main.py` con `python-dotenv` (`load_dotenv()`).

---

## Prompts de runtime (`prompts/`)

Crear archivos mínimos (contenido placeholder; se refinarán después):

| Archivo | Rol |
|---------|-----|
| `prompts/product_owner.md` | Instrucciones para generar historia de usuario |
| `prompts/qa.md` | Instrucciones para casos de prueba |
| `prompts/architecture.md` | Instrucciones para recomendación arquitectónica |

`PromptLoader` resuelve rutas con `Path(__file__).resolve().parent.parent / "prompts"`.

---

## Entregables esperados

- [ ] Código completo según el árbol objetivo y el orden de implementación.
- [ ] `tests/` con pytest; sin red real (mocks, `monkeypatch`, dobles inyectados).
- [ ] README actualizado con: instalación, `.env`, `streamlit run main.py`, `pytest`.
- [ ] Modo mock funcional sin variables de entorno.
- [ ] Modo IA funcional con proxy configurado.

---

## Restricciones (qué NO hacer)

- **No** commitear `.env` ni API keys reales.
- **No** llamar a APIs de IA fuera de `AIProxyClient`.
- **No** devolver estructuras ad hoc; siempre `SkillResult` / `PipelineResult`.
- **No** introducir imports "hacia arriba" (dependencias circulares).
- **No** mezclar lógica de presentación en skills ni pipeline (`MarkdownFormatter` + `main.py`).
- **No** duplicar el esqueleto de `run()` en cada skill concreta.

---

## Comandos

```bash
# Instalar dependencias
pip install -r requirements.txt
# o: pip install -e ".[dev]"

# Configurar entorno (opcional, para IA real)
cp .env.example .env
# editar .env con tu API key

# Ejecutar la app
streamlit run main.py

# Ejecutar pruebas
pytest
```

---

## Documentación de referencia (leer en orden si hay dudas)

1. [docs/00_overview.md](docs/00_overview.md) — visión general
2. [docs/01_architecture.md](docs/01_architecture.md) — capas y dependencias
3. [docs/02_patterns.md](docs/02_patterns.md) — patrones de diseño
4. [docs/03_folder_structure.md](docs/03_folder_structure.md) — árbol y orden
5. [docs/04_models.md](docs/04_models.md) — dataclasses
6. [docs/05_pipeline.md](docs/05_pipeline.md) — orquestador
7. [docs/06_skills.md](docs/06_skills.md) — skills (usar decisión BaseSkill de arriba)
8. [docs/07_interfaces.md](docs/07_interfaces.md) — infraestructura, UML
9. [docs/08_testing.md](docs/08_testing.md) — estrategia de pruebas

Diagrama UML: secciones en [docs/07_interfaces.md](docs/07_interfaces.md).

Prompts de workflow VS Code (opcional): [.github/prompts/](.github/prompts/).
