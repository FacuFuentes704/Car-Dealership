from pydantic import BaseModel
from app.models.sale import PaymentMethod
from typing import Optional
from datetime import datetime

class SaleCreate(BaseModel):
    client_id: Optional[int] = None
    employee_id: Optional[int] = None
    vehicle_id: int
    sale_price: int
    payment_method: Optional[PaymentMethod] = PaymentMethod.cash
    sale_date: Optional[datetime] = None
    notes: Optional[str] = None

class SaleResponse(BaseModel):
    id: int
    client_id: int
    employee_id: Optional[int] = None
    vehicle_id: int
    sale_price: int
    payment_method: Optional[PaymentMethod] = None
    sale_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SaleUpdate(BaseModel):
    client_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    employee_id: Optional[int] = None
    sale_price: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None
    sale_date: Optional[datetime] = None
    notes: Optional[str] = None