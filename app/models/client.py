from app.database import Base
from sqlalchemy import Integer, String, DateTime, Boolean, Enum, Column
import enum
from datetime import datetime
from sqlalchemy.orm import relationship

class ClientStatus(str, enum.Enum):
    waiting = "waiting"
    negotiating = "negotiating"
    closed = "closed"
    lost = "lost"

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    status = Column(Enum(ClientStatus), nullable=False)
    phone = Column(String(50))
    email = Column(String(200))
    notes = Column(String)
    is_active = Column(Boolean, default= True)
    created_at = Column(DateTime, default=datetime.utcnow)

    interests = relationship("ClientVehicleInterest", back_populates="client")