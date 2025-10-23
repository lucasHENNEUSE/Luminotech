import pandas as pd 
import logging
from datetime import datetime
import unicodedata # pour la normalisation des accents


CSV_PATH = "./csv/plats_a_la_carte.csv"
OUTPUT_CSV_PATH = "./plats_a_la_carte_transforme.csv"


logging.basicConfig( 
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    
)


def nettoyer_texte(texte: str) -> str:
    """Nettoie et normalise les accents, les espaces et met en minuscule."""
    if pd.isna(texte):
        return ""
    texte = str(texte).strip().lower()
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("utf-8")
    return texte

####################### Extraction #########################
def extract_from_csv(file_path: str) -> pd.DataFrame:
    """Extrait les données d’un fichier CSV avec gestion de l’encodage."""
    try:
        data = pd.read_csv(file_path, encoding="utf-8", sep=";")
        logging.info("Données extraites depuis le fichier CSV (UTF-8).")
        return data
    except UnicodeDecodeError:
        logging.warning("Fichier non UTF-8, tentative avec ISO-8859-1...")
        data = pd.read_csv(file_path, encoding="ISO-8859-1", sep=";")
        logging.info("Données extraites depuis le fichier CSV (ISO-8859-1).")
        return data
    except Exception as e:
        logging.error("Erreur lors de l’extraction du fichier CSV : %s", e)
        raise

###################### Transformation #########################
def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """Transforme le fichier de plats : ajoute les colonnes descriptives + critères."""
    
    # Normalisation des colonnes
    data.columns = [nettoyer_texte(c) for c in data.columns]
    
    if "plat" not in data.columns:
        raise KeyError("La colonne 'plat' est obligatoire dans le CSV.")
    if "critere" not in data.columns:
        raise KeyError("La colonne 'critere' est obligatoire dans le CSV.")

    # Nettoyage du contenu texte
    for col in data.columns:
        data[col] = data[col].apply(nettoyer_texte)

    # Extraire tous les critères uniques
    all_criteres = set()
    for liste in data["critere"]:
        mots = [mot.strip() for mot in liste.split(",") if mot.strip()]
        all_criteres.update(mots)

    all_criteres = sorted(all_criteres)
    logging.info("Critères uniques détectés : %s", ", ".join(all_criteres))

    # Ajouter une colonne pour chaque critère avec "oui" ou "non"
    for crit in all_criteres:
        data[crit] = data["critere"].apply(
            lambda c: "oui" if crit in [m.strip() for m in c.split(",")] else "non"
        )

    # Ajouter des métadonnées
    data["created_at"] = datetime.utcnow().isoformat()
    data["status"] = "actif"

    logging.info("Transformation terminée : %d plats traités, %d critères ajoutés.",
                 len(data), len(all_criteres))
    return data

# ######################## Load #################################
def load_to_csv(data: pd.DataFrame, output_path: str):
    """Sauvegarde le DataFrame transformé dans un fichier CSV."""
    try:
        data.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")
        logging.info("Données sauvegardées dans le fichier : %s", output_path)
    except Exception as e:
        logging.error("Erreur lors de la sauvegarde du CSV : %s", e)
        raise


def main(): # point d'entrée principal
    """Pipeline complet ETL : Extraction → Transformation → Chargement."""
    logging.info("Démarrage du processus ETL (plats et descriptions)...")
    data = extract_from_csv(CSV_PATH) # extraction des données
    data_transformed = transform_data(data) # transformation des données
    load_to_csv(data_transformed, OUTPUT_CSV_PATH) # chargement des données
    logging.info("Processus ETL terminé avec succès.") # fin du processus


if __name__ == "__main__": # point d'entrée du script
    main()
