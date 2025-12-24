// ===============================
// Conversion ville → coordonnées
// ===============================
async function getCoordinates(city) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${city}`;
    const response = await fetch(url);
    return response.json();
}

// ===============================
// Appel API Open-Meteo
// ===============================
async function getWeather(lat, lon) {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,weather_code&timezone=Europe/Paris&forecast_days=2`;
    const response = await fetch(url);
    return response.json();
}

// ===============================
// Traduction codes météo (WMO)
// ===============================
function getWeatherDescription(code) {
    const descriptions = {
        0: "☀️ Ensoleillé",
        1: "🌤️ Peu nuageux",
        2: "⛅ Partiellement nuageux",
        3: "☁️ Couvert",
        45: "🌫️ Brouillard",
        48: "🌫️ Brouillard givrant",

        51: "🌦️ Bruine légère",
        53: "🌦️ Bruine modérée",
        55: "🌧️ Bruine forte",

        61: "🌧️ Pluie faible",
        63: "🌧️ Pluie modérée",
        65: "🌧️ Pluie forte",

        66: "🌧️ Pluie verglaçante",
        67: "🌧️ Pluie verglaçante forte",

        71: "❄️ Neige faible",
        73: "❄️ Neige modérée",
        75: "❄️ Neige forte",

        80: "🌦️ Averses faibles",
        81: "🌦️ Averses modérées",
        82: "🌦️ Averses fortes",

        95: "⛈️ Orage",
        96: "⛈️ Orage avec grêle",
        99: "⛈️ Orage violent"
    };

    return descriptions[code] || "🌥️ Temps variable";
}

// ===============================
// Logique de suggestion de vin
// ===============================
function getWineSuggestion(temp, code) {
    let style, conseil, critere;

    if (temp > 28) {
        style = "Rosé / Bulles";
        conseil = "Servir très frais (2h au réfrigérateur).";
        critere = "Parfait pour les fortes chaleurs.";
    } else if (temp >= 20) {
        style = "Blanc vif";
        conseil = "Servir entre 8 et 10°C.";
        critere = "Fraîcheur et vivacité.";
    } else if (temp >= 15) {
        style = "Rouge structuré";
        conseil = "Aérer 20 à 30 minutes.";
        critere = "Équilibré et élégant.";
    } else {
        style = "Rouge puissant";
        conseil = "Servir autour de 17–18°C.";
        critere = "Idéal par temps frais.";
    }

    // Ajustement météo pluvieuse
    if (code >= 61 && code <= 69) {
        style = "Rouge léger";
        critere = "Temps pluvieux → vin réconfortant.";
    }

    return { style, conseil, critere };
}

// ===============================
// Affichage dans le DOM
// ===============================
function renderWeather(data, idPrefix) {
    document.getElementById("temp" + idPrefix).textContent = data.temp + "°C";
    document.getElementById("cond" + idPrefix).textContent = data.condition;
    document.getElementById("vin" + idPrefix).textContent = data.wine.style;
    document.getElementById("adv" + idPrefix).textContent = data.wine.conseil;
    document.getElementById("crit" + idPrefix).textContent = data.wine.critere;
}

// ===============================
// Message d’état
// ===============================
function status(msg, color = "#4b1e1e") {
    const el = document.getElementById("statusMsg");
    el.textContent = msg;
    el.style.color = color;
}

// ===============================
// Bouton de recherche
// ===============================
document.getElementById("searchBtn").addEventListener("click", async () => {
    const city = document.getElementById("cityInput").value.trim();

    if (!city) {
        status("Veuillez entrer une ville.", "red");
        return;
    }

    status("Recherche de la ville...");

    try {
        const results = await getCoordinates(city);

        if (results.length === 0) {
            status("Ville introuvable.", "red");
            return;
        }

        const lat = results[0].lat;
        const lon = results[0].lon;

        status("Chargement de la météo...");

        const weather = await getWeather(lat, lon);

        // AUJOURD’HUI
        const today = {
            temp: weather.daily.temperature_2m_max[0],
            condition: getWeatherDescription(weather.daily.weather_code[0]),
            wine: getWineSuggestion(
                weather.daily.temperature_2m_max[0],
                weather.daily.weather_code[0]
            )
        };

        // DEMAIN
        const tomorrow = {
            temp: weather.daily.temperature_2m_max[1],
            condition: getWeatherDescription(weather.daily.weather_code[1]),
            wine: getWineSuggestion(
                weather.daily.temperature_2m_max[1],
                weather.daily.weather_code[1]
            )
        };

        renderWeather(today, "Today");
        renderWeather(tomorrow, "Tom");

        status("Résultats pour " + results[0].display_name.split(",")[0]);

    } catch (error) {
        status("Erreur lors de la récupération des données.", "red");
        console.error(error);
    }
});
