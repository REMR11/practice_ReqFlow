# Guía de comentarios para models/schemas.py

## Dónde implementar

| Campo | Valor |
|-------|-------|
| **Archivo a crear** | [`models/schemas.py`](models/schemas.py) |
| **Capa** | Datos (`models/`) |
| **Orden sugerido** | 1 — empieza aquí (no depende de nada) |
| **Documentación de referencia** | [`docs/04_models.md`](docs/04_models.md) |

**Debes crear** el archivo `models/schemas.py` en esa ruta. Usa los comentarios de abajo como guía y completa el código con autocompletado de VS Code.

Esta guía está pensada para pegarse justo encima de las clases principales, de forma que el editor pueda inferir mejor la intención. Estas estructuras no tienen lógica: solo guardan datos que viajan por todo el sistema.

```python
# Clase utilizada para representar el resultado de una skill (Product Owner, QA o Arquitectura).
# Debe definir los cuatro campos que TODA skill devuelve al terminar su trabajo.
# Parametro content: texto en Markdown listo para mostrar en pantalla.
# Parametro is_mock: True si la respuesta fue generada sin IA real (modo ejemplo).
# Parametro skill_name: identificador legible de la skill ("product_owner", "qa", "architecture").
# Parametro error: mensaje de error si algo falló de forma controlada; None si todo salió bien.
@dataclass
class SkillResult:
    pass
```

```python
# Clase utilizada para representar el informe final del pipeline completo.
# Debe agrupar el requerimiento original y los tres resultados de las skills en un solo objeto.
# Parametro requirement: texto que escribió el usuario al inicio.
# Parametro user_story: resultado de ProductOwnerSkill (historia de usuario).
# Parametro qa_cases: resultado de QASkill (casos de prueba).
# Parametro architecture: resultado de ArchitectureSkill (recomendación arquitectónica).
# Retorna: un objeto que main.py usa para renderizar las tres secciones en pantalla.
@dataclass
class PipelineResult:
    pass
```

## Versión corta para usar como comentario

```python
# Clase utilizada para representar el resultado de una skill (Product Owner, QA o Arquitectura).
# Debe definir los cuatro campos que TODA skill devuelve al terminar su trabajo.

# Clase utilizada para representar el informe final del pipeline completo.
# Debe agrupar el requerimiento original y los tres resultados de las skills en un solo objeto.
```
