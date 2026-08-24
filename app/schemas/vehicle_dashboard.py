from pydantic import BaseModel
from typing import Optional

class VehicleDashboardResponse(BaseModel):
    disponibles: Optional[int]
    reservados: Optional[int]
    vendidos_mes: Optional[int]