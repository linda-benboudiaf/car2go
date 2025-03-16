from sqlalchemy import Column, Integer, String, Date, Boolean, TIMESTAMP, DECIMAL, CheckConstraint
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    modele = Column(String(100), nullable=False)
    annee_fab = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    plaque = Column(String(20), unique=True, nullable=False)
    controle_technique = Column(Date, nullable=False)
    prix_par_heure = Column(DECIMAL(10,2), nullable=False, default=20.00)
    disponible = Column(Boolean, default=True)
    image_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('double commande', 'classique')", name="cars_type_check"),
    )

    bookings = relationship("Booking", back_populates="car")