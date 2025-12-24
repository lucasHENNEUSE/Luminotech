import csv
import sqlite3
from datetime import datetime
import random

# Fichiers CSV
csv_file_plats = "./sql/plats_clean.csv"
csv_file_vins = "./sql/vins_fusionnes.csv"

# Connexion SQLite
conn = sqlite3.connect("accords.db")
cursor = conn.cursor()

# création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS suggestons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plat TEXT,
    vin TEXT,
    criteres TEXT,
    created_at TEXT
);
""")

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

# Importer les vins depuis le fichier (vins_fusionnes.csv)
vins = []
cursor.execute("DELETE FROM vins")  # nettoyage avant import
conn.commit()

with open(csv_file_vins, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nom_vin = str(row.get("nom") or row.get("nom_vin") or "").strip()
        description = str(row.get("description", "")).strip()
        source = str(row.get("source", "")).strip()
        criteres = str(row.get("criteres", "")).strip().lower()

        if nom_vin:  
            cursor.execute("""
                INSERT INTO vins (nom_vin, description, source, criteres)
                VALUES (?, ?, ?, ?)
            """, (nom_vin, description, source, criteres))

            vins.append({
                "id": cursor.lastrowid,
                "criteres": criteres
            })
        else:
            print(f"[Ligne ignorée] Pas de nom_vin détecté : {row}")

conn.commit()

# Importer les plats depuis le fichier (plats_clean.csv)
plats = []
cursor.execute("DELETE FROM plats")  # nettoyage avant import
conn.commit()

with open(csv_file_plats, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nom_plat = str(row.get("nom_plat", "")).strip()
        type_plat = str(row.get("type_plat", "")).strip()
        criteres = str(row.get("criteres", "")).lower().strip()

        cursor.execute("""
            INSERT INTO plats (nom_plat, type_plat, criteres, created_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, (nom_plat, type_plat, criteres, datetime.now().isoformat(), "actif"))

        plats.append({"id": cursor.lastrowid, "criteres": criteres})

conn.commit()

#Création automatique des accords mets/vins
cursor.execute("DELETE FROM accords_met_vin")
conn.commit()

for plat in plats:
    vins_matches = list(cursor.execute("SELECT id FROM vins WHERE criteres=?", (plat["criteres"],)))
    if vins_matches:
        vins_selectionnes = random.sample(vins_matches, min(3, len(vins_matches)))
        for vin in vins_selectionnes:
            cursor.execute("""
                INSERT INTO accords_met_vin (plat_id, vin_id, created_at, status)
                VALUES (?, ?, ?, ?)
            """, (plat["id"], vin[0], datetime.now().isoformat(), "actif"))

conn.commit()

# Résumé final
count_vins = cursor.execute("SELECT COUNT(*) FROM vins").fetchone()[0]
count_plats = cursor.execute("SELECT COUNT(*) FROM plats").fetchone()[0]
count_accords = cursor.execute("SELECT COUNT(*) FROM accords_met_vin").fetchone()[0]
count_suggestions = cursor.execute("SELECT COUNT(*) FROM suggestons").fetchone()[0]

print("\nImport terminé avec succès !")
print(f"→ {count_vins} vins insérés dans la table 'vins'")
print(f"→ {count_plats} plats insérés dans la table 'plats'")
print(f"→ {count_accords} accords générés automatiquement\n")
print(f"→ {count_suggestions} suggestions enregistrées dans la table 'suggestions'")

# Aperçu des 5 premiers vins
print("Exemple de vins insérés :")
for vin in cursor.execute("SELECT nom_vin, criteres FROM vins LIMIT 5"):
    print(f" - {vin[0]} ({vin[1]})")


# Requête SQL pour afficher les accords plats/vins
print("\n=== Liste des accords plats/vins générés ===\n")

query = """
SELECT 
    plats.nom_plat AS Plat,
    vins.nom_vin AS Vin,
    vins.criteres AS Critere_commun
FROM accords_met_vin amv
JOIN plats  ON amv.plat_id = plats.id
JOIN vins   ON amv.vin_id = vins.id
WHERE plats.criteres = vins.criteres
ORDER BY plats.nom_plat;
"""

cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(f"Plat : {row[0]} | Vin : {row[1]} | Critère : {row[2]}")

conn.close()
