# 00 - Visión general

| Anterior | Siguiente |
|----------|-----------|
| — | [01_architecture](01_architecture.md) |

Esta documentación está escrita para que puedas **construir el sistema desde cero**
siguiendo el orden correcto, entendiendo el "por qué" detrás de cada decisión. No
asume que ya conoces patrones de diseño avanzados: cada concepto se explica la
primera vez que aparece.

---

## ¿Qué hace este proyecto, en una frase?

El usuario escribe un **requerimiento** en texto plano (ej. "quiero un botón de
login con Google") en una app de Streamlit, y el sistema lo pasa automáticamente
por tres etapas de análisis —Product Owner, QA y Arquitectura— devolviendo tres
documentos en Markdown: una historia de usuario, una lista de casos de prueba, y
una recomendación arquitectónica.

Lo interesante no es solo *qué* hace, sino *cómo* lo hace: cada etapa no trabaja
en aislamiento. La etapa de QA conoce lo que dijo Product Owner, y la etapa de
Arquitectura conoce lo que dijeron las dos anteriores. Es una especie de "cadena
de montaje" donde cada estación recibe el trabajo de la anterior y le agrega su
parte.

A ese patrón —una secuencia de pasos donde cada paso es intercambiable y recibe
el output del anterior— se le llama **patrón Pipeline** (combinado con
**Strategy**). Es el corazón de este proyecto. Profundizamos en él en
[02_patterns](02_patterns.md).

---

## Índice de la documentación

| Documento | Contenido |
|---|---|
| [00_overview](00_overview.md) | Qué hace el proyecto, índice, orden de construcción, glosario |
| [01_architecture](01_architecture.md) | Mapa de capas, flujo de datos, dependencias sin ciclos |
| [02_patterns](02_patterns.md) | Pipeline, Strategy, Template Method, Proxy, DRY, inyección de dependencias |
| [03_folder_structure](03_folder_structure.md) | Árbol de carpetas y orden de implementación |
| [04_models](04_models.md) | `SkillResult` y `PipelineResult` |
| [05_pipeline](05_pipeline.md) | `RequirementPipeline` y la acumulación de `context` |
| [06_skills](06_skills.md) | `BaseSkill` y las tres skills concretas |
| [07_interfaces](07_interfaces.md) | Infraestructura, formateador, `main.py` y diagrama UML completo |
| [08_testing](08_testing.md) | Estrategia de pruebas alineada con la arquitectura |

---

## Orden de construcción resumido

Este es el orden que evita bloqueos (cada paso solo depende de lo ya construido).
El detalle está en [03_folder_structure](03_folder_structure.md).

1. `models/schemas.py` — no depende de nada. Empieza aquí.
2. `core/ai_proxy_client.py` y `core/prompt_loader.py` — independientes entre sí.
3. `skills/base_skill.py` — depende de los dos anteriores y de los modelos.
4. Las tres skills concretas — dependen de `base_skill.py`.
5. `core/pipeline.py` — depende de las tres skills.
6. `utils/formatter.py` — depende solo de los modelos (paralelo al paso 5).
7. `main.py` — al final, porque depende de todo lo anterior.

---

## Glosario rápido para conceptos nuevos

| Término | En palabras simples |
|---|---|
| Clase abstracta (`ABC`) | Un molde que define qué métodos debe tener cualquier clase que herede de él, pero no se puede instanciar directamente |
| Método abstracto | Un método que la clase base declara pero no implementa — obliga a cada subclase a darle su propia versión |
| Patrón Pipeline | Una secuencia de pasos donde cada paso recibe el resultado del anterior |
| Patrón Strategy | Varias implementaciones intercambiables que cumplen el mismo contrato (mismo método, misma firma) |
| Degradación elegante | Que el sistema sigue funcionando (en modo reducido) en lugar de romperse cuando algo externo falla |
| Inyección de dependencias | Pasar un objeto ya creado como parámetro (`ai_client`) en lugar de obligar a la clase a crearlo internamente — facilita hacer pruebas |
| DRY ("Don't Repeat Yourself") | Principio de no duplicar la misma lógica en varios lugares |

---

## Preguntas para validar tu entendimiento

Antes de empezar a programar, intenta responder esto sin ver la documentación:

1. ¿Por qué `RequirementPipeline.execute()` no necesita un `try/except` alrededor de cada llamada a `.run()`? (ver [05_pipeline](05_pipeline.md) y [06_skills](06_skills.md))
2. Si quisieras que `QASkill` también recibiera contexto de una futura `SecuritySkill`, ¿qué tendrías que modificar primero: `BaseSkill` o `RequirementPipeline`?
3. ¿Qué pasaría si `AIProxyClient.complete()` decidiera lanzar la excepción directamente hacia `main.py` en lugar de hacia la skill que la llama?

Si puedes responder estas tres preguntas con seguridad, ya entendiste la
arquitectura lo suficiente para empezar a construirla.
