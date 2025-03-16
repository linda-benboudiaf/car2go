from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_current_user
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.booking import Booking
from schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from database import get_db
from datetime import datetime
from typing import List

router = APIRouter(prefix="/bookings", tags=["Réservations"])

# Créer une réservation
@router.post("/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Non autorisé")
    new_booking = Booking(**booking.dict(), status="confirmée", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    return new_booking

# Récupérer toutes les réservations
@router.get("/", response_model=List[BookingResponse])
async def get_all_bookings(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Non autorisé")
    result = await db.execute(select(Booking))
    bookings = result.scalars().all()
    return bookings

# Récupérer une réservation par ID
@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Non autorisé")
    result = await db.execute(select(Booking).filter(Booking.id == booking_id))
    booking = result.scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return booking

# Mettre à jour une réservation
@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(booking_id: int, booking_update: BookingUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Non autorisé")
    result = await db.execute(select(Booking).filter(Booking.id == booking_id))
    booking = result.scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    if isinstance(current_user, dict):
        current_user = User(**current_user)

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    for key, value in booking_update.dict(exclude_unset=True).items():
        setattr(booking, key, value)

    booking.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(booking)
    return booking

# Supprimer une réservation
@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Non autorisé")
    result = await db.execute(select(Booking).filter(Booking.id == booking_id))
    booking = result.scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")

    if isinstance(current_user, dict):
        current_user = User(**current_user)

    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    await db.delete(booking)
    await db.commit()
    return {"message": "Réservation supprimée avec succès"}