from pydantic import BaseModel

class Vin(BaseModel):
    nom: str
    description: str
    source: str
    millésime: int = None
