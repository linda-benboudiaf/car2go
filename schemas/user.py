from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date

class UserBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    password: str
    telephone: str
    adresse: str
    date_naissance: date
    role: str
    license_date: Optional[date] = None
    numero_permis: Optional[str] = None
    numero_livret: Optional[str] = None

class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None
    date_naissance: Optional[date] = None
    role: Optional[str] = None
    license_date: Optional[date] = None
    numero_permis: Optional[str] = None
    numero_livret: Optional[str] = None
    password: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

