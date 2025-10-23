from fastapi import APIRouter, HTTPException
from API.database import collection_vins
from API.models import Vin
from bson import ObjectId

router = APIRouter(prefix="/vins", tags=["Vins"])

# GET : récupérer tous les vins
@router.get("/")
def get_all_vins():
    vins = list(collection_vins.find({}, {"_id": 0}))  # on exclut l'ID interne
    return vins

# GET : récupérer un vin par nom
@router.get("/{nom}")
def get_vin_by_name(nom: str):
    vin = collection_vins.find_one({"nom": {"$regex": nom, "$options": "i"}}, {"_id": 0})
    if not vin:
        raise HTTPException(status_code=404, detail="Vin non trouvé")
    return vin

# POST : ajouter un vin
@router.post("/")
def add_vin(vin: Vin):
    collection_vins.insert_one(vin.dict())
    return {"message": "Vin ajouté avec succès"}

# PUT : modifier un vin
@router.put("/{nom}")
def update_vin(nom: str, vin: Vin):
    result = collection_vins.update_one({"nom": {"$regex": nom, "$options": "i"},"millesime":""}, {"$set": vin.dict()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Vin non trouvé ou inchangé")
    return {"message": "Vin mis à jour avec succès"}

# DELETE : supprimer un vin
@router.delete("/{nom}")
def delete_vin(nom: str):
    result = collection_vins.delete_one({"nom": {"$regex": nom, "$options": "i"}})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vin non trouvé")
    return {"message": "Vin supprimé avec succès"}
