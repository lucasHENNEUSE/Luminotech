// Convertir une ville en coordonnées via API Nominatim
async function getCoordinates(city) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${city}`;
    const response = await fetch(url);
    return response.json();
}

// Appel Open Meteo
async function getWeather(lat, lon) {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&daily=temperature_2m_max,weather_code&timezone=Europe/Paris&forecast_days=2`;
    const response = await fetch(url);
    return response.json();
}

// Logique choix du vin
function getWineSuggestion(temp, code) {
    let style, conseil, critere;

    if (temp > 28) {
        style = "Rosé / Bulles";
        conseil = "Servir bien frais, 2h au frigo.";
        critere = "Idéal quand il fait très chaud.";
    } else if (temp >= 20) {
        style = "Blanc vif";
        conseil = "Servir entre 8–10°C.";
        critere = "Acidité rafraîchissante.";
    } else if (temp >= 15) {
        style = "Rouge structuré";
        conseil = "Aérer 20–30 min.";
        critere = "Parfait par température modérée.";
    } else {
        style = "Rouge puissant";
        conseil = "Servir vers 17–18°C.";
        critere = "Apporte rondeur et chaleur.";
    }

    if (code >= 61 && code <= 69) {
        style = "Rouge léger";
        critere = "Pluie → vin réconfortant.";
    }

    return { style, conseil, critere };
}

// Mise à jour du DOM
function renderWeather(data, idPrefix) {
    document.getElementById("temp" + idPrefix).textContent = data.temp + "°C";
    document.getElementById("cond" + idPrefix).textContent = data.condition;
    document.getElementById("vin" + idPrefix).textContent = data.wine.style;
    document.getElementById("adv" + idPrefix).textContent = data.wine.conseil;
    document.getElementById("crit" + idPrefix).textContent = data.wine.critere;
}

// Message helper
function status(msg, color = "#4b1e1e") {
    const el = document.getElementById("statusMsg");
    el.textContent = msg;
    el.style.color = color;
}

document.getElementById("searchBtn").addEventListener("click", async () => {
    const city = document.getElementById("cityInput").value.trim();

    if (!city) {
        status("Veuillez entrer une ville.", "red");
        return;
    }

    status("Recherche de la ville...", "#4b1e1e");

    const results = await getCoordinates(city);

    if (results.length === 0) {
        status("❌ Ville introuvable. Vérifiez l'orthographe.", "red");
        return;
    }

    const lat = results[0].lat;
    const lon = results[0].lon;

    status("Chargement de la météo...");

    const weather = await getWeather(lat, lon);

    // AUJOURD’HUI
    const today = {
        temp: weather.daily.temperature_2m_max[0],
        condition: "Code " + weather.daily.weather_code[0],
        wine: getWineSuggestion(
            weather.daily.temperature_2m_max[0],
            weather.daily.weather_code[0]
        )
    };

    // DEMAIN
    const tomorrow = {
        temp: weather.daily.temperature_2m_max[1],
        condition: "Code " + weather.daily.weather_code[1],
        wine: getWineSuggestion(
            weather.daily.temperature_2m_max[1],
            weather.daily.weather_code[1]
        )
    };

    renderWeather(today, "Today");
    renderWeather(tomorrow, "Tom");

    status("Résultats mis à jour !");
});
