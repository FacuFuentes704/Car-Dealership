from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleSummary(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    price: Optional[int] = None
    status: str
    plate: Optional[str] = None
    engine_number: Optional[str] = None
    chassis_number: Optional[str] = None

    class Config:
        from_attributes = True

class ClientSummary(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    status: str
    address: Optional[str] = None
    locality: Optional[str] = None
    document_number: Optional[str] = None

    class Config:
        from_attributes = True

class InterestResponse(BaseModel):
    id: int
    created_at: datetime
    vehicle: VehicleSummary

    class Config:
        from_attributes = True

class VehicleInterestResponse(BaseModel):
    id: int
    created_at: datetime
    client: ClientSummary

    class Config:
        from_attributes = True