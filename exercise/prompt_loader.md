# Guía de comentarios para core/prompt_loader.py

## Dónde implementar

| Campo | Valor |
|-------|-------|
| **Archivo a crear** | [`core/prompt_loader.py`](core/prompt_loader.py) |
| **Capa** | Infraestructura (`core/`) |
| **Orden sugerido** | 2 — después de `models/schemas.py` |
| **Archivos relacionados** | [`prompts/product_owner.md`](prompts/product_owner.md), [`prompts/qa.md`](prompts/qa.md), [`prompts/architecture.md`](prompts/architecture.md) |
| **Documentación de referencia** | [`docs/07_interfaces.md`](docs/07_interfaces.md) |

**Debes crear** el archivo `core/prompt_loader.py` en esa ruta. Usa los comentarios de abajo como guía y completa el código con autocompletado de VS Code.

Esta guía está pensada para pegarse justo encima de los métodos principales, de forma que el editor pueda inferir mejor la intención. Esta clase es responsable de leer los archivos `.md` de la carpeta `prompts/`.

```python
# Clase de excepción utilizada cuando no se encuentra un archivo de prompt.
# Debe heredar de Exception para que las skills puedan capturarla y usar un prompt de respaldo.
# Se lanza desde PromptLoader.load() cuando el archivo no existe en disco.
class PromptNotFoundError(Exception):
    pass
```

```python
# Método utilizado para inicializar el cargador de prompts y resolver la ruta a la carpeta prompts/.
# Debe guardar la ruta en self.prompts_dir como un objeto Path.
# Parametro prompts_dir: ruta personalizada; si es None, calcularla relativa al propio archivo
#   usando Path(__file__).resolve().parent.parent / "prompts" (así funciona desde cualquier directorio).
# Retorna: None (configura self.prompts_dir).
def __init__(self, prompts_dir: str | Path | None = None) -> None:
    pass
```

```python
# Método utilizado para leer el contenido completo de un archivo de prompt.
# Debe construir la ruta completa (prompts_dir / prompt_filename), verificar que exista y leer el archivo.
# Parametro prompt_filename: nombre del archivo, ej. "product_owner.md".
# Debe leer con encoding="utf-8" para soportar caracteres especiales.
# Debe lanzar PromptNotFoundError si el archivo no existe (mensaje descriptivo con el nombre del archivo).
# Retorna: str con el contenido completo del archivo .md.
def load(self, prompt_filename: str) -> str:
    pass
```

## Versión corta para usar como comentario

```python
# Clase de excepción utilizada cuando no se encuentra un archivo de prompt.
# Debe heredar de Exception para que las skills puedan capturarla y usar un prompt de respaldo.

# Método utilizado para inicializar el cargador de prompts y resolver la ruta a la carpeta prompts/.
# Debe guardar la ruta en self.prompts_dir como un objeto Path.

# Método utilizado para leer el contenido completo de un archivo de prompt.
# Debe construir la ruta, verificar que exista, leer con utf-8 y lanzar PromptNotFoundError si falta.
```
