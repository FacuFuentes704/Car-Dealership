from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleSummary(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    price: int
    status: str

    class Config:
        from_attributes = True

class ClientSummary(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    status: str

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