from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, TIMESTAMP, func, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="confirmée")
    purpose = Column(String(20), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="bookings")
    car = relationship("Car", back_populates="bookings")

    __table_args__ = (
        CheckConstraint("purpose IN ('self', 'accompanied')", name="bookings_purpose_check"),
        CheckConstraint("status IN ('confirmée', 'annulée', 'terminée')", name="bookings_status_check"),
    )