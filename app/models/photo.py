from app.database import Base
from sqlalchemy import DateTime, Integer, String, Column, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    is_main = Column(Boolean, default=False)

    vehicle = relationship("Vehicle", back_populates="photo")