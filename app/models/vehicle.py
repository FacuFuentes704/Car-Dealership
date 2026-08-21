from app.database import Base
from sqlalchemy import String, Integer, DateTime, Boolean, Column, Enum
import enum
from datetime import datetime
from sqlalchemy.orm import relationship

class FuelType(str, enum.Enum):
    gasoline = "gasoline"
    diesel = "diesel"
    hybrid = "hybrid"
    gasoline_gnc = "gasoline_gnc"
    diesel_gnc = "diesel_gnc"

class Transmission(str, enum.Enum):
    automatic = "automatic"
    manual = "manual"

class Status(str, enum.Enum):
    available = "available"
    reserved = "reserved"
    sold = "sold"

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(Enum(FuelType))
    transmission = Column(Enum(Transmission))
    status = Column(Enum(Status), default=Status.available)
    color = Column(String(100))
    brand = Column(String(200), nullable=False)
    model = Column(String(150), nullable=False)
    year = Column(Integer, nullable=False)
    plate = Column(String(100))
    km = Column(Integer)
    price = Column(Integer, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    interested_clients = relationship("ClientVehicleInterest", back_populates="vehicle")
    photos = relationship("Photo", back_populates="vehicle")