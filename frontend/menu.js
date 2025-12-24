function getWineSuggestion(temp, code, repas = "normal") {
    let style, conseil, critere;

    const pluie = code >= 61 && code <= 69;
    const froid = temp < 15;
    const chaud = temp >= 25;

    // 1 Priorité météo difficile
    if (pluie || froid) {
        style = "Rouge structuré";
        conseil = "Servir à 17–18°C, aérer 30 min.";
        critere = "Temps frais ou pluvieux → vin réconfortant.";
    }

    // 2 Repas copieux
    else if (repas === "copieux") {
        style = "Rouge puissant";
        conseil = "Carafer 1h si possible.";
        critere = "Accorde la richesse du plat.";
    }

    // 3 Forte chaleur
    else if (chaud) {
        style = "Blanc vif ou Rosé";
        conseil = "Servir bien frais (8–10°C).";
        critere = "Rafraîchissant par temps chaud.";
    }

    // 4 Cas équilibré
    else {
        style = "Rouge léger ou Blanc sec";
        conseil = "Servir à 12–15°C.";
        critere = "Polyvalent et harmonieux.";
    }

    return { style, conseil, critere };
}


document.getElementById("generateBtn").addEventListener("click", () => {

    const season = seasonSelect().value;
    const weather = weatherSelect().value;
    const meal = mealSelect().value;

    let starter, main, cheese, wine, advice;

    if (weather === "Froid" || weather === "Pluvieux" || season === "Hiver") {
        starter = "Velouté de champignons";
        main = "Bœuf mijoté au vin rouge";
        cheese = "Comté affiné";
        wine = "Rouge structuré – Bourgogne";
        advice = "Servir à 17°C, carafer 30 minutes.";
    } else if (weather === "Chaud" || season === "Été") {
        starter = "Salade fraîcheur";
        main = "Poisson grillé";
        cheese = "Chèvre frais";
        wine = "Blanc vif – Loire";
        advice = "Servir bien frais entre 8–10°C.";
    } else if (season === "Hiver") {
        starter = "Soupe à l'oignon";
        main = "Cassoulet";
        cheese = "Roquefort";
        wine = "Rouge puissant – Cahors";
        advice = "Servir à 18°C, parfait pour réchauffer.";
    } else if (season === "Été") {
        starter = "Tartare de tomates";
        main = "Brochettes de légumes grillés";
        cheese = "Feta";
        wine = "Rosé – Provence";
        advice = "Servir frais entre 10–12°C.";
    } else if (season === "Automne") { 
        starter = "Salade de saison";
        main = "Risotto aux champignons";
        cheese = "Tomme de Savoie";
        wine = "Rouge léger – Beaujolais";
        advice = "Servir à 15–16°C, parfait pour l'automne.";
    }else if (season === "Printemps") {
        starter = "Asperges vinaigrette";
        main = "Poulet aux herbes";
        cheese = "Crottin de Chavignol";
        wine = "Blanc sec – Sancerre";
        advice = "Servir frais entre 10–12°C, idéal pour le printemps.";
    }else if (season === "Été" && weather === "Chaud") {
        starter = "Gaspacho";
        main = "Salade niçoise";
        cheese = "Brousse";
        wine = "Rosé frais – Provence";
        advice = "Servir très frais entre 8–10°C.";
    }else if (season === "Hiver" && weather === "Froid") {
        starter = "Soupe de potiron";
        main = "Gratin dauphinois";
        cheese = "Reblochon";
        wine = "Rouge corsé – Rhône";
        advice = "Servir à 18°C, parfait pour les journées froides.";
    }else if (season === "Hiver" && weather === "Pluvieux") {
        starter = "Velouté de potiron";
        main = "Chili con carne";
        cheese = "Cantal";
        wine = "Rouge épicé – Languedoc";
        advice = "Servir à 17–18°C, idéal pour les jours de pluie.";
    }else if (season === "Hiver" && weather === "Ensoleillé") {
        starter = "Salade d'endives aux noix";
        main = "Magret de canard";
        cheese = "Fourme d'Ambert";
        wine = "Rouge fruité – Sud-Ouest";
        advice = "Servir à 16–18°C, parfait pour une journée ensoleillée.";
    }else if (season === "Hiver" && weather === "Neige" && meal !== "Dîner"){
        starter = "Fondue savoyarde";
        main = "Tartiflette";
        cheese = "Beaufort";
        wine = "Vin chaud épicé";
        advice = "Servir chaud, parfait pour les journées enneigées.";  
    }else if (season === "Hiver" && weather === "Nuageux"){
        starter = "Bruschetta aux champignons";
        main = "Pâtes à la carbonara";
        cheese = "Parmesan";
        wine = "Rouge léger – Beaujolais";
        advice = "Servir à 15–16°C, idéal pour une journée nuageuse.";
    }else if (season === "Printemps" && weather === "Pluvieux") {
        starter = "Soupe de légumes printaniers";
        main = "Quiche aux asperges";
        cheese = "Crottin de Chavignol";
        wine = "Blanc sec – Sancerre";
        advice = "Servir frais entre 10–12°C, idéal pour les jours de pluie.";
    }else if (season === "Printemps" && weather === "Ensoleillé") {
        starter = "Salade de fraises et épinards";
        main = "Saumon grillé aux herbes";
        cheese = "Chèvre frais";
        wine = "Blanc aromatique – Loire";
        advice = "Servir bien frais entre 8–10°C.";
    }else if (season === "Printemps" && weather === "Neige") {
        starter = "Velouté de petits pois";
        main = "Gratin de pommes de terre";
        cheese = "Tomme de Savoie";
        wine = "Vin chaud aux épices";
        advice = "Servir chaud, parfait pour les journées enneigées.";
    }else if (season === "Printemps" && weather === "Nuageux") {
        starter = "Salade de roquette et parmesan";
        main = "Pâtes aux légumes printaniers";
        cheese = "Pecorino";
        wine = "Rosé léger – Provence";
        advice = "Servir frais entre 10–12°C, idéal pour une journée nuageuse.";
    }else if (season === "Automne" && weather === "Pluvieux") {
        starter = "Velouté de courge";
        main = "Boeuf bourguignon";
        cheese = "Morbier";
        wine = "Rouge puissant – Bordeaux";
        advice = "Servir à 17–18°C, idéal pour les jours de pluie.";
    }else if (season === "Automne" && weather === "Ensoleillé") {
        starter = "Salade de betteraves rôties";
        main = "Filet de porc aux pommes";
        cheese = "Comté affiné";
        wine = "Rouge fruité – Beaujolais";
        advice = "Servir à 15–16°C, parfait pour une journée ensoleillée.";
    }else if (season === "Automne" && weather === "Neige") {
        starter = "Soupe à la citrouille";
        main = "Gratin dauphinois";
        cheese = "Reblochon";
        wine = "Vin chaud épicé";
        advice = "Servir chaud, parfait pour les journées enneigées.";
    }else if (season === "Automne" && weather === "Nuageux") {
        starter = "Bruschetta aux champignons";
        main = "Risotto aux champignons";
        cheese = "Parmesan";
        wine = "Rouge léger – Bourgogne";
        advice = "Servir à 15–16°C, idéal pour une journée nuageuse.";
    }else if (weather === "Ensoleillé") {
        starter = "Salade de fruits frais";
        main = "Filet de dorade au citron";
        cheese = "Mozzarella di Bufala";
        wine = "Blanc aromatique – Alsace";
        advice = "Servir bien frais entre 8–10°C.";
    }else if (weather === "Neige") {
        starter = "Fondue savoyarde";
        main = "Raclette traditionnelle";
        cheese = "Emmental";
        wine = "Vin chaud épicé";
        advice = "Servir chaud, parfait pour les journées enneigées.";
    }else if (weather === "Nuageux") {
        starter = "Bruschetta aux tomates";
        main = "Pâtes primavera";
        cheese = "Parmesan râpé";
        wine = "Rosé fruité – Languedoc";
        advice = "Servir frais entre 10–12°C, idéal pour une journée nuageuse.";
    } else if (meal === "Nuageux") {
        starter = "Terrine maison";
        main = "Volaille rôtie";
        cheese = "Brie";
        wine = "Rouge léger – Beaujolais";
        advice = "Servir à 15–16°C.";
    }
    if (meal === "végétarien") {
        starter = "Salade de quinoa aux légumes";
        main = "Curry de légumes";
        cheese = "Fromage de chèvre";
        wine = "Blanc sec – Sauvignon";
        advice = "Servir frais, équilibre les saveurs végétales.";
    }
    if (meal === " barbecue") {
        starter = "Brochettes de légumes";
        main = "Côtes de porc grillées";
        cheese = "Cheddar affiné";
        wine = "Zinfandel – Californie";
        advice = "Servir à 16–18°C, accompagne bien les grillades.";
    }
    if (meal === "romantique") {
        starter = "Foie gras sur toast";
        main = "Filet mignon aux morilles";
        cheese = "Camembert affiné";
        wine = "Pinot Noir – Bourgogne";
        advice = "Servir à 15–16°C, élégant et raffiné.";
    }
    if (meal === "apéritif") {
        starter = "Gougères au fromage";
        main = "Mini quiches variées";
        cheese = "Fromage à pâte molle";
        wine = "Prosecco – Italie";
        advice = "Servir très frais, parfait pour débuter.";
    }
    if (meal === "gourmet") {
        starter = "Tartare de saumon";
        main = "Filet de bœuf Rossini";
        cheese = "Coulommiers affiné";
        wine = "Sauternes – Bordeaux";
        advice = "Servir frais, sublime les plats raffinés.";
    }
    if (meal === "repas épicé") {
        starter = "Nems vietnamiens";
        main = "Curry thaïlandais";
        cheese = "Fromage frais";
        wine = "Gewurztraminer – Alsace";
        advice = "Servir frais, équilibre les épices.";
    }
    if (meal === "barbecue") {
        starter = "Brochettes de légumes";
        main = "Côtes de porc grillées";
        cheese = "Cheddar affiné";
        wine = "Zinfandel – Californie";
        advice = "Servir à 16–18°C, accompagne bien les grillades.";
    }   
    if (meal === "Repas léger") {
        wine = "Blanc sec – Sauvignon";
        advice = "Servir frais, parfait pour un repas léger.";
    }

    if (meal === "Repas festif") {
        wine = "Bulles – Champagne";
        advice = "Servir très frais, parfait pour célébrer.";
    }
    if (meal === "Repas copieux") {
        wine = "Rouge puissant – Bordeaux";
        advice = "Carafer 1h, accompagne bien les plats riches.";
    }
    if (meal === "Repas équilibré") {
        wine = "Rosé – Provence";
        advice = "Servir frais, vin polyvalent.";
    }
    if (meal === "Romantique") {
        wine = "Pinot Noir – Bourgogne";
        advice = "Servir à 15–16°C, élégant et raffiné.";
    }
    if (meal === "Apéritif") {
        wine = "Prosecco – Italie";
        advice = "Servir très frais, parfait pour débuter.";
    }
    if (meal === "Barbecue") {
        wine = "Zinfandel – Californie";
        advice = "Servir à 16–18°C, accompagne bien les grillades.";
    }
    if (meal === "Végétarien") {
        wine = "Chardonnay – Bourgogne";
        advice = "Servir frais, équilibre les saveurs végétales.";
    }
    if (meal === "Gourmet") {
        wine = "Sauternes – Bordeaux";
        advice = "Servir frais, sublime les plats raffinés.";
    }
    if (meal === "Repas épicé") {
        wine = "Gewurztraminer – Alsace";
        advice = "Servir frais, équilibre les épices.";
    }
    if (season === "Printemps") {
        advice += " Le printemps invite à la légèreté et à la fraîcheur.";
    }
    else if (season === "Automne") {
        advice += " En automne, privilégiez des vins plus corsés.";
    }
    if (weather === "Pluvieux") {
        advice += " Par temps pluvieux, un vin réconfortant est recommandé.";
    }
    else if (weather === "Ensoleillé") {
        advice += " Par temps ensoleillé, un vin rafraîchissant est parfait.";
    }
    if (season === "Printemps") {
        advice += " Le printemps invite à la légèreté et à la fraîcheur.";
    }
    else if (season === "Automne") {
        advice += " En automne, privilégiez des vins plus corsés.";
    }   

    showResult(starter, main, cheese, wine, advice);
});

function showResult(starter, main, cheese, wine, advice) {
    document.getElementById("starter").textContent = starter;
    document.getElementById("main").textContent = main;
    document.getElementById("cheese").textContent = cheese;
    document.getElementById("wine").textContent = wine;
    document.getElementById("advice").textContent = advice;
    document.getElementById("result").classList.remove("hidden");
}

const seasonSelect = () => document.getElementById("season");
const weatherSelect = () => document.getElementById("weather");
const mealSelect = () => document.getElementById("meal");

const token = localStorage.getItem("token");

async function genererMenu() {
    const saison = document.getElementById("saison").value;
    const meteo = document.getElementById("meteo").value;
    const repas = document.getElementById("repas").value;

    const res = await fetch(
        `http://127.0.0.1:8000/menu?saison=${saison}&meteo=${meteo}&repas=${repas}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await res.json();

    document.getElementById("entree").textContent = data.entree;
    document.getElementById("plat").textContent = data.plat;
    document.getElementById("fromage").textContent = data.fromage;
    document.getElementById("vin").textContent = data.vin;
}
localStorage.setItem("token", data.access_token);

wine: getWineSuggestion(
    weather.daily.temperature_2m_max[0],
    weather.daily.weather_code[0],
    document.getElementById("repas").value
)

function genererListeCourses(entree, plat) {
    const ulEntree = document.getElementById("courses-entree");
    const ulPlat = document.getElementById("courses-plat");

    ulEntree.innerHTML = "";
    ulPlat.innerHTML = "";

    if (RECETTES[entree]?.entree) {
        RECETTES[entree].entree.forEach(i => {
            ulEntree.innerHTML += `<li>${i.nom} : ${i.qte} ${i.unite}</li>`;
        });
    }

    if (RECETTES[plat]?.plat) {
        RECETTES[plat].plat.forEach(i => {
            ulPlat.innerHTML += `<li>${i.nom} : ${i.qte} ${i.unite}</li>`;
        });
    }

    document.getElementById("shopping").classList.remove("hidden");
}
