from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserCreate)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    if user.role not in ["apprenti", "accompagnateur"]:
        raise HTTPException(status_code=400, detail="Le rôle doit être 'apprenti' ou 'accompagnateur'.")

    if user.role == "accompagnateur" and not user.numero_permis:
        raise HTTPException(status_code=400, detail="Un accompagnateur doit avoir un numéro de permis.")

    if user.role == "apprenti" and not user.numero_livret:
        raise HTTPException(status_code=400, detail="Un apprenti doit avoir un numéro de livret.")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        password=hashed_password,
        telephone=user.telephone,
        adresse=user.adresse,
        date_naissance=user.date_naissance,
        role=user.role,
        license_date=user.license_date,
        numero_permis=user.numero_permis if user.role == "accompagnateur" else None,
        numero_livret=user.numero_livret if user.role == "apprenti" else None,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).filter(User.id == user_id))
    existing_user = result.scalar()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    for key, value in user.model_dump().items():
        if value is not None:
            setattr(existing_user, key, value)

    await db.commit()
    return existing_user

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    await db.delete(user)
    await db.commit()
    return {"message": "Utilisateur supprimé"}