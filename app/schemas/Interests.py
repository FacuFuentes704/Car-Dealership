from pydantic import BaseModel
from datetime import datetime

class InterestResponse(BaseModel):
    id: int
    client_id: int
    vehicle_id: int
    created_at: datetime

    class Config:
        from_attributes = True