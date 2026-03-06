/**
 * Fonction principale pour envoyer le message à l'IA
 */
async function sendMessage() {
    const inputElement = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const msg = inputElement.value.trim();

    // On ne fait rien si le champ est vide
    if (!msg) return;

    // 1. Afficher le message de l'utilisateur dans le chat
    appendMessage("user", msg);
    
    // Vider le champ de saisie
    inputElement.value = ""; 

    // 2. Afficher un message d'attente pour l'IA
    const loadingId = "loading-" + Date.now();
    appendMessage("ai", "Bacchus réfléchit...", loadingId);

    try {
        /**
         * 3. Appel à ton API FastAPI
         * On envoie juste le message en paramètre d'URL (Query Param)
         * AUCUN header d'authentification n'est requis ici
         */
        const response = await fetch(`http://127.0.0.1:8000/sommelier/chat?message=${encodeURIComponent(msg)}`, {
            method: "POST"
        });

        if (!response.ok) {
            throw new Error(`Erreur serveur : ${response.status}`);
        }

        const data = await response.json();

        // 4. Remplacer le texte d'attente par la réponse réelle de l'agent IA
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) {
            // .replace(/\n/g, '<br>') permet de garder les retours à la ligne de l'IA
            loadingElement.innerHTML = data.response.replace(/\n/g, '<br>');
        }

    } catch (error) {
        console.error("Erreur de connexion :", error);
        const loadingElement = document.getElementById(loadingId);
        if (loadingElement) {
            loadingElement.innerText = "Désolé, je n'arrive pas à me connecter à l'agent IA. Vérifie que ton serveur Python est bien lancé.";
        }
    }

    // Toujours scroller vers le bas pour voir la dernière réponse
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Fonction utilitaire pour créer les bulles de texte
 * @param {string} role - 'user' ou 'ai'
 * @param {string} text - Le contenu du message
 * @param {string} id - ID optionnel pour cibler la bulle plus tard
 */
function appendMessage(role, text, id = null) {
    const chatBox = document.getElementById("chatBox");
    
    // Créer le conteneur du message
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", role);
    
    // Créer le paragraphe de contenu
    const contentP = document.createElement("p");
    if (id) contentP.id = id;
    contentP.innerHTML = text;
    
    messageDiv.appendChild(contentP);
    chatBox.appendChild(messageDiv);
    
    // Scroll automatique
    chatBox.scrollTop = chatBox.scrollHeight;
}

/**
 * Gestionnaire d'événement pour la touche Entrée
 */
document.getElementById("userInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

// Ce code s'exécute automatiquement quand on arrive sur chat.html
window.addEventListener('load', () => {
    const storedIngredients = localStorage.getItem('ingredientsSelectionnes');
    
    if (storedIngredients) {
        const ingredients = JSON.parse(storedIngredients);
        
        // On prépare la question pour Bacchus
        const phraseRecette = `Bonjour Bacchus ! J'ai sélectionné ces ingrédients dans mon frigo : ${ingredients.join(', ')}. Peux-tu me proposer une recette et un vin ?`;
        
        // On nettoie la mémoire pour ne pas que le message revienne en boucle
        localStorage.removeItem('ingredientsSelectionnes');

        // On remplit le champ de texte et on simule un clic sur envoyer
        const inputElement = document.getElementById("userInput");
        if (inputElement) {
            inputElement.value = phraseRecette;
            sendMessage(); // On appelle ta fonction existante qui parle à l'IA
        }
    }
});