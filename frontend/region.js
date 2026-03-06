const REGIONS = {
    "Bourgogne": {
        vins: ["Pinot Noir (Gevrey-Chambertin)", "Chablis Domaine Daniel Dampt", "Beaune 1er Cru Château Philippe Le Hardi - Montée Rouges"],
        plats: ["Bœuf bourguignon", "Escargots de Bourgogne", "Jambon persillé"]
    },
    "Alsace": {
        vins: ["Alsace Gewürztraminer Domaine Sperry", "Riesling", "Pinot Gris"],
        plats: ["Choucroute garnie", "Flammekueche", "Baeckeoffe"]
    },
    "Bordeaux": {
        vins: ["Margaux Clos Laborie ", "Saint Estèphe Château Meyney", "Bordeaux Blanc Château Cazette"],
        plats: ["Entrecôte bordelaise", "Canelés", "Lamproie à la bordelaise"]
    },
    "Provence": {
        vins: ["Rosé de Provence", "Bandol", "Clos Cibonne (le Pradet)"],
        plats: ["Bouillabaisse", "Ratatouille", "Tapenade"]
    },
    "Rhone": {
        vins: ["Côtes du Rhône Domaine Brusset - Laurent B", "Châteauneuf-du-Pape", "Hermitage"],
        plats: ["Quenelles lyonnaises", "Gratin dauphinois", "Saucisson chaud"]
    },
    "Corse": {
        vins: ["Patrimonio", "Sciaccarellu", "Muscat du Cap Corse"],
        plats: ["Charcuterie (Lonzu, Coppa)", "Figatellu", "Civet de sanglier"]
    }
};

const params = new URLSearchParams(window.location.search);
const region = params.get("region");

if (region && REGIONS[region]) {
    // AJOUT DE LA CLASSE AU BODY (ex: page-bourgogne)
    document.body.classList.add("page-" + region.toLowerCase());

    document.getElementById("regionTitle").textContent = `Région : ${region}`;
    
    const vinsUl = document.getElementById("vins");
    const platsUl = document.getElementById("plats");

    REGIONS[region].vins.forEach(v => {
        vinsUl.innerHTML += `<li>${v}</li>`;
    });

    REGIONS[region].plats.forEach(p => {
        platsUl.innerHTML += `<li>${p}</li>`;
    });
} else {
    document.getElementById("regionTitle").textContent = "Région inconnue";
}