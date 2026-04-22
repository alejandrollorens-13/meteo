# Frontend Skills & Instructions

## Objetivo
Crear una interfaz de usuario limpia, responsive y accesible para mostrar la información meteorológica.

## Stack Tecnológico
- HTML5 semántico y CSS3 puro (o variables CSS modernas).
- JavaScript (ES6+ Modules).

## Reglas del Frontend
- **Estructura de Archivos JS:** Usa módulos. Separa el código en:
  - `api.js`: Solo se encarga de hacer el `fetch` al backend de FastAPI.
  - `ui.js`: Solo se encarga de manipular el DOM (ej. pintar datos, mostrar errores).
  - `main.js`: El controlador principal que une los eventos del DOM con la API.
- **Manipulación del DOM:** Usa `document.querySelector` y `document.getElementById`. Evita usar librerías externas como jQuery.
- **Plantillas:** Usa *Template Literals* (\` \`) para construir fragmentos de HTML dinámico antes de inyectarlos en el DOM mediante `innerHTML` o `insertAdjacentHTML`.
- **Manejo de Estado (Manual):** Crea funciones claras como `showLoading()`, `hideLoading()`, `showError(msg)` y `renderWeather(data)`.

## Mapeo de Iconos
*Instrucción para Copilot:* Cuando proceses el `weathercode` (código WMO) que viene del backend, utiliza la siguiente lógica para los iconos:
- 0: Sol claro ☀️
- 1, 2, 3: Parcialmente nublado ⛅
- 45, 48: Niebla 🌫️
- 51, 53, 55, 61, 63, 65: Lluvia 🌧️
- 71, 73, 75: Nieve ❄️
- 95, 96, 99: Tormenta ⛈️

> **Instrucción para Copilot**: Cuando generes controladores, mapea la respuesta cruda de Open Meteo a este contrato estandarizado.