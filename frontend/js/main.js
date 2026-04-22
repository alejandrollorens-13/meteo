import { fetchWeather } from "./api.js";
import { clearError, renderWeather, showError, showLoading } from "./ui.js";

const form = document.getElementById("weather-form");
const cityInput = document.getElementById("city-input");

const handleSearch = async (event) => {
  event.preventDefault();
  clearError();

  const city = cityInput?.value?.trim();
  if (!city) {
    showError("Introduce una ciudad válida.");
    return;
  }

  try {
    showLoading();
    const weatherData = await fetchWeather(city);
    renderWeather(weatherData);
  } catch (error) {
    showError(error.message || "No se pudo obtener la información meteorológica.");
  }
};

if (form) {
  form.addEventListener("submit", handleSearch);
}
