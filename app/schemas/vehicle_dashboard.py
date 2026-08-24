from pydantic import BaseModel
from typing import Optional

class VehicleDashboardResponse(BaseModel):
    disponibles: int
    reservados: int
    vendidos_mes: int