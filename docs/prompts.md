# Prompts para FastAPI (Backend)
- `@workspace Basándote en #backend-skills.md, crea el archivo principal main.py con FastAPI. Incluye la configuración de CORS y un endpoint GET /api/weather que reciba lat y lon como query parameters.`
- `@workspace Crea una función asíncrona usando httpx que llame a la API de Open Meteo con la lat y lon dadas. Captura los errores de conexión y lanza una HTTPException si falla.`
- `@workspace Crea los modelos de Pydantic basándote en la estructura de respuesta definida en #backend-skills.md para estandarizar el output del endpoint.`

# Prompts para Vanilla JS (Frontend)
- `@workspace Basándote en #frontend-skills.md, genera el archivo api.js con una función asíncrona que haga fetch al endpoint /api/weather de nuestro backend de FastAPI.`
- `@workspace Genera el archivo ui.js. Escribe una función que reciba el objeto de datos del clima e inyecte un template literal HTML dentro de un div con id "weather-container".`
- `@workspace En index.html, crea una estructura semántica básica con un input para buscar la ciudad, un botón de búsqueda, y un contenedor vacío para los resultados. Utiliza clases CSS descriptivas.`

## Prompts para Testing (Backend - FastAPI)
- `@workspace Basándote en #testing-skills.md, crea un test unitario con pytest para el endpoint /api/weather. Usa un mock para simular la respuesta de httpx y asegurarte de que no llamamos a la API real de Open Meteo.`
- `@workspace Crea un test con TestClient de FastAPI que verifique que si paso latitud y longitud inválidas, el servidor me devuelve un error HTTP 400.`

## Prompts para Testing (Frontend - Vanilla JS)
- `@workspace Basándote en #testing-skills.md, crea un test con Jest para la función que mapea los códigos del clima a iconos. Haz pruebas para los códigos 0 (sol), 71 (nieve) y 95 (tormenta).`
- `@workspace Escribe un test en Jest que simule el DOM, inyecte un div vacío, y mockee la función fetch para simular que recibimos datos del clima. Luego, verifica que el DOM se actualiza con la temperatura correcta.`