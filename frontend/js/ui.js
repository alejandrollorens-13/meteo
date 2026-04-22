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

  weatherContainer.innerHTML = `
    <div class="weather-shell loading-shell">
      <p class="loading-text">Cargando información meteorológica...</p>
    </div>
  `;
};

const formatForecastDate = (isoDate) => {
  if (!isoDate) return "Sin hora";

  const parsedDate = new Date(isoDate);
  if (Number.isNaN(parsedDate.getTime())) return isoDate;

  return new Intl.DateTimeFormat("es-ES", {
    weekday: "short",
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  }).format(parsedDate);
};

const getAlertClass = (level) => {
  if (level === "high") return "alert-high";
  if (level === "medium") return "alert-medium";
  return "alert-low";
};

export const renderWeather = (data) => {
  const weatherContainer = document.getElementById("weather-container");
  if (!weatherContainer) return;

  const locationName = data?.location?.name ?? "Ubicación seleccionada";
  const timezone = data?.location?.timezone ?? "UTC";
  const temperature = data?.current_weather?.temperature ?? "-";
  const condition = data?.current_weather?.condition ?? "Sin condición";
  const windSpeed = data?.current_weather?.wind_speed ?? "-";
  const alerts = data?.alerts ?? [];

  const forecastItems = (data?.forecast ?? []).slice(0, 24).map((item) => {
    const timeLabel = formatForecastDate(item?.time);
    const itemTemp = item?.temperature ?? "-";
    const weatherCode = item?.weather_code ?? "-";

    return `
      <li class="forecast-item">
        <span class="forecast-time">${timeLabel}</span>
        <span class="forecast-temp">${itemTemp} °C</span>
        <span class="forecast-code">WMO ${weatherCode}</span>
      </li>
    `;
  });

  const alertItems = alerts.map((alert) => {
    const alertClass = getAlertClass(alert?.level);
    const title = alert?.title ?? "Alerta meteorológica";
    const message = alert?.message ?? "Sin detalles disponibles";

    return `
      <div class="weather-alert ${alertClass}">
        <h5>${title}</h5>
        <p>${message}</p>
      </div>
    `;
  });

  weatherContainer.innerHTML = `
    <article class="weather-shell">
      <header class="weather-header">
        <div>
          <h3>${locationName}</h3>
          <p class="weather-timezone">Zona horaria: ${timezone}</p>
        </div>
        <span class="weather-chip">Actualizado</span>
      </header>

      <section class="current-weather-grid">
        <div class="metric-card">
          <p>Temperatura</p>
          <strong>${temperature} °C</strong>
        </div>
        <div class="metric-card">
          <p>Condición</p>
          <strong>${condition}</strong>
        </div>
        <div class="metric-card">
          <p>Viento</p>
          <strong>${windSpeed} km/h</strong>
        </div>
      </section>

      <section class="alerts-section">
        <h4>Alertas meteorológicas</h4>
        ${alertItems.join("") || '<p class="no-alerts">Sin alertas relevantes para las próximas horas.</p>'}
      </section>

      <section>
        <h4>Próximas 24 horas</h4>
        <ul class="forecast-grid">${forecastItems.join("") || "<li>Sin previsión disponible</li>"}</ul>
      </section>
    </article>
  `;
};
