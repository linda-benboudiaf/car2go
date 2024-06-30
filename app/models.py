from sqlalchemy import create_engine, Column, BigInteger, String, Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Car(Base):
    __tablename__ = "cars"
    id = Column(BigInteger, primary_key=True, index=True)
    brand = Column(String, index=True)
    model = Column(String, index=True)
    year = Column(BigInteger)
    availability = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)


class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    car_id = Column(BigInteger, ForeignKey("cars.id"))
    start_date = Column(Date)
    end_date = Column(Date)

    user = relationship("User")
    car = relationship("Car")
