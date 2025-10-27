"""
main.py — Point d’entrée principal du projet Luminotech
-------------------------------------------------------
Ce script orchestre toutes les étapes du pipeline :
1️⃣ Extraction & transformation des données CSV
2️⃣ Scraping + insertion MongoDB
3️⃣ Import des vins depuis l’API publique
4️⃣ Construction de la base SQLite finale
5️⃣ Lancement du serveur FastAPI
"""

import os
import subprocess
import logging
from time import sleep
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%H:%M:%S",
)

# Étapes du pipeline
STEPS = [
    {
        "name": "ETL CSV → plats_a_la_carte_transforme.csv",
        "command": ["python", "csv/ETL.py"],
    },
    {
        "name": "Scraping & insertion dans MongoDB",
        "command": ["python", "scrap_big_data/mongoweb.py"],
    },
    {
        "name": "Import des vins depuis l’API publique",
        "command": ["python", "api/import_wines_from_api.py"],
    },
    {
        "name": "Création et remplissage de la base SQLite",
        "command": ["python", "sql/script.py"],
    },
]


def run_step(step):
    """Exécute une étape du pipeline avec affichage clair."""
    logging.info(f"🚀 Démarrage de l’étape : {step['name']}")
    try:
        subprocess.run(step["command"], check=True)
        logging.info(f"✅ Étape terminée : {step['name']}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erreur pendant l’étape : {step['name']}")
        logging.error(str(e))
        exit(1)
    sleep(1)


def run_pipeline():
    """Orchestre le pipeline complet."""
    logging.info("🧾 Lancement du pipeline complet Luminotech...")
    logging.info("-" * 60)

    start_time = datetime.now()

    for step in STEPS:
        run_step(step)

    duration = (datetime.now() - start_time).total_seconds()
    logging.info(f"Pipeline terminé en {duration:.2f} secondes.")
    logging.info("-" * 60)


def launch_api():
    """Lance le serveur FastAPI avec uvicorn."""
    logging.info("Démarrage de l’API FastAPI...")
    try:
        subprocess.run(["uvicorn", "api.api:app", "--reload"])
    except KeyboardInterrupt:
        logging.warning("Arrêt manuel de l’API FastAPI.")
    except Exception as e:
        logging.error(f"Erreur lors du lancement de l’API : {e}")


if __name__ == "__main__":
    logging.info("Début du processus complet Luminotech")
    logging.info("Vérification de l’environnement...")

    # Vérifie que les chemins essentiels existent
    required_dirs = ["csv", "scrap_big_data", "api", "sql"]
    for d in required_dirs:
        if not os.path.exists(d):
            logging.error(f"Dossier manquant : {d}")
            exit(1)

    # Exécute le pipeline complet
    run_pipeline()

    # Lancement de l’API FastAPI
    launch_api()
