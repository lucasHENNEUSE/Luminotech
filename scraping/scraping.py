import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# Chargement des critères depuis le CSV
accords = pd.read_csv("./scrap_big_data/criteres.csv").set_index('vin')['criteres'].to_dict()
print(accords)

def determine_accompagnement(nom_vin):
    """Associe un critère (viande, poisson, etc.) selon le nom du vin"""
    nom_vin_lower = nom_vin.lower()
    for item in accords:
        if item.lower() in nom_vin_lower:
            return accords[item].strip()
    return "végétarien"  # valeur par défaut


def scrape_vinsdefrance(nombre_pages=2):
    """Scraping du site Vins de France Roanne"""
    base_url = "https://www.vinsdefrance-roanne.fr/vins-1.html"
    all_vins = []

    for page in range(1, nombre_pages):
        print(f"Page {page} en cours...")
        url = f"{base_url}?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        blocs = soup.find_all("div", class_="ct-description")
        print(f"{len(blocs)} blocs trouvés sur la page {page}.")

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
                        desc_parts.append(
                            sibling.get_text(strip=True)
                            if hasattr(sibling, "get_text")
                            else str(sibling).strip()
                        )
                    desc = " ".join(filter(None, desc_parts)).strip()

                    vin = {
                        "nom": nom_vin,
                        "description": desc,
                        "source": "Vins de France Roanne",
                        "criteres": determine_accompagnement(nom_vin),
                    }
                    all_vins.append(vin)
        time.sleep(2)

    return all_vins


def save_to_csv(data, file_path="vins_scrapes.csv"):
    """Sauvegarde les données extraites dans un fichier CSV"""
    if data:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"{len(data)} vins enregistrés dans le fichier : {file_path}")
    else:
        print("Aucune donnée à enregistrer.")


def main():
    vins = scrape_vinsdefrance(nombre_pages=2)
    save_to_csv(vins)


if __name__ == "__main__":
    main()
