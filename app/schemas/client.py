from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.client import ClientStatus
from datetime import datetime


class ClientCreate(BaseModel):
    name: str
    status: ClientStatus
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    vehicle_ids: Optional[list[int]] = []

class ClientResponse(BaseModel):
    id: int
    name:str
    status: ClientStatus
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ClientStatus] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None
    phone: Optional[str] = None
