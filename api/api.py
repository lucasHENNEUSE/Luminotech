from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
from api.auth import (
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    get_password_hash,
)

# Utilisateur de test
fake_user = {
    "username": "lucas",
    "password": get_password_hash("oceluc")  # mot de passe = oceluc
}

# Création de l'app FastAPI
app = FastAPI(title="API Accords Mets & Vins")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines (à restreindre plus tard si besoin)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Connexion SQLite
def get_db_connection():
    conn = sqlite3.connect("./sql/accords.db")
    conn.row_factory = sqlite3.Row
    return conn


# AUTHENTIFICATION
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"]:
        raise HTTPException(status_code=400, detail="Utilisateur inconnu")
    if not verify_password(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# ROUTES POUR LES VINS
@app.get("/vins")
def get_all_vins(token: str = Depends(verify_token)):
    conn = get_db_connection()
    vins = conn.execute("SELECT * FROM vins").fetchall()
    conn.close()
    return [dict(v) for v in vins]


@app.get("/vins/{nom}")
def get_vin_by_name(nom: str, token: str = Depends(verify_token)):
    conn = get_db_connection()
    vin = conn.execute("SELECT * FROM vins WHERE nom_vin LIKE ?", (f"%{nom}%",)).fetchone()
    conn.close()
    if vin is None:
        raise HTTPException(status_code=404, detail="Vin non trouvé")
    return dict(vin)


# ROUTES POUR LES PLATS
@app.get("/plats")
def get_all_plats(token: str = Depends(verify_token)):
    conn = get_db_connection()
    plats = conn.execute("SELECT * FROM plats").fetchall()
    conn.close()
    return [dict(p) for p in plats]


@app.get("/plats/{nom}")
def get_plat_by_name(nom: str, token: str = Depends(verify_token)):
    conn = get_db_connection()
    plat = conn.execute("SELECT * FROM plats WHERE nom_plat LIKE ?", (f"%{nom}%",)).fetchone()
    conn.close()
    if plat is None:
        raise HTTPException(status_code=404, detail="Plat non trouvé")
    return dict(plat)


# ACCORDS METS & VINS
@app.get("/accords/par_plat/{plat}")
def get_accords_par_plat(plat: str, token: str = Depends(verify_token)):
    conn = get_db_connection()
    plat_data = conn.execute("SELECT id FROM plats WHERE nom_plat LIKE ?", (f"%{plat}%",)).fetchone()
    if not plat_data:
        conn.close()
        raise HTTPException(status_code=404, detail="Plat non trouvé")

    accords = conn.execute("""
        SELECT vins.nom_vin, vins.criteres
        FROM accords_met_vin
        JOIN vins ON accords_met_vin.vin_id = vins.id
        WHERE accords_met_vin.plat_id = ?
    """, (plat_data["id"],)).fetchall()
    conn.close()
    return [dict(a) for a in accords]


@app.get("/accords/par_vin/{vin}")
def get_accords_par_vin(vin: str, token: str = Depends(verify_token)):
    conn = get_db_connection()
    vin_data = conn.execute("SELECT id FROM vins WHERE nom_vin LIKE ?", (f"%{vin}%",)).fetchone()
    if not vin_data:
        conn.close()
        raise HTTPException(status_code=404, detail="Vin non trouvé")

    accords = conn.execute("""
        SELECT plats.nom_plat, plats.criteres
        FROM accords_met_vin
        JOIN plats ON accords_met_vin.plat_id = plats.id
        WHERE accords_met_vin.vin_id = ?
    """, (vin_data["id"],)).fetchall()
    conn.close()
    return [dict(a) for a in accords]

#uvicorn api.api:app --reload
