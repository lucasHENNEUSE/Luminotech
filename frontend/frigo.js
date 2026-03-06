const API_URL = "http://127.0.0.1:8000";

// 1. Charger l'inventaire au lancement
async function refreshFrigo() {
    try {
        const res = await fetch(`${API_URL}/frigo`);
        const data = await res.json();
        const tbody = document.getElementById('frigo-body');
        
        if (!tbody) return; // Sécurité si l'élément n'existe pas
        
        tbody.innerHTML = "";

        data.forEach(item => {
            const statusClass = item.urgent ? 'urgent' : 'ok';
            tbody.innerHTML += `
                <tr>
                    <td><input type="checkbox" class="ingredient-check" value="${item.nom}"></td>
                    <td style="font-weight: 500;">${item.nom}</td>
                    <td>${item.date_ajout}</td>
                    <td class="${statusClass}">${item.jours_restants} jours</td>
                </tr>
            `;
        });
    } catch (e) {
        console.error("Erreur de connexion à l'API :", e);
    }
}

// 2. Ajouter un aliment
async function ajouterAliment() {
    const input = document.getElementById('nomAliment');
    const nom = input.value;
    if (!nom) return alert("Veuillez entrer un nom d'aliment !");

    try {
        await fetch(`${API_URL}/frigo/ajouter/${nom}`, { method: 'POST' });
        input.value = "";
        refreshFrigo(); // Rafraîchir la liste après l'ajout
    } catch (e) {
        console.error("Erreur lors de l'ajout :", e);
    }
}

// 3. Demander une recette (Sauvegarde et Redirection vers chat.html)
function demanderRecette() {
    // On récupère les noms des ingrédients cochés
    const selected = Array.from(document.querySelectorAll('.ingredient-check:checked'))
                          .map(cb => cb.value);
    
    if (selected.length === 0) {
        return alert("Sélectionnez au moins un ingrédient pour que Bacchus puisse vous aider !");
    }

    // On sauvegarde la liste dans la mémoire du navigateur (LocalStorage)
    localStorage.setItem('ingredientsSelectionnes', JSON.stringify(selected));

    // On redirige vers la page du chat
    window.location.href = "chat.html";
}

// 4. Tout sélectionner / Désélectionner
function toggleAll() {
    const master = document.getElementById('checkAll');
    const checks = document.querySelectorAll('.ingredient-check');
    if (master) {
        checks.forEach(c => c.checked = master.checked);
    }
}

// Charger les données dès l'ouverture de la page
window.onload = refreshFrigo;