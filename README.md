# Meteo Pulse 🌦️

**Portal Meteorológico Inteligente** - Una aplicación web moderna para consultar el clima actual, pronósticos horarios y alertas meteorológicas en tiempo real.

![Status](https://img.shields.io/badge/status-beta-yellow)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Características

- 🌍 **Búsqueda por ciudad** - Encuentra el clima de cualquier ciudad del mundo
- 🌡️ **Datos meteorológicos en tiempo real** - Temperatura, condición del cielo y velocidad del viento
- 📊 **Previsión de 24 horas** - Próximas 24 horas relativas a la hora actual de búsqueda
- ⚠️ **Alertas meteorológicas** - Avisos automáticos de tormentas, nieve, calor extremo, etc.
- 📱 **Diseño responsive** - Funciona perfectamente en desktop, tablet y móvil
- 🎨 **Interfaz moderna** - Bootstrap 5 con estilos personalizados y glassmorphism
- ⚡ **Sin dependencias externas** - Frontend vanilla JavaScript (ES6+)
- 🚀 **API proxy segura** - Backend que protege las llamadas a Open Meteo

## 📋 Requisitos Previos

- **Python 3.10+** - Para ejecutar el backend
- **Node.js 16+** (opcional) - Si quieres ejecutar tests del frontend con Jest

## 🏗️ Estructura del Proyecto

```
meteo/
├── backend/
│   ├── main.py                 # Aplicación FastAPI principal
│   └── requirements.txt         # Dependencias Python
├── frontend/
│   ├── index.html              # HTML principal
│   ├── styles.css              # Estilos CSS personalizados
│   └── js/
│       ├── api.js              # Cliente HTTP para consumir backend
│       ├── ui.js               # Funciones de renderizado del DOM
│       └── main.js             # Orquestador principal
├── tests/
│   ├── test_unitarios.py       # Pruebas unitarias de funciones puras
│   ├── test_integracion.py     # Pruebas de integración del endpoint
│   └── test_mocks.py           # Pruebas con mocks de httpx
├── docs/
│   ├── backend-skills.md       # Convenciones y patrones backend
│   ├── frontend-skills.md      # Convenciones y patrones frontend
│   ├── testing-skills.md       # Estrategia de testing
│   └── prompts.md              # Ejemplos de prompts para IA
├── .github/
│   └── copilot-instructions.md # Instrucciones para agentes IA
├── README.md                   # Este archivo
└── .gitignore                  # Archivos ignorados en git

```

## 🚀 Instalación y Ejecución

### Opción 1: Ejecutar Backend y Frontend por separado

#### Backend (FastAPI + Uvicorn)

```bash
# 1. Navegar a la carpeta backend
cd backend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar servidor en http://127.0.0.1:8000
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

La API estará disponible en `http://127.0.0.1:8000` con documentación interactiva en `/docs`.

#### Frontend (Servidor Estático)

```bash
# 1. Navegar a la carpeta frontend
cd frontend

# 2. Ejecutar servidor estático en http://127.0.0.1:5500
python -m http.server 5500 --bind 127.0.0.1
```

Abre el navegador en `http://127.0.0.1:5500` para acceder a la aplicación.

### Opción 2: Ejecutar ambos servidores en paralelo

Desde la raíz del proyecto, en dos terminales diferentes:

**Terminal 1 (Backend):**
```bash
cd backend && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend && python -m http.server 5500 --bind 127.0.0.1
```

## 📖 Cómo Usar

1. **Abre la aplicación** en `http://127.0.0.1:5500`
2. **Escribe o selecciona una ciudad** - Usa el buscador o haz clic en una de las sugerencias rápidas
3. **Haz clic en "Consultar clima"** - La aplicación obtiene datos en tiempo real
4. **Visualiza la información:**
   - Temperatura actual y condición del cielo
   - Velocidad del viento
   - Alertas meteorológicas (si aplica)
   - Pronóstico de las próximas 24 horas

## 🔌 API Backend

### Endpoint: GET `/api/weather`

Obtiene información meteorológica actual y pronóstico de 24 horas.

**Parámetros:**

| Parámetro | Tipo    | Requerido | Descripción                              |
|-----------|---------|-----------|------------------------------------------|
| `city`    | string  | Si*       | Nombre de la ciudad (mín. 2 caracteres) |
| `lat`     | float   | Si*       | Latitud (-90 a 90)                      |
| `lon`     | float   | Si*       | Longitud (-180 a 180)                   |

*Debe proporcionarse: `city` O ambos `lat` y `lon`

**Respuesta exitosa (200):**

```json
{
  "success": true,
  "location": {
    "name": "Madrid",
    "latitude": 40.4168,
    "longitude": -3.7038,
    "timezone": "Europe/Madrid"
  },
  "current_weather": {
    "temperature": 22.5,
    "condition": "Parcialmente nublado",
    "wind_speed": 9.4
  },
  "forecast": [
    {
      "time": "2026-04-22T16:00",
      "temperature": 23.1,
      "weather_code": 2
    },
    ...
  ],
  "alerts": [
    {
      "level": "medium",
      "title": "Viento fuerte",
      "message": "Se registran rachas de viento elevadas. Toma precauciones."
    }
  ]
}
```

**Códigos de error:**

| Código | Descripción                                      |
|--------|--------------------------------------------------|
| 400    | Parámetros inválidos o faltantes                 |
| 404    | Ciudad no encontrada                             |
| 422    | Validación fallida (lat/lon fuera de rango)      |
| 502    | Error en servicio de geocodificación             |
| 503    | No se pudo conectar con Open Meteo               |

**Ejemplos de uso:**

```bash
# Por nombre de ciudad
curl "http://127.0.0.1:8000/api/weather?city=Madrid"

# Por coordenadas
curl "http://127.0.0.1:8000/api/weather?lat=40.4168&lon=-3.7038"
```

## 🧪 Testing

### Ejecutar todos los tests

```bash
cd /path/to/meteo
python -m pytest tests -v
```

### Tipos de tests

- **Unitarios** (`test_unitarios.py`) - Funciones puras y modelos Pydantic
- **Integración** (`test_integracion.py`) - Endpoint FastAPI con mocks
- **Mocks** (`test_mocks.py`) - Llamadas async a Open Meteo con mocks httpx

### Resultados esperados

```
test_unitarios.py::test_map_weather_code_clear_sky PASSED
test_unitarios.py::test_map_weather_code_rain PASSED
test_unitarios.py::test_current_weather_model_shape PASSED
test_unitarios.py::test_weather_response_model_shape PASSED
test_integracion.py::test_get_weather_by_city_ok PASSED
test_integracion.py::test_get_weather_missing_params_returns_400 PASSED
test_integracion.py::test_get_weather_invalid_lat_returns_422 PASSED
test_mocks.py::test_fetch_open_meteo_weather_success PASSED
test_mocks.py::test_fetch_open_meteo_weather_request_error PASSED

============ 10 passed in 0.31s ============
```

## 🏗️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web asincrónico moderno
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Pydantic** - Validación de datos con modelos tipados
- **httpx** - Cliente HTTP asincrónico (no bloquea el event loop)

### Frontend
- **HTML5** - Estructura semántica
- **CSS3** - Estilos nativos + Bootstrap 5
- **Vanilla JavaScript (ES6+)** - Sin dependencias externas
- **Módulos ES6** - Separación clara de responsabilidades (api.js, ui.js, main.js)

### Servicios Externos
- **Open Meteo** - API pública de datos meteorológicos (gratuita, sin autenticación)

### Testing & DevOps
- **pytest** - Framework de testing Python
- **pytest-asyncio** - Soporte para tests asincronos

## 🔐 Arquitectura de Seguridad

```
┌───────────────────┐
│   Navegador       │
│ (Frontend Local)  │
└──────────┬────────┘
           │ Fetch CORS
           ▼
┌─────────────────────────────────┐
│  Backend Proxy (FastAPI)        │
│  - Valida parámetros            │
│  - Maneja CORS                  │
│  - Transforma respuestas        │
└──────────┬──────────────────────┘
           │ httpx.AsyncClient
           ▼
┌─────────────────────────────────┐
│  Open Meteo API (Pública)       │
│  - Datos meteorológicos reales  │
└─────────────────────────────────┘
```

**Beneficios del proxy:**
- 🛡️ Validación de entrada antes de llamar a externos
- 🔄 Transformación de datos para aislar cambios
- 📊 Posibilidad de añadir caching futuro
- ✅ Manejo centralizado de errores

## 📊 Mapeo de Códigos WMO

Los códigos meteorológicos WMO se traducen automáticamente a condiciones legibles:

| Código | Condición          |
|--------|-------------------|
| 0      | Despejado         |
| 1-3    | Parcialmente nublado |
| 45-48  | Niebla            |
| 51-65  | Lluvia            |
| 71-75  | Nieve             |
| 95-99  | Tormenta          |

## ⚠️ Alertas Meteorológicas

El sistema genera alertas automáticas basadas en:

- **Nivel HIGH (Rojo):**
  - Tormentas previstas (WMO 95-99)

- **Nivel MEDIUM (Naranja):**
  - Nieve prevista (WMO 71-75)
  - Viento fuerte (≥40 km/h)
  - Temperaturas altas (≥35°C)
  - Temperaturas bajo cero (≤0°C)

## 🚀 Próximas Funcionalidades Planeadas

- [ ] Guardar ciudades favoritas
- [ ] Gráficas de temperatura a lo largo del día
- [ ] Cambiar entre °C y °F
- [ ] Historial de búsquedas
- [ ] Notificaciones push de alertas
- [ ] Modo oscuro
- [ ] Soporte multi-idioma
- [ ] Predicción de precipitación (%)

## 🤝 Contribución

### Para Desarrolladores

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/alejandrollorens-13/meteo.git
   cd meteo
   ```

2. **Crear rama de feature:**
   ```bash
   git checkout -b feature/tu-feature
   ```

3. **Hacer cambios y tests:**
   - Sigue las convenciones en `docs/backend-skills.md` y `docs/frontend-skills.md`
   - Ejecuta `pytest tests -v` para validar
   - Usa commits con mensajes claros

4. **Push y crear Pull Request:**
   ```bash
   git push origin feature/tu-feature
   ```

### Convenciones

- **Idioma:** Comentarios y docs en español; código en inglés
- **Estilo:** ES6+ frontend, async/await backend, sin librerías externas
- **Testing:** Cobertura mínima 80%, sin llamadas reales a servicios

## 📝 Reglas de Oro del Proyecto

❌ **NUNCA:**
- Llamar a Open Meteo directamente desde el frontend
- Usar `requests` en FastAPI (usar `httpx`)
- Hacer llamadas reales a servidores en tests (usar mocks)
- Mezclar lógica de presentación con lógica de datos

✅ **SIEMPRE:**
- Validar entrada en el backend
- Usar manejo explícito de errores
- Escribir tests antes de mergear
- Mantener módulos pequeños y enfocados

## 📚 Documentación Adicional

- [Instrucciones para Copilot](./.github/copilot-instructions.md) - Guía para agentes IA
- [Backend Skills](./docs/backend-skills.md) - Patrones y reglas del backend
- [Frontend Skills](./docs/frontend-skills.md) - Patrones y reglas del frontend
- [Testing Skills](./docs/testing-skills.md) - Estrategia de testing completa
- [Prompts](./docs/prompts.md) - Ejemplos de prompts para generación de código

## 🐛 Reporte de Bugs

Si encuentras un bug:

1. Abre un issue con detalles:
   - Pasos para reproducir
   - Comportamiento esperado
   - Comportamiento actual
   - Captura de pantalla (si es UI)

2. Incluye información del entorno:
   - Sistema operativo
   - Versión de Python/Node
   - Navegador (si es frontend)

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Alejandro Llorens** - [@alejandrollorens-13](https://github.com/alejandrollorens-13)

## 🙏 Agradecimientos

- [Open Meteo](https://open-meteo.com/) - API meteorológica pública y gratuita
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [Bootstrap](https://getbootstrap.com/) - Sistema de diseño responsive

---

**Última actualización:** 22 de abril de 2026  
**Versión:** 1.0.0 (Beta)

¿Preguntas? Abre un issue o contacta al equipo de desarrollo.
