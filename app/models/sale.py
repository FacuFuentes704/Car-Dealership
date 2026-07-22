from app.database import Base
from sqlalchemy import String, Integer, Column, ForeignKey, Enum, DateTime
import enum
from datetime import datetime

class PaymentMethod(str, enum.Enum):
    cash = "cash"
    financing = "financing"
    transfer = "transfer"
    cash_financing = "cash_financing"
    trade_in = "trade_in"
    mixed = "mixed"

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    sale_price = Column(Integer, nullable=False)
    payment_method = Column(Enum(PaymentMethod))
    sale_date = Column(DateTime)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
