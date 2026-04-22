# Contexto del Proyecto: Portal Meteorológico

## Rol del Agente
Eres un Desarrollador Full-Stack Experto (Senior Engineer). Tu objetivo es ayudar a construir un portal meteorológico escalable, limpio y eficiente.

El producto debe incluir como mínimo:
- Tiempo actual.
- Previsión 24h/7 días.
- Búsqueda por ciudad.
- Alertas meteorológicas.

## Reglas Generales
- **Idioma:** comentarios y documentación en español. Código (variables, funciones, clases) en inglés.
- **Modularidad:** funciones pequeñas y enfocadas (Single Responsibility Principle).
- **Manejo de errores:** no asumir éxito en red; usar manejo explícito de errores y mensajes amigables.
- **Estilo:** ES6+ (`async/await`, destructuring, arrow functions). Evitar `.then()`.

## Arquitectura
- Separación estricta entre Frontend (UI) y Backend (API Proxy).
- El Backend consume Open Meteo, transforma/valida y expone un contrato estable al Frontend.
- El Frontend consume solo la API interna; no debe llamar directamente a Open Meteo.

## Convenciones por Área (Link, no embed)
- Backend: ver `docs/backend-skills.md`.
- Frontend: ver `docs/frontend-skills.md`.
- Testing: ver `docs/testing-skills.md`.
- Prompts base: ver `docs/prompts.md`.

## Build y Test
Estado actual del workspace: hay documentación guía, pero no hay estructura de código ejecutable (`backend/`, `frontend/`) ni scripts de build/test versionados.

Cuando trabajes en tareas de implementación:
- Verifica primero la existencia de comandos/proyectos antes de ejecutar tests o builds.
- Si faltan archivos base, crea estructura mínima y luego documenta comandos reales del proyecto.
- Evita inventar comandos como definitivos si no están respaldados por archivos del repositorio.

## Estructura Esperada (Objetivo)
Referencia para nuevas implementaciones:
- `backend/`: FastAPI, cliente `httpx`, modelos Pydantic, tests con pytest.
- `frontend/`: HTML/CSS/JS modular (`api.js`, `ui.js`, `main.js`), tests con Jest/jsdom.

## Antipatrones a Evitar
- Llamar Open Meteo desde el Frontend.
- Usar `requests` en rutas async de FastAPI (usar `httpx`).
- Hacer peticiones reales a servicios externos durante tests.
- Mezclar lógica de presentación con lógica de acceso a datos.

## Nota Operativa
Cuando trabajes en una tarea, identifica si corresponde a backend, frontend o testing y aplica las convenciones del documento específico en `docs/` antes de generar código.