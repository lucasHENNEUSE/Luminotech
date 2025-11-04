Luminotech — Accords Mets & Vins
Présentation du projet

Luminotech est un projet de développement d’API autour des accords mets & vins.
Il vise à créer une chaîne complète de traitement de données (ETL) et une API REST sécurisée permettant de consulter et enrichir des données issues de plusieurs sources hétérogènes.

Ce projet illustre la mise en œuvre d’un pipeline complet, depuis la collecte multi-source jusqu’à la mise à disposition via une API FastAPI.

Objectifs

Construire un pipeline complet à partir de plusieurs sources : CSV, MongoDB, SQL, scraping web et API publique.

Fusionner et normaliser les données issues de différentes origines pour les consolider dans une base SQLite.

Créer une API REST avec FastAPI et sécuriser l’accès via JWT.

Permettre la recherche et la consultation d’accords entre les plats et les vins.

Architecture du projet
LUMINOTECH/
│
├── api/
│   ├── api.py                     # Routes FastAPI
│   ├── auth.py                    # Authentification JWT
│   └── import_wines_from_api.py   # Import des vins depuis API publique
│
├── csv/
│   ├── ETL.py                     # Nettoyage et transformation des plats
│   ├── plats_a_la_carte.csv       # Fichier brut des plats
│   └── plats_a_la_carte_transforme.csv
│
├── scrap_big_data/
│   ├── criteres.csv               # Critères d’association (viande, poisson, etc.)
│   └── mongoweb.py                # Extraction et structuration des données en ligne
│
├── sql/
│   ├── vins_fusionnes.csv         # Fusion Mongo + scraping ( agrégation )
│   ├── plats_clean.csv            # Données plats nettoyées
│   ├── accords.db                 # Base SQLite finale
│   └── script.py                  # Script d’intégration complète
│
├── docker-compose.yml
├── requirements.txt
└── README.md

Étapes du pipeline
Extraction et transformation des plats (CSV)
python csv/ETL.py


Nettoie les données brutes, supprime les accents, uniformise les libellés, ajoute des métadonnées et produit un fichier propre :
plats_a_la_carte_transforme.csv

Récupération des vins depuis une source en ligne
python scrap_big_data/mongoweb.py


Les données relatives aux vins ont été récupérées à partir d’une source publique en ligne et  d'une base MongoDB (Docker).

Fusion et normalisation des données

Les données MongoDB étant limitées, un ETL de fusion a permis de combiner les données MongoDB et les données issues du web pour produire un fichier unique :
vins_fusionnes.csv

Cette étape supprime les doublons et harmonise les colonnes (nom, description, source, criteres).

Création et remplissage de la base SQLite
python sql/script.py

Ce script :

Crée les tables plats, vins et accords_met_vin

Importe les plats et vins depuis les CSV nettoyés

Génère automatiquement les accords mets & vins selon les critères communs

Produit la base accords.db

Enrichissement via API publique
python api/import_wines_from_api.py


Importe les données depuis https://api.sampleapis.com/wines

augmentant le nombre de références disponibles dans la base SQLite.

Lancer l’API FastAPI
uvicorn api.api:app --reload


Ouvrir ensuite dans le navigateur :
http://127.0.0.1:8000/docs

Authentification et sécurité

L’accès aux routes est sécurisé par un système de JSON Web Tokens (JWT).
Il faut d’abord obtenir un token via /token, puis l’utiliser dans les en-têtes de requêtes.

Endpoints principaux
Méthode	Endpoint	Description
POST	/token	Authentifie l’utilisateur et renvoie un JWT
GET	/vins	Liste tous les vins
GET	/vins/{nom}	Recherche un vin spécifique
GET	/plats	Liste tous les plats
GET	/plats/{nom}	Recherche un plat spécifique
GET	/accords/par_plat/{plat}	Trouve les vins associés à un plat
GET	/accords/par_vin/{vin}	Trouve les plats associés à un vin

Technologies utilisées
Catégorie	Outils
Langage	Python 3
Framework API	FastAPI
Bases de données	SQLite + MongoDB
Traitement & nettoyage	Pandas
Collecte de données	BeautifulSoup (source publique en ligne)
Authentification	JWT (JSON Web Tokens)
Serveur local	Uvicorn
Environnement	Docker (MongoDB)



Respect du RGPD

Le projet ne manipule actuellement aucune donnée personnelle.
Cependant, dans une version future (application mobile ou web), certaines informations utilisateur pourraient être collectées (nom, prénom, e-mail).
Dans ce cas, le projet sera conforme au Règlement Général sur la Protection des Données (RGPD) : consentement, droit d’accès, suppression et sécurisation des données.

Auteur

Lucas HENNEUSE
Promotion Développeur IA – Simplon 2025
GitHub : lucasHENNEUSE