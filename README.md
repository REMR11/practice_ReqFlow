# ReqFlow — De un requerimiento a tres documentos

> **¿Nunca has programado?** Este README está pensado para ti. No necesitas saber Python de memoria para entender de qué va el proyecto ni por dónde empezar.

---

## ¿Qué es esto?

Imagina que trabajas en un equipo de software y alguien te dice:

> *"Quiero un botón de login con Google en la página de inicio."*

Eso es un **requerimiento**: una idea escrita con palabras normales.

Este proyecto te enseña a construir una **aplicación web sencilla** que recibe ese texto y, automáticamente, produce **tres documentos útiles**:

| Paso | Rol (como en un equipo real) | Qué genera |
|------|------------------------------|------------|
| 1 | **Product Owner** (define qué quiere el usuario) | Una **historia de usuario** |
| 2 | **QA** (piensa en qué puede fallar) | **Casos de prueba** |
| 3 | **Arquitectura** (piensa en cómo construirlo) | Una **recomendación técnica** |

La aplicación usa **inteligencia artificial** para redactar esos documentos, pero está diseñada para **seguir funcionando** aunque la IA no esté disponible (mostrará respuestas de ejemplo).

---

## ¿Qué hay en este repositorio?

**Este repositorio es la guía y el plano del proyecto.** Aquí encontrarás la documentación para construirlo paso a paso. El código Python lo irás creando tú siguiendo las instrucciones.

```
schema/
├── README.md                 ← Estás aquí
├── docs/                     ← Documentación principal (léela en orden)
├── .github/
│   ├── instructions/         ← Reglas para asistentes de IA (Copilot, etc.)
│   └── prompts/              ← Comandos listos para generar código con IA
├── diagrama_de_clases_uml.md ← Diagrama visual de cómo se conectan las piezas
└── documentacion_requirement_to_artifacts.md  ← Índice alternativo a docs/
```

Todavía **no hay código Python** en este repo: es normal. La idea es que lo construyas siguiendo la documentación o usando los prompts de `.github/prompts/`.

---

## Analogía simple: una fábrica en cadena

Piensa en el sistema como una **línea de ensamblaje** con tres estaciones:

```
  Escribes un requerimiento
           │
           ▼
  ┌─────────────────────┐
  │ 1. Product Owner    │  → Historia de usuario
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ 2. QA               │  → Casos de prueba (ve lo que hizo el paso 1)
  └──────────┬──────────┘
             ▼
  ┌─────────────────────┐
  │ 3. Arquitectura     │  → Recomendación (ve los pasos 1 y 2)
  └──────────┬──────────┘
             ▼
     Tres documentos listos
```

Cada estación recibe el trabajo de la anterior. Por eso QA no empieza de cero: ya conoce la historia de usuario. Y Arquitectura conoce tanto la historia como los casos de prueba.

---

## Palabras que vas a ver (glosario mínimo)

| Palabra | Qué significa aquí |
|---------|-------------------|
| **Requerimiento** | Texto que describe lo que se quiere construir |
| **Pipeline** | Secuencia de pasos en orden fijo |
| **Skill** | Un “trabajador” del pipeline (PO, QA o Arquitectura) |
| **Streamlit** | Herramienta para crear páginas web con Python sin saber HTML |
| **Markdown** | Formato de texto con títulos y listas (como este README) |
| **Mock** | Respuesta de ejemplo cuando la IA no está disponible |
| **Repositorio (repo)** | Carpeta del proyecto guardada en Git/GitHub |

---

## ¿Qué vas a construir al final?

Cuando termines de implementar todo, tu proyecto se verá así:

```
Proyecto/
├── main.py                       # La app web (Streamlit)
├── skills/                       # Los tres “trabajadores” del pipeline
├── core/                         # Motor: conexión con IA y orquestación
├── models/                       # Formularios de datos (estructuras simples)
├── prompts/                      # Instrucciones que le das a la IA
├── utils/                        # Formateo para mostrar resultados bonitos
└── tests/                        # Pruebas automáticas (opcional al inicio)
```

---

## Por dónde empezar

### Paso 1 — Lee la documentación en orden

Abre la carpeta [`docs/`](docs/) y sigue este camino:

1. [00_overview.md](docs/00_overview.md) — Visión general
2. [01_architecture.md](docs/01_architecture.md) — Cómo se conectan las piezas
3. [02_patterns.md](docs/02_patterns.md) — Ideas de diseño explicadas sin jerga
4. [03_folder_structure.md](docs/03_folder_structure.md) — Qué archivo crear y en qué orden
5. [04_models.md](docs/04_models.md) → [08_testing.md](docs/08_testing.md) — Detalle de cada parte

No hace falta leerlo todo de un golpe. Un documento por sesión está bien.

### Paso 2 — Crea la estructura de carpetas

Sigue el orden de [03_folder_structure.md](docs/03_folder_structure.md). Empieza siempre por `models/schemas.py` (no depende de nada más).

Si usas **GitHub Copilot** o un asistente de IA en el editor, puedes usar el prompt `scaffold-project` en [`.github/prompts/scaffold-project.prompt.md`](.github/prompts/scaffold-project.prompt.md) para generar carpetas y archivos vacíos.

### Paso 3 — Implementa pieza por pieza

Orden recomendado (cada paso solo usa lo que ya construiste):

1. `models/schemas.py`
2. `core/ai_proxy_client.py` y `core/prompt_loader.py`
3. `skills/base_skill.py`
4. Las tres skills: Product Owner, QA, Arquitectura
5. `core/pipeline.py`
6. `utils/formatter.py`
7. `main.py`

Hay prompts en `.github/prompts/` para cada etapa (`implement-models`, `implement-pipeline`, etc.).

---

## Herramientas que necesitarás (cuando empieces a programar)

| Herramienta | Para qué sirve |
|-------------|----------------|
| **Python 3.10+** | Lenguaje del proyecto |
| **Git** | Guardar versiones del código (este repo ya usa Git) |
| **Editor de código** | VS Code, Cursor, etc. |
| **Streamlit** | Interfaz web (`pip install streamlit`) |
| **pytest** | Ejecutar pruebas (`pip install pytest`) |

Variables de entorno opcionales (solo si conectas IA real):

```bash
AI_PROXY_URL=https://tu-proxy.ejemplo.com
AI_PROXY_API_KEY=tu-clave-secreta
```

Sin esas variables, la app funciona igual con respuestas de ejemplo (modo mock).

---

## Ejemplo de uso (cuando la app esté lista)

1. Ejecutas: `streamlit run main.py`
2. Se abre una página en el navegador
3. Escribes, por ejemplo: *"Botón de login con Google en la home"*
4. Pulsas el botón de analizar
5. Ves tres secciones: historia de usuario, casos de prueba y recomendación arquitectónica

---

## Ejecucion rapida

### 1) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2) Configurar variables de entorno (opcional para IA real)

```bash
cp .env.example .env
```

Luego edita `.env` y agrega tu `AI_PROXY_API_KEY`.

### 3) Ejecutar la app Streamlit

```bash
streamlit run main.py
```

### 4) Ejecutar pruebas

```bash
pytest
```

### Modo mock vs modo IA real

- **Modo mock (sin credenciales):** si `AI_PROXY_URL` y/o `AI_PROXY_API_KEY` no
  estan definidas, la app sigue funcionando y cada skill devuelve una respuesta
  de ejemplo (`is_mock=True`).
- **Modo IA real (con credenciales):** si ambas variables estan configuradas,
  `AIProxyClient` hace `POST {AI_PROXY_URL}/chat` y las skills usan el contenido
  real devuelto por el proxy.

---

## Cómo colaborar en GitHub

Si es tu primera vez con Git:

1. **Clonar** el repo: copiar el proyecto a tu computadora
2. **Commit**: guardar un “punto de control” con un mensaje
3. **Push**: subir tus cambios a GitHub
4. **Pull request**: pedir que revisen e integren tu trabajo

Para autenticarte en GitHub ya no sirve la contraseña de tu cuenta. Usa un **token de acceso personal** o una **clave SSH**. Si tienes dudas, pide ayuda a un mentor del bootcamp.

---

## Preguntas para comprobar que entendiste

Antes de escribir código, intenta responder (sin mirar la doc):

1. ¿Por qué QA recibe la historia de usuario y no solo el requerimiento original?
2. ¿Qué pasa si la IA no responde? ¿Se cae toda la app?
3. ¿Cuál es el primer archivo que debes crear y por qué?

Las respuestas están en [docs/00_overview.md](docs/00_overview.md).

---

## ¿Necesitas ayuda?

- **Documentación detallada:** carpeta [`docs/`](docs/)
- **Diagrama visual:** [`diagrama_de_clases_uml.md`](diagrama_de_clases_uml.md)
- **Reglas del proyecto para IA:** [`.github/instructions/copilot.instructions.md`](.github/instructions/copilot.instructions.md)

---

## Licencia y organización

Proyecto educativo de **KodigoOrg** — práctica de flujo de requerimientos a artefactos con arquitectura en capas y asistentes de IA.
