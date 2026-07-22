from app.database import Base
from sqlalchemy import Integer, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship
from datetime import datetime

class ClientVehicleInterest(Base):
    __tablename__ = "client_vehicle_interests"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    vehicle = relationship("Vehicle", back_populates="interested_clients")
    client = relationship("Client", back_populates="interests")