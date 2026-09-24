from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.vehicle import FuelType, Status, Transmission, Condition
from app.schemas.photo import PhotoResponse
from app.schemas.sale import SaleSummary
from app.schemas.Interests import VehicleInterestResponse

class VehicleCreate(BaseModel):
    fuel_type: Optional[FuelType] = FuelType.gasoline
    status: Optional[Status] = Status.available
    transmission: Optional[Transmission] = Transmission.manual
    color: Optional[str] = None
    is_offer: Optional[bool] = None
    brand: str
    price_cash: Optional[int] = None
    price_internal: Optional[int] = None
    model: str
    condition: Optional[Condition] = Condition.used
    year: int
    plate: Optional[str] = None
    km: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
    features: Optional[dict] = None

class VehicleResponse(BaseModel):
    id: int
    status: Status
    transmission: Transmission
    color: Optional[str] = None
    photos: list[PhotoResponse] = []
    brand: str
    sale: Optional[SaleSummary] = None
    is_active: bool
    is_offer: Optional[bool] = None
    condition: Condition
    price_cash: Optional[int] = None
    price_internal: Optional[int] = None
    fuel_type: FuelType
    model: str
    interested_clients: list[VehicleInterestResponse] = []
    year: int
    plate: Optional[str] = None
    km: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
    engine_number: Optional[str] = None
    chassis_number: Optional[str] = None
    features: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

class VehiclePublicResponse(BaseModel):
    id: int
    status: Status
    transmission: Transmission
    color: Optional[str] = None
    brand: str
    fuel_type: FuelType
    is_offer: Optional[bool] = None
    condition: Condition
    model: str
    year: int
    km: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
    features: Optional[dict] = None
    photos: list[PhotoResponse] = []

    class Config:
        from_attributes = True

class VehicleUpdate(BaseModel):
    fuel_type: Optional[FuelType] = None
    status: Optional[Status] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    is_offer: Optional[bool] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price_cash: Optional[int] = None
    price_internal: Optional[int] = None
    condition: Optional[Condition] = None
    plate: Optional[str] = None
    is_active: Optional[bool] = None
    km: Optional[int] = None
    transmission: Optional[Transmission] = None
    price: Optional[int] = None
    description: Optional[str] = None
    engine_number: Optional[str] = None
    chassis_number: Optional[str] = None
    features: Optional[dict] = None