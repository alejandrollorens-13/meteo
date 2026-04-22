"""Pruebas con mocks para llamadas externas mediante httpx.AsyncClient."""

from pathlib import Path
import sys
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from fastapi import HTTPException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = PROJECT_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from main import fetch_open_meteo_weather


@pytest.mark.asyncio
@patch("main.httpx.AsyncClient")
async def test_fetch_open_meteo_weather_success(mock_async_client_class):
    """Debe parsear correctamente una respuesta simulada de Open Meteo."""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "latitude": 40.4168,
        "longitude": -3.7038,
        "timezone": "Europe/Madrid",
        "current": {
            "temperature_2m": 22.5,
            "weather_code": 1,
            "wind_speed_10m": 10.0,
        },
        "hourly": {
            "time": ["2026-04-22T10:00", "2026-04-22T11:00"],
            "temperature_2m": [22.5, 23.0],
            "weather_code": [1, 2],
        },
    }

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_async_client_class.return_value = mock_client

    result = await fetch_open_meteo_weather(40.4168, -3.7038)

    assert result.success is True
    assert result.location["timezone"] == "Europe/Madrid"
    assert result.current_weather.condition == "Parcialmente nublado"
    assert len(result.forecast) == 2


@pytest.mark.asyncio
@patch("main.httpx.AsyncClient")
async def test_fetch_open_meteo_weather_request_error(mock_async_client_class):
    """Debe traducir error de conexión a HTTPException 503."""
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get = AsyncMock(side_effect=httpx.RequestError("network down"))
    mock_async_client_class.return_value = mock_client

    with pytest.raises(HTTPException) as exc_info:
        await fetch_open_meteo_weather(40.0, -3.0)

    assert exc_info.value.status_code == 503
