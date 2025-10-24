import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import pandas as pd

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27018/")
db = client["projet_e1"]
collection = db["vins_vinsdefrance"]
accords=pd.read_csv("./scrap_big_data/criteres.csv").set_index('vin')['criteres'].to_dict()
print(accords)

def determine_accompagnement(nom_vin):
    nom_vin_lower = nom_vin.lower()
    for item in  accords:
        if item.lower() in nom_vin_lower:
            return accords[item].strip()
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
                        "criteres": determine_accompagnement(nom_vin)
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
