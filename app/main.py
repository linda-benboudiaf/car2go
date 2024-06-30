from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .models import engine, SessionLocal
from .config import STRIPE_API_KEY
from fastapi.middleware.cors import CORSMiddleware
import stripe

stripe.api_key = STRIPE_API_KEY

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Car2Go API",
    description="API for Car2Go car rental service",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "https://www.yourwebsite.com",
        "email": "your.email@domain.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db=db, car=car)


@app.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, skip=skip, limit=limit)
    return cars


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db=db, reservation=reservation)


@app.get("/reservations/{car_id}", response_model=List[schemas.Reservation])
def read_reservations(car_id: int, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, car_id=car_id)
    return reservations

@app.post("/create-payment-intent/")
async def create_payment_intent(request: Request):
    data = await request.json()
    try:
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency='eur',
            metadata={'integration_check': 'accept_a_payment'},
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))