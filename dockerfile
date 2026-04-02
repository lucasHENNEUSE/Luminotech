# Image de base Python
FROM python:3.12-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie et installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de tout le code
COPY . .

# Port exposé par FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]