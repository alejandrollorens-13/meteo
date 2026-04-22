export const showError = (message) => {
  const errorContainer = document.getElementById("error-container");
  if (!errorContainer) return;

  errorContainer.textContent = message;
};

export const clearError = () => {
  const errorContainer = document.getElementById("error-container");
  if (!errorContainer) return;

  errorContainer.textContent = "";
};

export const showLoading = () => {
  const weatherContainer = document.getElementById("weather-container");
  if (!weatherContainer) return;

  weatherContainer.innerHTML = "<p>Cargando información meteorológica...</p>";
};

export const renderWeather = (data) => {
  const weatherContainer = document.getElementById("weather-container");
  if (!weatherContainer) return;

  const locationName = data?.location?.name ?? "Ubicación seleccionada";
  const timezone = data?.location?.timezone ?? "UTC";
  const temperature = data?.current_weather?.temperature ?? "-";
  const condition = data?.current_weather?.condition ?? "Sin condición";
  const windSpeed = data?.current_weather?.wind_speed ?? "-";

  const forecastItems = (data?.forecast ?? []).slice(0, 6).map((item) => {
    const timeLabel = item?.time ?? "Sin hora";
    const itemTemp = item?.temperature ?? "-";
    return `<li><strong>${timeLabel}</strong>: ${itemTemp} °C</li>`;
  });

  weatherContainer.innerHTML = `
    <article>
      <h3>${locationName}</h3>
      <p>Temperatura actual: ${temperature} °C</p>
      <p>Condición: ${condition}</p>
      <p>Viento: ${windSpeed} km/h</p>
      <p>Zona horaria: ${timezone}</p>
      <h4>Previsión próxima</h4>
      <ul>${forecastItems.join("") || "<li>Sin previsión disponible</li>"}</ul>
    </article>
  `;
};
