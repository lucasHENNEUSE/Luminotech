const API_URL = "http://127.0.0.1:8000";

// DOM
const vinSelect = document.getElementById("vinSelect");
const platSelect = document.getElementById("platSelect");
const suggestionText = document.getElementById("suggestionText");
const descriptionText = document.getElementById("descriptionText");

let vins = [];
let plats = [];
let token = null;


// ------------------------------
// 1. LOGIN AUTO
// ------------------------------
async function login() {
    const formData = new URLSearchParams();
    formData.append("username", "lucas");
    formData.append("password", "oceluc");

    const res = await fetch(`${API_URL}/token`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    token = data.access_token;

    return token;
}


// ------------------------------
// 2. CHARGER VINS + PLATS
// ------------------------------
async function loadData() {
    if (!token) await login();

    const headers = { "Authorization": `Bearer ${token}` };

    // Vins
    const resVins = await fetch(`${API_URL}/vins`, { headers });
    vins = await resVins.json();
    fillSelect(vinSelect, vins, "nom_vin");

    // Plats
    const resPlats = await fetch(`${API_URL}/plats`, { headers });
    plats = await resPlats.json();
    fillSelect(platSelect, plats, "nom_plat");
}

function fillSelect(select, list, key) {
    select.innerHTML = '<option value="">— Choisir —</option>';

    list.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item[key];
        opt.textContent = item[key];
        select.appendChild(opt);
    });
}


// ------------------------------
// 3. AFFICHER ACCORDS
// ------------------------------
async function updateSuggestion() {
    const vin = vinSelect.value;
    const plat = platSelect.value;

    if (vin) {
        const res = await fetch(`${API_URL}/accords/par_vin/${vin}`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const accords = await res.json();

        suggestionText.innerHTML = accords.length
            ? accords.map(a => `🥘 ${a.nom_plat} (${a.criteres})`).join("<br>")
            : "Aucun accord trouvé.";

        // Description du vin
        const vinObj = vins.find(v => v.nom_vin === vin);
        descriptionText.textContent = vinObj?.description || "Aucune description.";
    }

    if (plat) {
        const res = await fetch(`${API_URL}/accords/par_plat/${plat}`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const accords = await res.json();

        suggestionText.innerHTML = accords.length
            ? accords.map(a => `🍷 ${a.nom_vin} (${a.criteres})`).join("<br>")
            : "Aucun accord trouvé.";

        // Description du plat
        const platObj = plats.find(p => p.nom_plat === plat);
        descriptionText.textContent = platObj?.criteres || "";
    }
}


// ------------------------------
// ÉVÉNEMENTS
// ------------------------------
vinSelect.addEventListener("change", updateSuggestion);
platSelect.addEventListener("change", updateSuggestion);


// ------------------------------
// LANCEMENT
// ------------------------------
loadData();
