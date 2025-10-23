import pandas as pd

# Lire ton CSV brut
df = pd.read_csv("./csv/plats_a_la_carte_transforme.csv", sep=";")

# Sélection des colonnes utiles
df_clean = pd.DataFrame()
df_clean["nom_plat"] = df["plat"]
df_clean["type_plat"] = df.apply(lambda x: "dessert" if x["dessert"] == "oui" 
                                 else "poisson" if x["poisson"] == "oui"
                                 else "viande" if x["viande"] == "oui"
                                 else "plat principal", axis=1)
df_clean["accompagnement"] = df["accompagnements"]
df_clean["criteres"] = df["critere"]

# Nettoyage du texte (minuscules, suppression espaces)
df_clean["nom_plat"] = df_clean["nom_plat"].str.strip().str.lower()
df_clean["criteres"] = df_clean["criteres"].str.replace(";", ", ").str.strip()

# Export CSV propre
df_clean.to_csv("plats_clean.csv", index=False)
print("Fichier plats_clean.csv créé avec succès !")
