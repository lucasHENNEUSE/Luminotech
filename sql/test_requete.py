import sqlite3

# Connexion à la base SQLite
conn = sqlite3.connect("accords.db")
cursor = conn.cursor()

# Requête SQL pour afficher les accords plats/vins
query = """
SELECT 
    plats.nom_plat AS Plat,
    vins.nom_vin AS Vin,
    vins.criteres AS Critere_commun
FROM accords_met_vin amv
JOIN plats  ON amv.plat_id = plats.id
JOIN vins  ON amv.vin_id = vins.id
WHERE plats.criteres = vins.criteres
ORDER BY plats.nom_plat;
"""

# Exécution et affichage des résultats
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(f"Plat : {row[0]} | Vin : {row[1]} | Critère : {row[2]}")

conn.close()
