import asyncio
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from models.user import User
from models.car import Car
from routes.auth import get_current_user


@pytest.fixture
def client():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async with async_session() as session:
            user = User(
                nom="Test",
                prenom="User",
                email="test@example.com",
                password="hashed",
                telephone="1234567890",
                adresse="123 Street",
                date_naissance=datetime(1990, 1, 1).date(),
                role="apprenti",
                numero_livret="ABC123",
            )
            car = Car(
                nom="Car",
                modele="Model",
                annee_fab=2020,
                type="classique",
                plaque="ABC123",
                controle_technique=datetime.utcnow().date(),
                prix_par_heure=20.0,
                disponible=True,
                image_url="http://example.com/car.jpg",
            )
            session.add_all([user, car])
            await session.commit()
            await session.refresh(user)
            await session.refresh(car)
            return user, car

    user, car = asyncio.run(init_db())

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    def override_get_current_user():
        return {
            "id": user.id,
            "nom": user.nom,
            "prenom": user.prenom,
            "email": user.email,
            "role": user.role,
        }

    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c, user, car

    app.dependency_overrides.clear()


def test_overlapping_booking_rejected(client):
    c, user, car = client

    start = datetime.utcnow()
    end = start + timedelta(hours=1)

    booking1 = {
        "user_id": user.id,
        "car_id": car.id,
        "start_time": start.isoformat(),
        "end_time": end.isoformat(),
        "purpose": "self",
    }

    response1 = c.post("/bookings/", json=booking1)
    assert response1.status_code == 200

    overlap_start = start + timedelta(minutes=30)
    overlap_end = overlap_start + timedelta(hours=1)

    booking2 = {
        "user_id": user.id,
        "car_id": car.id,
        "start_time": overlap_start.isoformat(),
        "end_time": overlap_end.isoformat(),
        "purpose": "self",
    }

    response2 = c.post("/bookings/", json=booking2)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Car is already booked for the selected time range"

