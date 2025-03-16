from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.auth import UserRegister, TokenResponse, UserLogin
from utils.auth import create_access_token, verify_token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=TokenResponse)
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):

    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validation en fonction du rôle
    if user.role == "apprenti" and not user.numero_livret:
        raise HTTPException(status_code=400, detail="Un apprenti doit avoir un numéro de livret.")
    if user.role == "accompagnateur":
        if not user.numero_permis:
            raise HTTPException(status_code=400, detail="Un accompagnateur doit avoir un numéro de permis.")
        if not user.license_date:
            raise HTTPException(status_code=400, detail="Un accompagnateur doit avoir une date d'obtention de permis.")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        telephone=user.telephone,
        adresse=user.adresse,
        date_naissance=user.date_naissance,
        role=user.role,
        license_date=user.license_date,
        numero_permis=user.numero_permis if user.role == "accompagnateur" else None,
        numero_livret=user.numero_livret if user.role == "apprenti" else None,
        hashed_password=hashed_password
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(form_data.password, user.hash_password(form_data.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email = payload.get("sub")
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"id": user.id, "nom": user.nom, "prenom": user.prenom, "email": user.email}