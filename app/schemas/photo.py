from pydantic import BaseModel

class PhotoResponse(BaseModel):
    id: int
    url: str
    is_main: bool
    vehicle_id: int

    class Config:
        from_attributes = True