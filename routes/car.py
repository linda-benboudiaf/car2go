from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.car import Car
from schemas.car import CarCreate, CarResponse, CarUpdate
from datetime import date

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.post("/", response_model=CarResponse)
async def create_car(car: CarCreate, db: AsyncSession = Depends(get_db)):
    new_car = Car(
        nom=car.nom,
        modele=car.modele,
        annee_fab=car.annee_fab,
        type=car.type,
        plaque=car.plaque,
        controle_technique=car.controle_technique,
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)
    return new_car

@router.get("/{car_id}", response_model=CarResponse)
async def get_car(car_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car).filter(Car.id == car_id))
    car = result.scalar()
    if not car:
        raise HTTPException(status_code=404, detail="Voiture non trouvée")
    return car

@router.get("/", response_model=list[CarResponse])
async def get_all_cars(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car))
    cars = result.scalars().all()
    return cars

@router.put("/{car_id}", response_model=CarResponse)
async def update_car(car_id: int, car: CarUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car).filter(Car.id == car_id))
    existing_car = result.scalar()
    if not existing_car:
        raise HTTPException(status_code=404, detail="Voiture non trouvée")

    for key, value in car.model_dump(exclude_unset=True).items():
        setattr(existing_car, key, value)

    existing_car.updated_at = date.today()
    await db.commit()
    await db.refresh(existing_car)
    return existing_car

@router.delete("/{car_id}")
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car).filter(Car.id == car_id))
    car = result.scalar()
    if not car:
        raise HTTPException(status_code=404, detail="Voiture non trouvée")

    await db.delete(car)
    await db.commit()
    return {"message": "Voiture supprimée"}