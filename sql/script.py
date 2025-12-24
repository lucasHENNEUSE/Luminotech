import csv
import sqlite3
from datetime import datetime, UTC
import random
import os

# Fichiers CSV (Vérifiez que ces chemins sont corrects par rapport à la racine)
csv_file_plats = "./sql/plats_clean.csv"
csv_file_vins = "./sql/vins_fusionnes.csv"

# Connexion SQLite
conn = sqlite3.connect("accords.db")
cursor = conn.cursor()

# 1. Création des tables
# Correction de "suggestons" en "suggestions"
cursor.execute("""
CREATE TABLE IF NOT EXISTS suggestions (
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

# CORRECTION ICI : Ajout de la parenthèse fermante );
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    ia_response TEXT,
    created_at TEXT
);
""")

conn.commit()

# 2. Importer les vins depuis le fichier (vins_fusionnes.csv)
vins = []
cursor.execute("DELETE FROM vins")  # nettoyage avant import
conn.commit()

if os.path.exists(csv_file_vins):
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
    print(f"[ERREUR] Fichier introuvable : {csv_file_vins}")

conn.commit()

# 3. Importer les plats depuis le fichier (plats_clean.csv)
plats = []
cursor.execute("DELETE FROM plats")  # nettoyage avant import
conn.commit()

if os.path.exists(csv_file_plats):
    with open(csv_file_plats, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nom_plat = str(row.get("nom_plat", "")).strip()
            type_plat = str(row.get("type_plat", "")).strip()
            criteres = str(row.get("criteres", "")).lower().strip()

            cursor.execute("""
                INSERT INTO plats (nom_plat, type_plat, criteres, created_at, status)
                VALUES (?, ?, ?, ?, ?)
            """, (nom_plat, type_plat, criteres, datetime.now(UTC).isoformat(), "actif"))

            plats.append({"id": cursor.lastrowid, "criteres": criteres})
else:
    print(f"[ERREUR] Fichier introuvable : {csv_file_plats}")

conn.commit()

# 4. Création automatique des accords mets/vins
cursor.execute("DELETE FROM accords_met_vin")
conn.commit()

for plat in plats:
    # On récupère les vins qui ont le même critère
    cursor.execute("SELECT id FROM vins WHERE criteres=?", (plat["criteres"],))
    vins_matches = cursor.fetchall()
    
    if vins_matches:
        vins_selectionnes = random.sample(vins_matches, min(3, len(vins_matches)))
        for vin in vins_selectionnes:
            cursor.execute("""
                INSERT INTO accords_met_vin (plat_id, vin_id, created_at, status)
                VALUES (?, ?, ?, ?)
            """, (plat["id"], vin[0], datetime.now(UTC).isoformat(), "actif"))

conn.commit()

# 5. Résumé final
count_vins = cursor.execute("SELECT COUNT(*) FROM vins").fetchone()[0]
count_plats = cursor.execute("SELECT COUNT(*) FROM plats").fetchone()[0]
count_accords = cursor.execute("SELECT COUNT(*) FROM accords_met_vin").fetchone()[0]
# Utilisation du nom corrigé "suggestions"
count_suggestions = cursor.execute("SELECT COUNT(*) FROM suggestions").fetchone()[0]

print("\n Import terminé avec succès !")
print(f"→ {count_vins} vins insérés dans la table 'vins'")
print(f"→ {count_plats} plats insérés dans la table 'plats'")
print(f"→ {count_accords} accords générés automatiquement")
print(f"→ {count_suggestions} suggestions trouvées dans la table 'suggestions'\n")

# Requête SQL pour afficher les accords plats/vins
print("=== Aperçu des accords générés ===")
query = """
SELECT 
    plats.nom_plat AS Plat,
    vins.nom_vin AS Vin,
    vins.criteres AS Critere_commun
FROM accords_met_vin amv
JOIN plats  ON amv.plat_id = plats.id
JOIN vins   ON amv.vin_id = vins.id
LIMIT 10;
"""

for row in cursor.execute(query):
    print(f"Plat : {row[0]} | Vin : {row[1]} | Critère : {row[2]}")

conn.close()