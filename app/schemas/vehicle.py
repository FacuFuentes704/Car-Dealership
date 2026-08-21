from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.vehicle import FuelType, Status, Transmission
from app.schemas.photo import PhotoResponse
from app.schemas.Interests import VehicleInterestResponse

class VehicleCreate(BaseModel):
    fuel_type: Optional[FuelType] = FuelType.gasoline
    status: Optional[Status] = Status.available
    transmission: Optional[Transmission] = Transmission.manual
    color: Optional[str] = None
    brand: str
    model: str
    year: int
    plate: Optional[str] = None
    km: Optional[int] = 0
    price: int
    description: Optional[str] = None

class VehicleResponse(BaseModel):
    id: int
    status: Status
    transmission: Transmission
    color: Optional[str] = None
    photos: list[PhotoResponse] = []
    brand: str
    fuel_type: FuelType
    model: str
    interested_clients: list[VehicleInterestResponse] = []
    year: int
    plate: Optional[str] = None
    km: int
    price: int
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class VehicleUpdate(BaseModel):
    fuel_type: Optional[FuelType] = None
    status: Optional[Status] = None
    color: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    plate: Optional[str] = None
    km: Optional[int] = None
    price: Optional[int] = None
    description: Optional[str] = None
