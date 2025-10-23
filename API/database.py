from pymongo import MongoClient

# Connexion Mongo locale
client = MongoClient("mongodb://localhost:27018/")

# Sélection de la base et de la collection
db = client["projet_e1"]
collection_vins = db["vins_vinsdefrance"]
