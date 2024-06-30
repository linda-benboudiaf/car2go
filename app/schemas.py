from pydantic import BaseModel
from datetime import date


class CarBase(BaseModel):
    brand: str
    model: str
    year: int


class CarCreate(CarBase):
    pass


class Car(CarBase):
    id: int
    availability: bool

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    fullname: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ReservationBase(BaseModel):
    user_id: int
    car_id: int
    start_date: date
    end_date: date


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int

    class Config:
        orm_mode = True
