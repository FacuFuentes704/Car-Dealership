from app.database import Base
from sqlalchemy import Integer, String, DateTime, Boolean, Enum, Column
import enum
from datetime import datetime

class Status(str, enum.Enum):
    waiting = "waiting"
    negotiating = "negotiating"
    closed = "closed"
    lost = "lost"

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    status = Column(Enum(Status), nullable=False)
    phone = Column(String(50))
    email = Column(String(200))
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)