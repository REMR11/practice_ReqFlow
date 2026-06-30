# 03 - Estructura de carpetas

| Anterior | Siguiente |
|----------|-----------|
| [02_patterns](02_patterns.md) | [04_models](04_models.md) |

---

## Árbol final

```
Proyecto/
├── main.py                       # Punto de entrada (app Streamlit)
├── skills/
│   ├── __init__.py
│   ├── base_skill.py             # Clase abstracta — el "contrato"
│   ├── product_owner_skill.py    # Primera estación del pipeline
│   ├── qa_skill.py               # Segunda estación
│   └── architecture_skill.py     # Tercera estación
├── core/
│   ├── __init__.py
│   ├── ai_proxy_client.py        # Único punto de salida hacia la IA
│   ├── prompt_loader.py          # Lee los prompts desde archivos .md
│   └── pipeline.py               # El orquestador (la "línea de ensamblaje")
├── models/
│   ├── __init__.py
│   └── schemas.py                # Estructuras de datos puras
├── prompts/
│   ├── product_owner.md
│   ├── qa.md
│   └── architecture.md
└── utils/
    ├── __init__.py
    └── formatter.py              # Convierte resultados a Markdown para mostrar
```

---

## ¿Por qué existe la carpeta `core/`?

Porque `AIProxyClient`, `PromptLoader` y `RequirementPipeline` son piezas que las
tres skills necesitan por igual. Si copiáramos esa lógica dentro de cada skill,
cualquier cambio (ej. el formato de la petición HTTP) tendría que repetirse tres
veces y eventualmente alguna copia quedaría desactualizada. Sacarlas a una carpeta
compartida es aplicar el principio **DRY** (ver [02_patterns](02_patterns.md)).

---

## Orden de implementación, paso a paso

Como vas a construir esto desde cero, este es el orden que evita bloqueos (cada
paso solo depende de lo que ya construiste):

1. **`models/schemas.py`** — no depende de nada. Empieza aquí. Ver [04_models](04_models.md).
2. **`core/ai_proxy_client.py`** y **`core/prompt_loader.py`** — independientes entre sí, puedes hacerlos en cualquier orden, pero antes que las skills. Ver [07_interfaces](07_interfaces.md).
3. **`skills/base_skill.py`** — depende de los dos anteriores y de los modelos. Ver [06_skills](06_skills.md).
4. **Las tres skills concretas** — dependen de `base_skill.py`. Ver [06_skills](06_skills.md).
5. **`core/pipeline.py`** — depende de las tres skills. Ver [05_pipeline](05_pipeline.md).
6. **`utils/formatter.py`** — depende solo de los modelos, puedes hacerlo en paralelo con el paso 5. Ver [07_interfaces](07_interfaces.md).
7. **`main.py`** — al final, porque depende de todo lo anterior. Ver [07_interfaces](07_interfaces.md).

Para verificar que no introduces dependencias circulares mientras programas,
consulta la tabla de dependencias en [01_architecture](01_architecture.md).
