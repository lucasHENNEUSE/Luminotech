import pandas as pd
import sqlite3
from pymongo import MongoClient

# Connexions
client = MongoClient("mongodb://localhost:27018/")
db = client["projet_e1"]
vins_collection = db["vins_vinsdefrance"]

# Lecture du CSV des plats
plats_df = pd.read_csv("./sql/plats_clean.csv")

# Récupération des vins depuis MongoDB
vins = list(vins_collection.find({}, {"_id": 0}))
vins_df = pd.DataFrame(vins)

# Connexion SQLite 
conn = sqlite3.connect("accords_met_vin.db")
cursor = conn.cursor()

#Création des tables SQLite
cursor.execute("""
CREATE TABLE IF NOT EXISTS plats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_plat TEXT,
    type TEXT,
    intensite TEXT,
    aromes TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_vin TEXT,
    description TEXT,
    source TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plat_id INTEGER,
    vin_id INTEGER,
    score REAL,
    FOREIGN KEY (plat_id) REFERENCES plats (id),
    FOREIGN KEY (vin_id) REFERENCES vins (id)
)
""")

conn.commit()

# Remplissage des tables plats et vins 
plats_df.to_sql("plats", conn, if_exists="replace", index=False)
vins_df.to_sql("vins", conn, if_exists="replace", index=False)

#  Fonction pour calculer un score d’accord 
def calculer_score(plat, vin):
    score = 0

    if "rouge" in vin["description"].lower() and plat["type"] in ["viande rouge", "viande blanche"]:
        score += 0.5
    if "blanc" in vin["description"].lower() and plat["type"] in ["poisson", "vegetarien"]:
        score += 0.5
    

    return round(min(score, 1.0), 2)

# Génération des accords mets-vins
for _, plat in plats_df.iterrows():
    for _, vin in vins_df.iterrows():
        score = calculer_score(plat, vin)
        if score > 0.5:  # seuil pour considérer un bon accord
            cursor.execute("""
                INSERT INTO accords (plat_id, vin_id, score)
                VALUES (?, ?, ?)
            """, (plat.name + 1, vin.name + 1, score))

conn.commit()
conn.close()

print(" Accords mets-vins générés et enregistrés dans SQLite !")
