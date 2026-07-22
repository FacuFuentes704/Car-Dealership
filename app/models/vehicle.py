from app.database import Base
from sqlalchemy import String, Integer, DateTime, Boolean, Column, Enum
import enum
from datetime import datetime

class Fuel_Type(str, enum.Enum):
    gasolina = "gasolina"
    diesel = "diesel"
    hibrido = "hibrido"
    gasolina_gnc = "gasolina con gnc"
    diesel_gnc = "diesel con gnc"

class Transmission(str, enum.Enum):
    automatico = "automatico"
    manual = "manual"

class Status(str, enum.Enum):
    available = "disponible"
    reserved = "reservado"
    sold = "vendido"

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(Enum(Fuel_Type))
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
