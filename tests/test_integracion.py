"""Pruebas de integración del endpoint FastAPI sin red real."""

from pathlib import Path
import sys
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from main import CurrentWeather, WeatherResponse, app

client = TestClient(app)


@patch("main.resolve_city_to_coordinates", new_callable=AsyncMock)
@patch("main.fetch_open_meteo_weather", new_callable=AsyncMock)
def test_get_weather_by_city_ok(mock_fetch_weather, mock_resolve_city):
    """Debe devolver 200 y payload estable cuando city es válido."""
    mock_resolve_city.return_value = {
        "name": "Madrid",
        "latitude": 40.4168,
        "longitude": -3.7038,
    }
    mock_fetch_weather.return_value = WeatherResponse(
        success=True,
        location={"name": None, "latitude": 40.4168, "longitude": -3.7038, "timezone": "Europe/Madrid"},
        current_weather=CurrentWeather(temperature=22.0, condition="Despejado", wind_speed=9.0),
        forecast=[],
    )

    response = client.get("/api/weather", params={"city": "Madrid"})

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["location"]["name"] == "Madrid"



def test_get_weather_missing_params_returns_400():
    """Debe devolver 400 si faltan city y coordenadas."""
    response = client.get("/api/weather")
    assert response.status_code == 400



def test_get_weather_invalid_lat_returns_422():
    """Debe devolver 422 por validación de Query cuando lat es inválida."""
    response = client.get("/api/weather", params={"lat": 100, "lon": 2})
    assert response.status_code == 422
