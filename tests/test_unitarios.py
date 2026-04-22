"""Pruebas unitarias de funciones puras y modelos del backend."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from main import CurrentWeather, WeatherResponse, map_weather_code_to_condition


def test_map_weather_code_clear_sky():
    """Debe mapear código 0 a despejado."""
    assert map_weather_code_to_condition(0) == "Despejado"


def test_map_weather_code_rain():
    """Debe mapear códigos de lluvia correctamente."""
    assert map_weather_code_to_condition(61) == "Lluvia"


def test_map_weather_code_unknown():
    """Debe devolver estado desconocido para códigos no contemplados."""
    assert map_weather_code_to_condition(999) == "Condición desconocida"


def test_current_weather_model_shape():
    """Debe crear un modelo CurrentWeather válido."""
    model = CurrentWeather(temperature=22.4, condition="Despejado", wind_speed=8.2)
    assert model.temperature == 22.4
    assert model.condition == "Despejado"
    assert model.wind_speed == 8.2


def test_weather_response_model_shape():
    """Debe crear un modelo WeatherResponse válido."""
    current = CurrentWeather(temperature=19.0, condition="Niebla", wind_speed=3.1)
    payload = WeatherResponse(
        success=True,
        location={"name": "Madrid", "latitude": 40.4, "longitude": -3.7, "timezone": "Europe/Madrid"},
        current_weather=current,
        forecast=[{"time": "2026-04-22T10:00", "temperature": 20.0, "weather_code": 1}],
    )

    assert payload.success is True
    assert payload.location["name"] == "Madrid"
    assert payload.current_weather.condition == "Niebla"
    assert len(payload.forecast) == 1
