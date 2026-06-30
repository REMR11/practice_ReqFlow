# 06 - Skills (`skills/`)

| Anterior | Siguiente |
|----------|-----------|
| [05_pipeline](05_pipeline.md) | [07_interfaces](07_interfaces.md) |

---

## `class BaseSkill(ABC)`

Esta es la pieza más importante para entender el patrón **Template Method** (ver
[02_patterns](02_patterns.md)): define un esqueleto de pasos fijo, donde algunos
los implementa la clase base y otros los completa cada subclase.

`BaseSkill` es una **clase abstracta** (`ABC` en Python significa "Abstract Base
Class"). Nunca vas a crear una instancia de `BaseSkill` directamente — solo existe
para que otras clases hereden de ella. Es como un molde de galletas: el molde
define la forma general, pero cada galleta (cada skill concreta) tiene su propio
sabor.

**Atributos de instancia (heredados):**

| Atributo | Tipo | Descripción |
|---|---|---|
| `skill_name` | `str` | Fijado por la subclase en su `__init__` |
| `prompt_filename` | `str` | Nombre del archivo `.md`, fijado por la subclase |
| `system_prompt` | `str` | Cargado vía `PromptLoader` en `__init__` |
| `ai_client` | `AIProxyClient` | Instancia inyectada o creada por defecto |

### `__init__(self, skill_name, prompt_filename, ai_client=None, prompt_loader=None) -> None`

- Si `ai_client` es `None`, crea uno propio: `AIProxyClient()`.
- Si `prompt_loader` es `None`, crea uno propio: `PromptLoader()`.
- Intenta `self.system_prompt = prompt_loader.load(prompt_filename)`; si lanza `PromptNotFoundError`, asigna un prompt de respaldo genérico embebido en código (no rompe la skill).

### `run(self, requirement: str, context: str = "") -> SkillResult` *(abstracto)*

El contrato que toda subclase debe respetar es siempre el mismo:

1. Si el cliente de IA no está disponible (`is_available == False`), usar inmediatamente la respuesta mock.
2. Si está disponible, intentar llamar a la IA real dentro de `try/except AIProxyError`; si falla, caer también a la respuesta mock.
3. Nunca, bajo ninguna circunstancia, dejar que una excepción se escape hacia `main.py`. Cualquier error se convierte en un `SkillResult` con el campo `error` lleno.

Este último punto es clave: como `BaseSkill.run()` garantiza que nunca lanza
excepciones, `RequirementPipeline` no necesita envolver cada llamada en
`try/except` (ver [05_pipeline](05_pipeline.md)).

- **Parámetros:** `requirement` (texto original del usuario) y `context` (texto acumulado de outputs de skills previas, vacío `""` si es la primera).

### `_mock_response(self, requirement: str) -> SkillResult` *(abstracto)*

- Retorna un `SkillResult` con `is_mock=True` — una respuesta de ejemplo, en Markdown válido.
- **Usado por:** `run()` de la misma instancia, nunca desde fuera de la clase.

### `_build_user_message(self, requirement: str, context: str) -> str` *(concreto, compartido)*

- Combina ambos en un solo mensaje para `ai_client.complete()`. Si `context` está vacío, retorna solo `requirement`; si no, algo como `f"Requerimiento original:\n{requirement}\n\nContexto previo:\n{context}"`.

---

## Las tres skills concretas

`ProductOwnerSkill`, `QASkill` y `ArchitectureSkill` siguen exactamente el mismo
patrón estructural — la única diferencia es qué prompt cargan y qué hacen con el
`context`.

| Skill | ¿Usa el `context` recibido? | ¿Qué produce? |
|---|---|---|
| `ProductOwnerSkill` | No (es la primera, no hay nada previo) | Historia de usuario con criterios de aceptación |
| `QASkill` | Sí — recibe la historia de usuario completa | Lista de casos de prueba críticos |
| `ArchitectureSkill` | Sí — recibe historia de usuario + casos de prueba combinados | Recomendación de componentes y patrón arquitectónico |

Esta tabla es la prueba de que el patrón Strategy/Pipeline funciona: el "molde"
(`run(requirement, context)`) es idéntico en las tres, pero cada una decide
internamente qué tan relevante es el `context` para su trabajo.

Cada subclase llama en su `__init__` a `super().__init__(...)` fijando su
`skill_name` y su `prompt_filename` (`"product_owner.md"`, `"qa.md"`,
`"architecture.md"`), e implementa su propio `run()` y `_mock_response()`.

Cuando agregues una cuarta skill en el futuro, solo necesitas decidir en qué punto
del pipeline insertarla y qué `context` acumulado le vas a pasar — la forma general
ya está resuelta por `BaseSkill`. Ver [05_pipeline](05_pipeline.md).
