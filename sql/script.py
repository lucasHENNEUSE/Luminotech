import csv
import sqlite3
from datetime import datetime
from pymongo import MongoClient
import random

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27018/")
db = client["projet_e1"]
collection = db["vins_vinsdefrance"]

# Chemin vers ton CSV
csv_file = "./sql/plats_clean.csv"

# Connexion SQLite
conn = sqlite3.connect("accords.db")
cursor = conn.cursor()

# Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS plats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_plat TEXT,
    type_plat TEXT,
    criteres TEXT,
    created_at TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_vin TEXT,
    description TEXT,
    source TEXT,
    criteres TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accords_met_vin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plat_id INTEGER,
    vin_id INTEGER,
    created_at TEXT,
    status TEXT,
    FOREIGN KEY (plat_id) REFERENCES plats(id),
    FOREIGN KEY (vin_id) REFERENCES vins(id)
)
""")
conn.commit()

# Remplir la table vins depuis MongoDB
vins = list(collection.find())
for vin in vins:
    cursor.execute("""
        INSERT INTO vins (nom_vin, description, source, criteres)
        VALUES (?, ?, ?, ?)
    """, (
        vin.get("nom"),
        vin.get("description", ""),
        vin.get("source", ""),
        vin.get("criteres", vin.get("accompagnement", "vegetarien"))  # prend criteres si existe sinon accompagnement
    ))

conn.commit()

# Remplir la table plats depuis CSV
plats = []
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("""
            INSERT INTO plats (nom_plat, type_plat, criteres, created_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, (row["nom_plat"], row["type_plat"], row["criteres"].lower(), datetime.now().isoformat(), "actif"))
        plats.append({"id": cursor.lastrowid, "criteres": row["criteres"].lower()})

conn.commit()

# Créer les accords : max 3 vins par plat
for plat in plats:
    # récupérer les vins correspondant au critere du plat
    vins_matches = list(cursor.execute("SELECT id FROM vins WHERE criteres=?", (plat["criteres"],)))
    if vins_matches:
        vins_selectionnes = random.sample(vins_matches, min(3, len(vins_matches)))
        for vin in vins_selectionnes:
            cursor.execute("""
                INSERT INTO accords_met_vin (plat_id, vin_id, created_at, status)
                VALUES (?, ?, ?, ?)
            """, (plat["id"], vin[0], datetime.now().isoformat(), "actif"))

conn.commit()
conn.close()
print("Tables plats, vins et accords_met_vin créées et remplies avec succès !")
