const validateBtn = document.getElementById("validateBtn");
const confirmBox = document.getElementById("confirmBox");

const recapPlat = document.getElementById("recapPlat");
const recapVin = document.getElementById("recapVin");
const recapDetail = document.getElementById("recapDetail");

validateBtn.addEventListener("click", () => {
    const plat = document.getElementById("suggestPlat").value;
    const vin = document.getElementById("suggestVin").value;
    const detail = document.getElementById("suggestDetail").value;

    // Remplit la fenêtre de confirmation
    recapPlat.textContent = plat || "—";
    recapVin.textContent = vin || "—";
    recapDetail.textContent = detail || "—";

    confirmBox.style.display = "flex";
});

// Annuler
document.getElementById("cancelConfirm").addEventListener("click", () => {
    confirmBox.style.display = "none";
});

// Confirmer l’envoi
document.getElementById("confirmSend").addEventListener("click", async () => {
    const data = {
        plat: document.getElementById("suggestPlat").value,
        vin: document.getElementById("suggestVin").value,
        detail: document.getElementById("suggestDetail").value
    };

    // METS ICI TON URL D’API
    const API_URL = "http://localhost:5500/suggestion";

    try {
        await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        window.location.href = "app.html"; // retour page précédente

    } catch (error) {
        alert("Erreur : impossible d'envoyer la suggestion.");
    }
});
