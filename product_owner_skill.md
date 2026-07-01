# Guía de comentarios para skills/product_owner_skill.py

## Dónde implementar

| Campo | Valor |
|-------|-------|
| **Archivo a completar** | [`skills/product_owner_skill.py`](skills/product_owner_skill.py) |
| **Capa** | Skills (`skills/`) |
| **Orden sugerido** | 3 — después de `skills/base_skill.py` (ya implementado; no modificar en este ejercicio) |
| **Hereda de** | [`skills/base_skill.py`](skills/base_skill.py) |
| **Prompt que carga** | [`prompts/product_owner.md`](prompts/product_owner.md) |
| **Skills similares (referencia)** | [`skills/qa_skill.py`](skills/qa_skill.py), [`skills/architecture_skill.py`](skills/architecture_skill.py) |
| **Documentación de referencia** | [`docs/06_skills.md`](docs/06_skills.md) |

Los archivos `.py` **no fueron eliminados**. Abre `skills/product_owner_skill.py` en el editor, pega los comentarios de abajo encima de cada método y completa el código con autocompletado.

Esta skill es la **primera estación** del pipeline: genera la historia de usuario. No reimplementa `run()` — eso lo hace `BaseSkill`.

```python
# Método utilizado para configurar la skill de Product Owner con su nombre y archivo de prompt.
# Debe llamar a super().__init__() pasando los valores fijos de esta skill.
# Parametro ai_client: cliente de IA inyectado; None para crear uno por defecto.
# Parametro prompt_loader: cargador de prompts inyectado; None para crear uno por defecto.
# Debe fijar skill_name="product_owner" y prompt_filename="product_owner.md".
# BaseSkill se encargará de cargar el prompt y preparar run(); esta clase solo configura la identidad.
def __init__(
    self,
    ai_client: AIProxyClient | None = None,
    prompt_loader: PromptLoader | None = None,
) -> None:
    pass
```

```python
# Método utilizado para devolver una respuesta de ejemplo cuando no hay IA disponible o falla el proxy.
# Debe construir un texto Markdown con historia de usuario y criterios de aceptación.
# Parametro requirement: texto original del usuario; incluirlo en la historia ("Como usuario, quiero {requirement}...").
# Debe incluir sección "### Historia de Usuario" y "### Criterios de Aceptacion" con al menos 2-3 bullets.
# Debe retornar SkillResult con is_mock=True, skill_name=self.skill_name y error=None.
# Retorna: SkillResult con contenido de ejemplo listo para mostrar en pantalla.
def _mock_response(self, requirement: str) -> SkillResult:
    pass
```

## Versión corta para usar como comentario

```python
# Método utilizado para configurar la skill de Product Owner con su nombre y archivo de prompt.
# Debe llamar a super().__init__() con skill_name="product_owner" y prompt_filename="product_owner.md".

# Método utilizado para devolver una respuesta de ejemplo cuando no hay IA disponible o falla el proxy.
# Debe retornar SkillResult con historia de usuario en Markdown e is_mock=True.
```
