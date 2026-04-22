from typing import Any
from urllib.parse import quote_plus

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class CurrentWeather(BaseModel):
    temperature: float
    condition: str
    wind_speed: float


class WeatherResponse(BaseModel):
    success: bool
    location: dict[str, Any]
    current_weather: CurrentWeather
    forecast: list[dict[str, Any]]


def map_weather_code_to_condition(weather_code: int | None) -> str:
    if weather_code == 0:
        return "Despejado"
    if weather_code in {1, 2, 3}:
        return "Parcialmente nublado"
    if weather_code in {45, 48}:
        return "Niebla"
    if weather_code in {51, 53, 55, 61, 63, 65}:
        return "Lluvia"
    if weather_code in {71, 73, 75}:
        return "Nieve"
    if weather_code in {95, 96, 99}:
        return "Tormenta"
    return "Condición desconocida"


async def fetch_open_meteo_weather(lat: float, lon: float) -> WeatherResponse:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,weather_code",
        "forecast_days": 7,
        "timezone": "auto",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail="Error de Open Meteo") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="No se pudo conectar con Open Meteo") from exc

    payload = response.json()
    current_payload = payload.get("current", {})
    hourly_payload = payload.get("hourly", {})

    hourly_times = hourly_payload.get("time", [])[:24]
    hourly_temperatures = hourly_payload.get("temperature_2m", [])[:24]
    hourly_weather_codes = hourly_payload.get("weather_code", [])[:24]

    forecast = []
    for index, item_time in enumerate(hourly_times):
        forecast.append(
            {
                "time": item_time,
                "temperature": hourly_temperatures[index] if index < len(hourly_temperatures) else None,
                "weather_code": hourly_weather_codes[index] if index < len(hourly_weather_codes) else None,
            }
        )

    current_weather = CurrentWeather(
        temperature=float(current_payload.get("temperature_2m", 0.0)),
        condition=map_weather_code_to_condition(current_payload.get("weather_code")),
        wind_speed=float(current_payload.get("wind_speed_10m", 0.0)),
    )

    return WeatherResponse(
        success=True,
        location={
            "name": None,
            "latitude": payload.get("latitude", lat),
            "longitude": payload.get("longitude", lon),
            "timezone": payload.get("timezone", "UTC"),
        },
        current_weather=current_weather,
        forecast=forecast,
    )


async def resolve_city_to_coordinates(city: str) -> dict[str, Any]:
    geocode_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={quote_plus(city)}&count=1&language=es&format=json"
    )

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(geocode_url)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail="Error de geocodificación en Open Meteo") from exc
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="No se pudo conectar al servicio de geocodificación") from exc

    results = response.json().get("results", [])
    if not results:
        raise HTTPException(status_code=404, detail="No se encontró la ciudad solicitada")

    first_match = results[0]
    return {
        "name": first_match.get("name", city),
        "latitude": first_match.get("latitude"),
        "longitude": first_match.get("longitude"),
    }

app = FastAPI(title="Meteo API")

# Permite el acceso desde el frontend en entorno local.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/weather", response_model=WeatherResponse)
async def get_weather(
    city: str | None = Query(None, min_length=2, description="Nombre de ciudad"),
    lat: float | None = Query(None, ge=-90, le=90, description="Latitud entre -90 y 90"),
    lon: float | None = Query(None, ge=-180, le=180, description="Longitud entre -180 y 180"),
):
    """Obtiene el clima actual y la previsión de 24 horas por ciudad o coordenadas."""
    location_name: str | None = None

    if city:
        location = await resolve_city_to_coordinates(city)
        lat = float(location["latitude"])
        lon = float(location["longitude"])
        location_name = location["name"]

    if lat is None or lon is None:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar city o ambas coordenadas lat/lon",
        )

    weather_response = await fetch_open_meteo_weather(lat, lon)
    if location_name:
        weather_response.location["name"] = location_name

    return weather_response
