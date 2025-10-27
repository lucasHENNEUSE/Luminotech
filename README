#Luminotech — Accords Mets & Vins

#Présentation du projet

Luminotech est un projet de data engineering et de développement d’API autour des accords mets et vins.

Il vise à construire une chaîne complète ETL + API REST sécurisée, intégrant plusieurs sources de données :  
- Fichiers plats (CSV),
- API publique,
- Scraping web,
- Base de données Big Data (MongoDB),
- Consolidation finale dans une base SQLite.

L’API FastAPI expose ensuite ces données nettoyées et harmonisées pour permettre la recherche et la recommandation d’accords.

#Objectifs

- Construire un pipeline complet à partir de 5 sources.  
- Nettoyer, enrichir et centraliser les données dans SQLite.  
- Créer une API REST FastAPI avec authentification sécurisée JWT.  
- Permettre la consultation simple des accords vins-plats.

#Architecture du projet

LUMINOTECH/

.venv/                        
 api/
     __init__.py
    api.py                    
    auth.py                   
    import_wines_from_api.py  

 csv/
    ETL.py                    
    plats_a_la_carte.csv
    plats_a_la_carte_transforme.csv

 scrap_big_data/
    criteres.csv
    mongoweb.py               

 sql/
    accords.db               
    plats_clean.csv
    plats_clean.json
    script.py  

 docker-compose.yml             
 requirements.txt               
.gitignore

# Préparation des données:

    1. Extraction et transformation des plats (CSV)

python csv/ETL.py

Nettoie et enrichit les plats pour générer plats_a_la_carte_transforme.csv.

    2.Scraping des vins depuis Vins de Francep

python scrap_big_data/mongoweb.py

Scrape le site vinsdefrance-roanne.fr, insère les données dans MongoDB (via Docker) et ajoute les critères d’accords.

    3.Création et remplissage de la base SQLite

python sql/script.py

Crée les tables (vins, plats, accords_met_vin) et génère les liens d’accords entre plats et vins.

    4.Import des vins via API publique

python api/import_wines_from_api.py

Récupère les vins depuis https://api.sampleapis.com/wines et les insère dans accords.db.

# Lancer l’API FastAPI

uvicorn api.api:app --reload

ouverture dans le navigateur :
http://127.0.0.1:8000/docs

# Authentification JWT

L’API est sécurisée par JSON Web Tokens (JWT).

# Endpoints principaux

| Méthode  | Endpoint                      | Description                        |
| -------- | ----------------------------- | ---------------------------------- |
| **POST** | `/token`                      | Authentifie et renvoie un JWT      |
| **GET**  | `/vins`                       | Liste tous les vins                |
| **GET**  | `/vins/{nom}`                 | Recherche d’un vin                 |
| **GET**  | `/plats`                      | Liste tous les plats               |
| **GET**  | `/plats/{nom}`                | Recherche d’un plat                |
| **GET**  | `/accord_v_p/par_plat/{plat}` | Trouve les vins associés à un plat |
| **GET**  | `/accord_v_p/par_vin/{vin}`   | Trouve les plats associés à un vin |

# Technologies utilisées
Catégorie	Outils
Langage	Python3
Framework API	FastAPI
Base de données	SQLite + MongoDB
Scraping	BeautifulSoup
ETL / Data Cleaning	Pandas
Sécurité / Authentification	JWT
Serveur	Uvicorn
Virtualisation	Docker

# Auteur

Lucas HENNEUSE

