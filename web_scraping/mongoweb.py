import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27018/")
db = client["projet_e1"]
collection = db["vins_vinsdefrance"]

# Dictionnaire complet des accords vin/met
accords = {
    "Cornas Terres Brulées": "viande rouge",
    "Cahors Grand Cru": "viande rouge",
    "Hermitage, Le chevalier de Sterimberg": "viande rouge",
    "Clos Vougeot Le Petit Mauperthuis": "viande rouge",
    "Rully 1er cru  \"Préaux\"": "viande blanche",
    "Chambolle Musigny": "viande rouge",
    "Gevrey Chambertin": "viande rouge",
    "Morey Saint-Denis": "viande rouge",
    "Bonnes Mares Grand Cru": "viande rouge",
    "Grand Echezeaux Grand Cru": "viande rouge",
    "Clos Vougeot Grand Cru": "viande rouge",
    "Charmes Chambertin": "viande rouge",
    "Bandol": "viande rouge",
    "Châteauneuf du Pape": "viande rouge",
    "Crozes-Hermitage": "viande rouge",
    "Cornas : Cuvée Jana": "viande rouge",
    "Hermitage Les Bessards": "viande rouge",
    "Hermitage Ligne de Crête": "viande rouge",
    "Hermitage": "viande rouge",
    "Côtes du Vivarais": "viande rouge",
    "Madiran": "viande rouge",
    "Cahors : New Black Wine": "viande rouge",
    "Margaux": "viande rouge",
    "Saint-Emilion Premier GCC B": "viande rouge",
    "Saint-Julien": "viande rouge",
    "Pauillac": "viande rouge",
    "Pessac-Léognan": "viande rouge",
    "Les Brunes": "viande rouge",
    "Minervois": "viande rouge",
    "Domaine Lafage": "viande rouge",
    "Barolo": "viande rouge",
    "Brunello di Montalcino": "viande rouge",

    # Vins blancs
    "Rully 1er cru La Pucelle": "poisson",
    "Chablis Grand Cru Valmur": "poisson",
    "Chevalier Montrachet Grand Cru": "poisson",
    "Sauternes": "végétarien",
    "Sancerre Exils": "poisson",
    "Sancerre Le Mont Damné": "poisson",
    "Montlouis sur Loire": "poisson",
    "Vouvray Vincent Foreau": "végétarien",
    "Pouilly Fumé": "poisson",
    "Condrieu Chery": "poisson",

    # Autres
    "Magnum Prestige": "végétarien",
    "Vin rouge": "viande rouge"
}

def determine_accompagnement(nom_vin):
    nom_vin_lower = nom_vin.lower()
    for cle, accomp in accords.items():
        if cle.lower() in nom_vin_lower or nom_vin_lower in cle.lower():
            return accomp
    return "végétarien"  # valeur par défaut

def scrape_vinsdefrance(nombre_pages=2):
    base_url = "https://www.vinsdefrance-roanne.fr/vins-1.html"
    all_vins = []

    for page in range(1, nombre_pages):
        print(f"Page {page} en cours...")
        url = f"{base_url}?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        blocs = soup.find_all("div", class_="ct-description")
        print(f" {len(blocs)} blocs trouvés sur la page {page}.")

        for bloc in blocs:
            paragraphes = bloc.find_all("p")
            for p in paragraphes:
                strongs = p.find_all("strong")
                for strong in strongs:
                    nom_vin = strong.text.strip()
                    desc_parts = []
                    for sibling in strong.next_siblings:
                        if sibling.name == "br":
                            break
                        desc_parts.append(sibling.get_text(strip=True) if hasattr(sibling, "get_text") else str(sibling).strip())
                    desc = " ".join(filter(None, desc_parts)).strip()
                    
                    vin = {
                        "nom": nom_vin,
                        "description": desc,
                        "source": "Vins de France Roanne",
                        "accompagnement": determine_accompagnement(nom_vin)
                    }
                    all_vins.append(vin)
        time.sleep(2)

    return all_vins

def save_to_mongo(data):
    if data:
        collection.insert_many(data)
        print(f"{len(data)} vins enregistrés dans MongoDB.")
    else:
        print("Aucune donnée à enregistrer.")

def main():
    vins = scrape_vinsdefrance(nombre_pages=2)
    save_to_mongo(vins)

if __name__ == "__main__":
    main()
