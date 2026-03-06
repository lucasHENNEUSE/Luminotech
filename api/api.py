from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from datetime import datetime
from capteur import mon_frigo
from pydantic import BaseModel
from typing import List
import sqlite3

# Importation de l'agent IA depuis ton nouveau fichier
from Agent_IA.agent_ia import bacchus_agent

# Importations de ton module d'authentification
from api.auth import (
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    get_password_hash,
)

# ------------------------------
# CONFIG
# ------------------------------

app = FastAPI(title="API Accords Mets & Vins")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# BDD
# ------------------------------
def get_db_connection():
    conn = sqlite3.connect("./accords.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------------
# UTILISATEUR (FAKE)
# ------------------------------
fake_user = {
    "username": "lucas",
    "password": get_password_hash("oceluc")
}

# ------------------------------
# AUTH
# ------------------------------

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"]:
        raise HTTPException(status_code=400, detail="Utilisateur inconnu")

    if not verify_password(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


def require_token(token: str = Depends(oauth2_scheme)):
    """Wrapper pour valider un token avant d'accéder aux routes."""
    verify_token(token)
    return token

# ================================================================
# NOUVELLE ROUTE : SOMMELIER IA (BACCHUS)
# ================================================================

# Avant : @app.post("/sommelier/chat", tags=["IA"])
# Avant : async def chat_with_bacchus(message: str, token: str = Depends(require_token)):

# APRÈS (Version libre sans compte) :
@app.post("/sommelier/chat", tags=["IA"])
async def chat_with_bacchus(message: str):
    """
    Route libre : Plus besoin de token pour tester l'IA.
    """
    try:
        config = {"configurable": {"thread_id": "session_test_libre"}}
        result = bacchus_agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config=config
        )
        return {"response": result["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ================================================================
# ROUTES : VINS
# ================================================================

@app.get("/vins", tags=["vins"])
def get_all_vins(token: str = Depends(require_token)):
    conn = get_db_connection()
    vins = conn.execute("SELECT * FROM vins").fetchall()
    conn.close()
    return [dict(v) for v in vins]


@app.get("/vins/{nom}", tags=["vins"])
def get_vin_by_name(nom: str, token: str = Depends(require_token)):
    conn = get_db_connection()
    vin = conn.execute(
        "SELECT * FROM vins WHERE nom_vin LIKE ?", (f"%{nom}%",)
    ).fetchone()
    conn.close()

    if vin is None:
        raise HTTPException(404, "Vin non trouvé")

    return dict(vin)


@app.put("/vins", tags=["vins"])
def add_vin(nom_vin: str, description: str, source: str, criteres: str,
            token: str = Depends(require_token)):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO vins (nom_vin, description, source, criteres) VALUES (?, ?, ?, ?)",
        (nom_vin, description, source, criteres)
    )
    conn.commit()
    conn.close()

    return {"message": "Vin ajouté avec succès"}


@app.delete("/vins/{id}", tags=["vins"])
def delete_vin(id: int, token: str = Depends(require_token)):
    conn = get_db_connection()
    conn.execute("DELETE FROM vins WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"message": f"Vin ID {id} supprimé"}


# ================================================================
# ROUTES : PLATS
# ================================================================

@app.get("/plats", tags=["plats"])
def get_all_plats(token: str = Depends(require_token)):
    conn = get_db_connection()
    plats = conn.execute("SELECT * FROM plats").fetchall()
    conn.close()
    return [dict(p) for p in plats]


@app.get("/plats/{nom}", tags=["plats"])
def get_plat_by_name(nom: str, token: str = Depends(require_token)):
    conn = get_db_connection()
    plat = conn.execute(
        "SELECT * FROM plats WHERE nom_plat LIKE ?", (f"%{nom}%",)
    ).fetchone()
    conn.close()

    if plat is None:
        raise HTTPException(404, "Plat non trouvé")

    return dict(plat)


@app.put("/plats", tags=["plats"])
def add_plat(nom_plat: str, type_plat: str, criteres: str,
             created_at: str, status: str,
             token: str = Depends(require_token)):

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO plats (nom_plat, type_plat, criteres, created_at, status) VALUES (?, ?, ?, ?, ?)",
        (nom_plat, type_plat, criteres, created_at, status)
    )
    conn.commit()
    conn.close()

    return {"message": "Plat ajouté avec succès"}


@app.delete("/plats/{id}", tags=["plats"])
def delete_plat(id: int, token: str = Depends(require_token)):
    conn = get_db_connection()
    conn.execute("DELETE FROM plats WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"message": f"Plat ID {id} supprimé"}

# ================================================================
# ROUTE : MENU DÉGUSTATION
# ================================================================

@app.get("/menu", tags=["menu"])
def generer_menu(
    saison: str,
    meteo: str,
    repas: str,
    token: str = Depends(require_token)
):
    conn = get_db_connection()
    criteres = f"{saison};{meteo};{repas}"

    def get_plat(type_plat):
        return conn.execute("""
            SELECT * FROM plats
            WHERE type_plat = ?
            AND criteres LIKE ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (type_plat, f"%{criteres}%")).fetchone()

    entree = get_plat("entrée")
    plat = get_plat("plat")
    fromage = get_plat("fromage")

    if not plat:
        conn.close()
        raise HTTPException(404, "Aucun plat correspondant")

    vin = conn.execute("""
        SELECT vins.*
        FROM accords_met_vin
        JOIN vins ON accords_met_vin.vin_id = vins.id
        WHERE accords_met_vin.plat_id = ?
        ORDER BY RANDOM()
        LIMIT 1
    """, (plat["id"],)).fetchone()

    conn.close()

    return {
        "entree": entree["nom_plat"] if entree else None,
        "plat": plat["nom_plat"],
        "fromage": fromage["nom_plat"] if fromage else None,
        "vin": vin["nom_vin"] if vin else "Suggestion libre"
    }


# ================================================================
# ROUTES : ACCORDS METS-VINS
# ================================================================

@app.get("/accords/par_plat/{plat}", tags=["accords"])
def get_accords_par_plat(plat: str, token: str = Depends(require_token)):
    conn = get_db_connection()

    row = conn.execute(
        "SELECT id FROM plats WHERE nom_plat LIKE ?", (f"%{plat}%",)
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(404, "Plat non trouvé")

    accords = conn.execute("""
        SELECT vins.nom_vin, vins.criteres
        FROM accords_met_vin
        JOIN vins ON accords_met_vin.vin_id = vins.id
        WHERE accords_met_vin.plat_id = ?
    """, (row["id"],)).fetchall()

    conn.close()
    return [dict(a) for a in accords]


@app.get("/accords/par_vin/{vin}", tags=["accords"])
def get_accords_par_vin(vin: str, token: str = Depends(require_token)):
    conn = get_db_connection()

    row = conn.execute(
        "SELECT id FROM vins WHERE nom_vin LIKE ?", (f"%{vin}%",)
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(404, "Vin non trouvé")

    accords = conn.execute("""
        SELECT plats.nom_plat, plats.criteres
        FROM accords_met_vin
        JOIN plats ON accords_met_vin.plat_id = plats.id
        WHERE accords_met_vin.vin_id = ?
    """, (row["id"],)).fetchall()

    conn.close()
    return [dict(a) for a in accords]


@app.put("/accords", tags=["accords"])
def add_accord(plat_id: int, vin_id: int, created_at: str, status: str,
                token: str = Depends(require_token)):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO accords_met_vin (plat_id, vin_id, created_at, status) VALUES (?, ?, ?, ?)",
        (plat_id, vin_id, created_at, status),
    )
    conn.commit()
    conn.close()

    return {"message": "Accord ajouté"}


@app.delete("/accords/{id}", tags=["accords"])
def delete_accord(id: int, token: str = Depends(require_token)):
    conn = get_db_connection()
    conn.execute("DELETE FROM accords_met_vin WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"message": f"Accord ID {id} supprimé"}

# Modèle pour la sélection d'ingrédients
class SelectionIngredients(BaseModel):
    ingredients: List[str]

@app.get("/frigo", tags=["Frigo"])
def obtenir_inventaire():
    """Retourne l'état actuel du frigo pour le front-end."""
    inventaire = []
    for item in mon_frigo.contenu:
        if not item.consomme:
            jours_restants = (item.alerte_dlc - datetime.now()).days
            inventaire.append({
                "nom": item.nom,
                "date_ajout": item.date_ajout.strftime("%d/%m/%Y"),
                "jours_restants": jours_restants,
                "urgent": jours_restants <= 1
            })
    return inventaire

@app.post("/frigo/ajouter/{nom}", tags=["Frigo"])
def ajouter_aliment_frigo(nom: str):
    """Permet d'ajouter un aliment via l'interface web."""
    mon_frigo.ajouter_aliment(nom)
    return {"message": f"{nom} ajouté au frigo"}

@app.post("/sommelier/recette", tags=["IA"])
async def recette_personnalisee(selection: SelectionIngredients):
    """
    Bacchus propose une recette basée UNIQUEMENT sur les ingrédients cochés en HTML.
    """
    try:
        ingredients_str = ", ".join(selection.ingredients)
        prompt = f"Propose-moi une recette précise utilisant ces ingrédients : {ingredients_str}. Accompagne cela d'un conseil de sommelier."
        
        config = {"configurable": {"thread_id": "session_web_frigo"}}
        result = bacchus_agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config=config
        )
        return {"response": result["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))