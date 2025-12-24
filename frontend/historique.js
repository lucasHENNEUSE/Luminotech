const API_URL = "http://localhost:8000";
const TOKEN = localStorage.getItem("token");

async function loadHistory() {
    const res = await fetch(`${API_URL}/suggestions`, {
        headers: { Authorization: `Bearer ${TOKEN}` }
    });
    const data = await res.json();

    const box = document.getElementById("historyBox");
    box.innerHTML = "";

    data.forEach(s => {
        const div = document.createElement("div");
        div.className = "suggestion";
        div.innerHTML = `
            <p><strong>Plat :</strong> ${s.plat}</p>
            <p><strong>Vin :</strong> ${s.vin}</p>
            <p><strong>Critères :</strong> ${s.criteres}</p>
            <button class="delete-btn" onclick="deleteOne(${s.id})">Supprimer</button>
        `;
        box.appendChild(div);
    });
}

async function deleteOne(id) {
    await fetch(`${API_URL}/suggestions/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${TOKEN}` }
    });
    loadHistory();
}

document.getElementById("clearAll").addEventListener("click", async () => {
    if (!confirm("Supprimer tout l'historique ?")) return;

    await fetch(`${API_URL}/suggestions`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${TOKEN}` }
    });
    loadHistory();
});

loadHistory();
