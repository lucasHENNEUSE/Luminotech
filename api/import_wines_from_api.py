import requests
import sqlite3
from datetime import datetime

# URL de base de l'API publique
BASE_URL = "https://api.sampleapis.com/wines"

# Connexion SQLite
conn = sqlite3.connect("./accords.db")
cursor = conn.cursor()

# Création de la table si elle n’existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS vins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_vin TEXT,
    description TEXT,
    source TEXT,
    criteres TEXT
)
""")

# Liste des catégories de vins à importer
categories = ["reds", "whites", "sparkling"]

for cat in categories:
    print(f" Import de la catégorie : {cat}")
    response = requests.get(f"{BASE_URL}/{cat}")
    if response.status_code != 200:
        print(f" Erreur {response.status_code} pour {cat}")
        continue

    vins = response.json()

    for v in vins:
        nom = v.get("wine") or v.get("title") or "Vin inconnu"
        desc = v.get("description", "Aucune description")
        source = v.get("winery", cat)
        # On fait un critère simple basé sur la catégorie
        crit = "vin rouge" if cat == "reds" else (
            "vin blanc" if cat == "whites" else
            "autre"
        )

        cursor.execute("""
        INSERT INTO vins (nom_vin, description, source, criteres)
        VALUES (?, ?, ?, ?)
        """, (nom, desc, source, crit))

conn.commit()
conn.close()
print(" Données importées avec succès depuis SampleAPIs !")
