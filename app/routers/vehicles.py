from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services.vehicle_service import create_vehicle, update_vehicle, delete_vehicle, get_vehicles, get_vehicles_by_id
from app.auth.auth import get_current_user
from app.models.user import User
from app.database import get_db

vehicles_router = APIRouter(prefix="/vehicles",
                            tags=["vehicles"])

@vehicles_router.post("/", response_model=VehicleResponse)
def create(vehicle_data: VehicleCreate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return create_vehicle(db, vehicle_data)

@vehicles_router.get("/", response_model=list[VehicleResponse])
def show_vehicles(db: Session = Depends(get_db)):
    return get_vehicles(db)

@vehicles_router.patch("/{vehicle_id}", response_model=VehicleResponse)
def update(vehicle_id: int, vehicle_data: VehicleUpdate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return update_vehicle(db, vehicle_data, vehicle_id)

@vehicles_router.get("/{vehicle_id}", response_model=VehicleResponse)
def show_by_id(vehicle_id: int, db:Session = Depends(get_db)):
    return get_vehicles_by_id(db, vehicle_id)

@vehicles_router.delete("/{vehicle_id}", response_model=VehicleResponse)
def delete(vehicle_id: int, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return delete_vehicle(db, vehicle_id)