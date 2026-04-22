# Backend Skills & Instructions (FastAPI)

## Stack Tecnológico
- Python 3.10+
- Framework: FastAPI
- Cliente HTTP asíncrono: `httpx` (No usar `requests` para no bloquear el event loop)
- Servidor ASGI: Uvicorn

## Reglas del Backend
- **Asincronía:** Todas las rutas que llamen a Open Meteo deben usar `async def` y `await httpx.AsyncClient()`.
- **Validación de Datos:** Usa **Pydantic** para definir el modelo de respuesta. Esto autogenerará la documentación en `/docs` (Swagger UI).
- **CORS:** Configura `CORSMiddleware` en la aplicación de FastAPI para permitir peticiones desde el origen del frontend (ej. `http://localhost:5500` o `http://127.0.0.1:5500`).
- **Manejo de Errores:** Usa `HTTPException` de FastAPI para devolver errores 400 (parámetros inválidos) o 500 (Open Meteo caído).

## Contrato de Datos (Modelo Pydantic)
*Instrucción:* Usa este esquema mental para generar las clases Pydantic de respuesta:
```python
class CurrentWeather(BaseModel):
    temperature: float
    condition: str
    wind_speed: float

class WeatherResponse(BaseModel):
    success: bool
    location: dict
    current_weather: CurrentWeather
    forecast: list
```
