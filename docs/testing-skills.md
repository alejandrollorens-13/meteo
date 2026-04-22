# Testing Skills & Instructions

## Objetivo
Crear una suite de pruebas robusta que garantice el correcto funcionamiento del portal meteorológico sin depender de servicios externos (Open Meteo) durante la ejecución de los tests.

## 🐍 Backend Testing (Python / FastAPI)
- **Framework:** Usa `pytest` y `pytest-asyncio` para pruebas asíncronas.
- **Cliente de Pruebas:** Usa `TestClient` de FastAPI (`from fastapi.testclient import TestClient`) para pruebas de integración de los endpoints.
- **Regla de ORO (Mocks):** NUNCA hagas peticiones reales a Open Meteo en los tests. Usa `unittest.mock.patch` o `pytest-mock` para simular las respuestas de `httpx.AsyncClient.get`.
- **Estructura de Tests Backend:**
  - *Unitarios:* Prueba funciones aisladas (ej. la lógica que formatea la respuesta de Open Meteo al modelo Pydantic).
  - *Mocks:* Prueba el servicio que hace el fetch asíncrono, mockeando la respuesta HTTP para que devuelva un JSON estático.
  - *Integración:* Usa `TestClient` para llamar a `/api/weather?lat=x&lon=y` y verifica que devuelve un HTTP 200 y el JSON estructurado correctamente.

## 🌐 Frontend Testing (Vanilla JS)
- **Framework:** Usa `Jest` configurado con `jsdom` (para poder simular el DOM del navegador en Node.js).
- **Regla de ORO (Mocks):** NUNCA hagas llamadas reales al backend durante los tests del frontend. Sobrescribe la función global `fetch` usando `jest.fn()` para devolver promesas resueltas con datos falsos.
- **Estructura de Tests Frontend:**
  - *Unitarios:* Prueba funciones lógicas puras en `ui.js` (ej. la función que mapea el código WMO a un emoji/icono).
  - *Mocks:* En `api.js`, mockea `fetch` para probar cómo tu código maneja un error 500 o una respuesta exitosa 200.
  - *Integración (DOM):* En `ui.js`, crea un contenedor falso en el `document.body`, llama a tus funciones de renderizado y usa `expect(document.querySelector('.temperature').textContent).toBe('22.5')` para validar.