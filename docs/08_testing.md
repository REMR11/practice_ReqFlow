# 08 - Estrategia de pruebas

| Anterior | Siguiente |
|----------|-----------|
| [07_interfaces](07_interfaces.md) | — |

Esta guía es **prescriptiva**: describe qué probar y cómo, aprovechando dos
decisiones de diseño que hacen el sistema muy testeable —la **inyección de
dependencias** (puedes pasar dobles de prueba por constructor) y la **degradación
elegante** (el sistema tiene un comportamiento mock bien definido cuando no hay
IA). Ver [02_patterns](02_patterns.md).

---

## Estructura sugerida

```
tests/
├── __init__.py
├── conftest.py                 # fixtures compartidas (clientes fake, monkeypatch de env)
├── test_models.py
├── test_ai_proxy_client.py
├── test_prompt_loader.py
├── test_base_skill.py
├── test_skills.py
├── test_pipeline.py
└── test_formatter.py
```

Herramientas recomendadas: `pytest` como runner y `monkeypatch` / `unittest.mock`
(ambos sin dependencias extra) para aislar red y variables de entorno.

---

## Qué probar por componente

### `models/schemas.py` ([04_models](04_models.md))

- Construcción de `SkillResult` y `PipelineResult` con sus campos.
- Valor por defecto de `error` (`None`) cuando no se pasa.

### `AIProxyClient` ([07_interfaces](07_interfaces.md))

- Sin credenciales (`monkeypatch.delenv` de `AI_PROXY_URL` / `AI_PROXY_API_KEY`) -> `is_available is False`, y `__init__` no lanza.
- Con credenciales presentes -> `is_available is True`.
- `complete()` con respuesta HTTP simulada (mock de `requests.post`) -> devuelve solo el texto extraído, no el JSON crudo.
- Error HTTP, timeout o status inválido -> lanza `AIProxyError`.

### `PromptLoader` ([07_interfaces](07_interfaces.md))

- `prompts_dir` por defecto se resuelve con `Path(__file__)` y apunta a `prompts/` aunque cambies el directorio de trabajo (`monkeypatch.chdir`).
- `load("existe.md")` devuelve el contenido con `encoding="utf-8"`.
- `load("no_existe.md")` lanza `PromptNotFoundError`.

### `BaseSkill` y skills concretas ([06_skills](06_skills.md))

El contrato de `run()` es lo más importante a verificar:

- IA no disponible (`ai_client.is_available is False`) -> retorna `SkillResult` con `is_mock=True`, sin tocar la red.
- IA disponible pero `complete()` lanza `AIProxyError` -> cae a `_mock_response()` (`is_mock=True`).
- IA disponible y `complete()` responde bien -> `is_mock=False` y `content` con el texto de la IA.
- **`run()` nunca propaga excepciones**: ante cualquier fallo retorna un `SkillResult` (con `error` lleno si corresponde). Esta es la garantía de la que depende el pipeline.
- `_build_user_message()` con `context=""` devuelve solo el `requirement`; con `context` no vacío incluye ambos.

Ejemplo de doble de prueba para el cliente de IA:

```python
class FakeAIClient:
    def __init__(self, available=True, raises=False, text="respuesta IA"):
        self.is_available = available
        self._raises = raises
        self._text = text

    def complete(self, system_prompt, user_message, max_tokens=1000):
        if self._raises:
            raise AIProxyError("fallo simulado")
        return self._text
```

### `RequirementPipeline` ([05_pipeline](05_pipeline.md))

Aquí la inyección de dependencias brilla: pasa skills falsas que devuelvan
`SkillResult` fijos y verifica la orquestación sin IA ni prompts reales.

- Orden de ejecución PO -> QA -> Arquitectura.
- Acumulación de `context`: QA recibe `user_story.content`; Arquitectura recibe `user_story.content` + `qa_cases.content` combinados.
- `execute()` devuelve un `PipelineResult` con los tres resultados y el `requirement` original.

```python
class FixedSkill:
    def __init__(self, name):
        self.name = name
        self.received_context = None

    def run(self, requirement, context=""):
        self.received_context = context
        return SkillResult(content=f"{self.name}-out", is_mock=True,
                            skill_name=self.name, error=None)

def test_context_se_acumula():
    po, qa, arch = FixedSkill("po"), FixedSkill("qa"), FixedSkill("arch")
    pipeline = RequirementPipeline(po, qa, arch)
    pipeline.execute("un requerimiento")
    assert qa.received_context == "po-out"
    assert "po-out" in arch.received_context and "qa-out" in arch.received_context
```

### `MarkdownFormatter` ([07_interfaces](07_interfaces.md))

- Resultado normal -> incluye el encabezado (`## {title}`) y el `content`.
- `is_mock=True` -> incluye el banner de modo mock.
- `error` no `None` -> renderiza el bloque de error en lugar del contenido.
- `format_pipeline_result()` concatena las tres secciones separadas por `---`.

---

## Aislar variables de entorno

Como `AIProxyClient` lee `AI_PROXY_URL` y `AI_PROXY_API_KEY` del entorno, usa
`monkeypatch` para fijarlas o borrarlas por test, garantizando que la suite sea
determinista y no dependa de la máquina donde corre:

```python
def test_sin_credenciales(monkeypatch):
    monkeypatch.delenv("AI_PROXY_URL", raising=False)
    monkeypatch.delenv("AI_PROXY_API_KEY", raising=False)
    assert AIProxyClient().is_available is False
```
