from sqlalchemy import Column, Integer, String, Date, CheckConstraint
from database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    telephone = Column(String(20), nullable=False)
    adresse = Column(String(200), nullable=False)
    date_naissance = Column(Date, nullable=False)
    role = Column(String(20), nullable=False)
    license_date = Column(Date, nullable=True)
    numero_permis = Column(String(20), nullable=True)
    numero_livret = Column(String(20), nullable=True)

    def verify_password(self, password: str) -> bool:
        """Vérifie si le mot de passe fourni correspond au hash stocké."""
        return pwd_context.verify(password, self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hache un mot de passe avant de le stocker."""
        return pwd_context.hash(password)

    __table_args__ = (
        CheckConstraint("role IN ('apprenti', 'accompagnateur')", name="users_role_check"),
        CheckConstraint(
            "(role = 'accompagnateur' AND numero_permis IS NOT NULL AND numero_livret IS NULL) OR "
            "(role = 'apprenti' AND numero_livret IS NOT NULL AND numero_permis IS NULL)",
            name="users_check_combined"
        ),

    )
    bookings = relationship("Booking", back_populates="user")