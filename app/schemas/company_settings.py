from pydantic import BaseModel
from typing import Optional

class CompanySettingsResponse(BaseModel):
    id: int
    business_name: str
    address: Optional[str] = None
    locality: Optional[str] = None
    document_number: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class CompanySettingsUpdate(BaseModel):
    business_name: Optional[str] = None
    address: Optional[str] = None
    locality: Optional[str] = None
    document_number: Optional[str] = None
    phone: Optional[str] = None