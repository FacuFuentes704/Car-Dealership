from pydantic import BaseModel
from app.models.sale import PaymentMethod
from typing import Optional
from datetime import datetime
from app.schemas.Interests import VehicleSummary, ClientSummary

class SaleCreate(BaseModel):
    client_id: Optional[int] = None
    vehicle_id: int
    sale_price: int
    payment_method: Optional[PaymentMethod] = PaymentMethod.cash
    sale_date: Optional[datetime] = None
    notes: Optional[str] = None

    reserva_amount: Optional[int] = None
    entrega_amount: Optional[int] = None
    otros_amount: Optional[str] = None
    saldo_financiado: Optional[int] = None
    cantidad_cuotas: Optional[int] = None
    monto_cuota: Optional[int] = None
    fecha_primera_cuota: Optional[datetime] = None
    observaciones: Optional[str] = None

    engine_number: Optional[str] = None
    chassis_number: Optional[str] = None

    client_address: Optional[str] = None
    client_locality: Optional[str] = None
    client_document_number: Optional[str] = None

class SaleResponse(BaseModel):
    id: int
    client: ClientSummary
    employee_id: Optional[int] = None
    vehicle: VehicleSummary
    sale_price: int
    payment_method: Optional[PaymentMethod] = None
    sale_date: Optional[datetime] = None
    notes: Optional[str] = None
    boleto_generado: Optional[bool] = None
    reserva_amount: Optional[int] = None
    entrega_amount: Optional[int] = None
    otros_amount: Optional[str] = None
    saldo_financiado: Optional[int] = None
    cantidad_cuotas: Optional[int] = None
    monto_cuota: Optional[int] = None
    fecha_primera_cuota: Optional[datetime] = None
    observaciones: Optional[str] = None
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
    boleto_generado: Optional[bool] = None
    notes: Optional[str] = None
    reserva_amount: Optional[int] = None
    entrega_amount: Optional[int] = None
    otros_amount: Optional[str] = None
    saldo_financiado: Optional[int] = None
    cantidad_cuotas: Optional[int] = None
    monto_cuota: Optional[int] = None
    fecha_primera_cuota: Optional[datetime] = None
    observaciones: Optional[str] = None

class SaleSummary(BaseModel):
    id: int
    sale_price: int
    sale_date: Optional[datetime] = None
    created_at: datetime
    boleto_generado: Optional[bool] = False
    client: ClientSummary

    class Config:
        from_attributes = True

class SaleSummaryConVehiculo(BaseModel):
    id: int
    sale_price: int
    sale_date: Optional[datetime] = None
    created_at: datetime
    boleto_generado: Optional[bool] = False
    vehicle: VehicleSummary

    class Config:
        from_attributes = True