import pandas as pd


# Lecture du CSV brut
df = pd.read_csv("./csv/plats_a_la_carte_transforme.csv", sep=";")

# Transformation et nettoyage
df_clean = pd.DataFrame()
df_clean["nom_plat"] = df["plat"].str.strip().str.lower()

# Détermination du type de plat
df_clean["type_plat"] = df.apply(
    lambda x: "vegetarien" if str(x["vegetarien"]).lower() == "oui"
    else "poisson" if str(x["poisson"]).lower() == "oui"
    else "viande" if str(x["viande"]).lower() == "oui"
    else "plat principal",
    axis=1
)

# Autres colonnes utiles
df_clean["accompagnement"] = df["accompagnements"].fillna("").str.strip()
df_clean["criteres"] = df["critere"].fillna("").str.strip().str.replace(";", ", ")
df_clean["created_at"] = df.get("created_at", "")
df_clean["status"] = df.get("status", "actif")

# Conversion en dictionnaire
plats_list = df_clean.to_dict(orient="records")

# Export en JSON
#with open("plats_clean.json", "w", encoding="utf-8") as f:
    #json.dump(plats_list, f, indent=4, ensure_ascii=False)

df_clean.to_csv("plats_clean.csv", index=False) 
print("Fichier plats_clean.csv créé avec succès !")

print(f"Fichier CSV créé avec succès : {len(plats_list)} plats exportés → plats_clean.csv")
