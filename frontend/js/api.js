const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchWeather = async (city) => {
  const url = `${API_BASE_URL}/api/weather?city=${encodeURIComponent(city)}`;
  const response = await fetch(url);

  if (!response.ok) {
    let message = "No se pudo obtener la información meteorológica.";

    try {
      const errorPayload = await response.json();
      message = errorPayload?.detail ?? message;
    } catch {
      // Mantiene mensaje por defecto si la respuesta no es JSON.
    }

    throw new Error(message);
  }

  return response.json();
};
