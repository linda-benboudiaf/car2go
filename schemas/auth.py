from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    nom: constr(max_length=100)
    prenom: constr(max_length=100)
    email: EmailStr
    telephone: constr(max_length=15)
    adresse: constr(max_length=255)
    date_naissance: date
    role: constr(max_length=20)
    license_date: Optional[date] = None
    numero_permis: Optional[constr(max_length=20)] = None
    numero_livret: Optional[constr(max_length=20)] = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"