async function sendMessage() {
    const inputElement = document.getElementById("userInput");
    const msg = inputElement.value;
    if (!msg) return;

    // On utilise URLSearchParams pour envoyer le texte correctement à FastAPI
    const params = new URLSearchParams({ message: msg });

    const res = await fetch(`http://127.0.0.1:8000/sommelier/chat?${params}`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });

    const data = await res.json();

    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `
        <div style="margin-bottom:10px;">
            <p><strong>Moi :</strong> ${msg}</p>
            <p style="background:#f0f0f0; padding:10px; border-radius:5px;">
                <strong>Sommelier IA :</strong> ${data.response.replace(/\n/g, '<br>')}
            </p>
        </div>
    `;
    inputElement.value = ""; // Vide le champ après envoi
}