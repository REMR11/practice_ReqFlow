# 02 - Patrones de diseño

| Anterior | Siguiente |
|----------|-----------|
| [01_architecture](01_architecture.md) | [03_folder_structure](03_folder_structure.md) |

---

## El patrón Pipeline/Strategy explicado con un ejemplo cotidiano

Imagina una línea de ensamblaje de un restaurante de hamburguesas:

1. **Estación 1** pone la carne en el pan.
2. **Estación 2** agrega vegetales, *usando como base lo que dejó la Estación 1* (no va a poner vegetales si no hay pan).
3. **Estación 3** empaca la hamburguesa final, *considerando todo lo que se acumuló antes*.

Cada estación:
- Tiene una interfaz **idéntica** desde afuera (recibe una hamburguesa parcial, entrega una hamburguesa más completa).
- No necesita saber **cómo** trabaja la estación anterior, solo necesita su resultado.
- Puede ser **reemplazada o agregada** sin rediseñar toda la línea (ej. agregar una "Estación 4: agregar salsa especial" no rompe nada).

En este proyecto, las "estaciones" son `ProductOwnerSkill`, `QASkill` y
`ArchitectureSkill`. Todas implementan el mismo método `run()`, todas reciben
`requirement` + `context`, y todas devuelven el mismo tipo de objeto
(`SkillResult`). Eso es lo que hace posible que en el futuro agregues una
`SecuritySkill` o una `EstimationSkill` sin tener que modificar el orquestador
desde cero — solo la agregas a la cadena. Ver [05_pipeline](05_pipeline.md).

---

## Template Method (`BaseSkill`)

El **Template Method** define un esqueleto de pasos fijo, donde algunos pasos los
implementa la clase base y otros los completa cada subclase. `BaseSkill.run()`
define el contrato común (intentar IA real, caer a mock, nunca lanzar excepción),
mientras que cada skill concreta completa los detalles específicos. El desarrollo
de este patrón está en [06_skills](06_skills.md).

---

## Proxy y degradación elegante (`AIProxyClient`)

En vez de darle tu tarjeta de crédito directamente a cada empleado, les das una
tarjeta corporativa con un límite controlado por ti. El proveedor de la tarjeta
(tu proxy) es el único que conoce el número real de tu cuenta (la API key del
proveedor de IA). Cada empleado (cada skill) usa su tarjeta corporativa sin saber
el número real.

`AIProxyClient` es esa tarjeta corporativa: las skills nunca hablan directamente
con OpenAI o Anthropic. Además aplica **degradación elegante**: si faltan las
credenciales, no lanza un error sino que marca `is_available = False` y el sistema
sigue funcionando en modo mock. El detalle está en [07_interfaces](07_interfaces.md).

---

## DRY ("Don't Repeat Yourself")

`AIProxyClient`, `PromptLoader` y `RequirementPipeline` son piezas que las tres
skills necesitan por igual. Si copiáramos esa lógica dentro de cada skill,
cualquier cambio tendría que repetirse tres veces y eventualmente alguna copia
quedaría desactualizada. Sacarlas a `core/` es aplicar el principio de no repetir
código. Ver [03_folder_structure](03_folder_structure.md).

---

## Inyección de dependencias

Pasar un objeto ya creado como parámetro (`ai_client`, `prompt_loader`) en lugar
de obligar a la clase a crearlo internamente facilita las pruebas: puedes inyectar
un cliente falso sin tocar red real. Tanto `BaseSkill` como `RequirementPipeline`
aceptan sus dependencias por constructor con valores por defecto. Ver
[08_testing](08_testing.md).

---

## Separación de negocio y presentación

`MarkdownFormatter` tiene una sola responsabilidad: convertir resultados en texto
Markdown. Las skills no deberían preocuparse por *cómo se ve* su resultado en
pantalla, solo por *generarlo*. Cambiar cómo se muestra algo no debería requerir
tocar cómo se calcula.
