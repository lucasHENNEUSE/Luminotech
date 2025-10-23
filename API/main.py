from fastapi import FastAPI
from API.routes import vins

app = FastAPI(title="API Vins - Luminotech")

app.include_router(vins.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Luminotech Vins!"}
