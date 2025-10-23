from fastapi import FastAPI
from API.routes import vins, auth_routes

app = FastAPI(title="API Vins - Luminotech")

app.include_router(vins.router)
app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Luminotech Vins!"}
