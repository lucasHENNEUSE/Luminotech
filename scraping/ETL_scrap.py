import pandas as pd
from pymongo import MongoClient

# === CONFIGURATION ===
CSV_SOURCE = "./scraping/vins_scrapes.csv"          # fichier CSV issu du scraping
OUTPUT_CSV = "./vins_fusionnes.csv"        # fichier final propre sans doublons
MONGO_URI = "mongodb://localhost:27018/"
DB_NAME = "projet_e1"
COLLECTION_NAME = "vins_vinsdefrance"


############### extraction #################
print("Lecture du fichier CSV...")
df_csv = pd.read_csv(CSV_SOURCE)

print(f"→ {len(df_csv)} lignes chargées depuis {CSV_SOURCE}")

print("\nConnexion à MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Récupération des données Mongo dans un DataFrame
data_mongo = list(collection.find({}, {"_id": 0}))  # on exclut le champ _id
df_mongo = pd.DataFrame(data_mongo)
print(f"→ {len(df_mongo)} documents récupérés depuis MongoDB")


################ transformation #################
print("\nNormalisation des données...")

# Harmonisation des noms de colonnes
df_csv.columns = df_csv.columns.str.strip().str.lower()
df_mongo.columns = df_mongo.columns.str.strip().str.lower()

# Vérifie que les colonnes essentielles sont présentes
required_cols = ["nom", "description", "source", "criteres"]
for col in required_cols:
    if col not in df_csv.columns:
        df_csv[col] = ""
    if col not in df_mongo.columns:
        df_mongo[col] = ""

# Nettoyage des chaînes (minuscules, suppression espaces)
for df in [df_csv, df_mongo]:
    df["nom"] = df["nom"].astype(str).str.strip().str.lower()
    df["description"] = df["description"].astype(str).str.strip()
    df["criteres"] = df["criteres"].astype(str).str.strip().str.lower()
    df["source"] = df["source"].astype(str).str.strip()


# Fusion et suppression des doublons 
print("\nFusion des deux sources...")
df_fusion = pd.concat([df_csv, df_mongo], ignore_index=True)

# Suppression des doublons selon le nom du vin
df_fusion = df_fusion.drop_duplicates(subset=["nom"], keep="first")

print(f"→ Après nettoyage : {len(df_fusion)} vins uniques trouvés.")


################ enregistrement ##############
df_fusion.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"\nFichier final créé : {OUTPUT_CSV}")
print(f"   Total : {len(df_fusion)} lignes sauvegardées sans doublons.")
