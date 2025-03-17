from fastapi import APIRouter, Depends, HTTPException
from routes.auth import get_current_user
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.booking import Booking
from models.car import Car
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

# Récupérer les réservations par user_id
@router.get("/user")
async def get_bookings_by_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Non autorisé")

    # Vérifier si current_user est un dict et le convertir en User
    if isinstance(current_user, dict):
        current_user = User(**current_user)

    # Jointure entre Booking et Car pour obtenir plus d'infos
    result = await db.execute(
        select(Booking, Car)
        .join(Car, Booking.car_id == Car.id)
        .filter(Booking.user_id == current_user.id)
    )

    bookings = result.all()

    print(bookings)

    # Transformation des résultats en un format plus complet
    bookings_list = [
        {
            "id": booking.Booking.id,
            "user_id": booking.Booking.user_id,
            "car_id": booking.Booking.car_id,
            "start_time": booking.Booking.start_time,
            "end_time": booking.Booking.end_time,
            "purpose": booking.Booking.purpose,
            "status": booking.Booking.status,
            "created_at": booking.Booking.created_at,
            "updated_at": booking.Booking.updated_at,
            "car": {  # Ajout des infos de la voiture
                "id": booking.Car.id,
                "nom": booking.Car.nom,
                "modele": booking.Car.modele,
                "annee_fab": booking.Car.annee_fab,
                "type": booking.Car.type,
                "plaque": booking.Car.plaque,
                "controle_technique": booking.Car.controle_technique,
                "prix_par_heure": booking.Car.prix_par_heure,
                "disponible": booking.Car.disponible,
                "image_url": booking.Car.image_url,
            }
        }
        for booking in bookings
    ]


    return bookings_list

# Récupérer une réservation par ID
@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if isinstance(current_user, dict):
        current_user = User(**current_user)

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