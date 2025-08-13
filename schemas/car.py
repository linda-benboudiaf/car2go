from pydantic import BaseModel
from datetime import date
from typing import Optional

class CarBase(BaseModel):
    nom: str
    modele: str
    annee_fab: int
    type: str
    plaque: str
    controle_technique: date

class CarCreate(CarBase):
    pass

class CarUpdate(BaseModel):
    nom: Optional[str] = None
    modele: Optional[str] = None
    # Use the same field name as the database model to ensure updates work correctly
    annee_fab: Optional[int] = None
    type: Optional[str] = None
    plaque: Optional[str] = None
    controle_technique: Optional[date] = None

class CarResponse(CarBase):
    id: int
    nom: str
    modele: str
    annee_fab: int
    type: str
    plaque: str
    controle_technique: date
    prix_par_heure: float
    disponible: bool
    # image_url may be NULL in the database
    image_url: Optional[str] = None
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
