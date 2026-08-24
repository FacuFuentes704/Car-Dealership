from pydantic import BaseModel
from typing import Optional

class ClientDashboardResponse(BaseModel):
    negotiating: Optional[int]
    closed: Optional[int]
    waiting: Optional[int]
    lost: Optional[int]