from app.database import Base
from sqlalchemy import String, Integer, Column, ForeignKey, Enum, DateTime, Boolean
import enum
from datetime import datetime
from sqlalchemy.orm import relationship

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
    reserva_amount = Column(Integer, nullable=True)
    entrega_amount = Column(Integer, nullable=True)
    otros_amount = Column(String, nullable=True)
    saldo_financiado = Column(Integer, nullable=True)
    boleto_generado = Column(Boolean, default=False)
    cantidad_cuotas = Column(Integer, nullable=True)
    monto_cuota = Column(Integer, nullable=True)
    fecha_primera_cuota = Column(DateTime, nullable=True)
    observaciones = Column(String, nullable=True)
    sale_date = Column(DateTime)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="sales")
    vehicle = relationship("Vehicle", back_populates="sale")