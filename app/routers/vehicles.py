from fastapi import Depends, APIRouter, File, UploadFile
from app.schemas.photo import PhotoResponse
from app.services.photo_service import upload_photo, update_photo, delete_photos
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate, VehiclePublicResponse
from app.services.vehicle_service import create_vehicle, update_vehicle, delete_vehicle, get_vehicles, get_vehicles_by_id
from app.auth.auth import get_current_user
from app.models.user import User
from app.database import get_db

vehicles_router = APIRouter(prefix="/vehicles",
                            tags=["vehicles"])

@vehicles_router.post("/", response_model=VehicleResponse)
def create(vehicle_data: VehicleCreate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return create_vehicle(db, vehicle_data)

@vehicles_router.get("/", response_model=list[VehiclePublicResponse])
def show_vehicles(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 20,
    brand: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None,
    fuel_type: Optional[str] = None,
    transmission: Optional[str] = None,
    status: Optional[str] = None,
    km_max: Optional[int] = None,
    search: Optional[str] = None
):
    return get_vehicles(db, page, limit, brand, model, year, price_min, price_max, fuel_type, transmission, status, km_max, search)

@vehicles_router.get("/admin", response_model=list[VehicleResponse])
def show_vehicles_adms(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 20,
    user_data: User = Depends(get_current_user),
    brand: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None,
    fuel_type: Optional[str] = None,
    transmission: Optional[str] = None,
    status: Optional[str] = None,
    km_max: Optional[int] = None,
    search: Optional[str] = None
):
    return get_vehicles(db, page, limit, brand, model, year, price_min, price_max, fuel_type, transmission, status, km_max, search)

@vehicles_router.patch("/{vehicle_id}", response_model=VehicleResponse)
def update(vehicle_id: int, vehicle_data: VehicleUpdate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return update_vehicle(db, vehicle_data, vehicle_id)

@vehicles_router.delete("/{vehicle_id}", status_code=204)
def delete(vehicle_id: int, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return delete_vehicle(db, vehicle_id)

@vehicles_router.post("/{vehicle_id}/photos", response_model=list[PhotoResponse])
def photos(vehicle_id: int, db: Session = Depends(get_db), photos: list[UploadFile] = File(), user_id: User = Depends(get_current_user)):
    fotos_subidas = []
    for i, photo in enumerate(photos):
        is_main = i == 0
        foto_subida = upload_photo(db, vehicle_id, is_main, photo)
        fotos_subidas.append(foto_subida)
    return fotos_subidas

@vehicles_router.patch("/{vehicle_id}/photos/{photo_id}", response_model=PhotoResponse)
def up_photo(vehicle_id: int, photo_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    return update_photo(db, photo_id, vehicle_id)

@vehicles_router.get("/{vehicle_id}", response_model=VehiclePublicResponse)
def show_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    return get_vehicles_by_id(db, vehicle_id)

@vehicles_router.get("/{vehicle_id}/admin", response_model=VehicleResponse)
def show_by_id_adm(vehicle_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    return get_vehicles_by_id(db, vehicle_id)

@vehicles_router.delete("/{vehicle_id}/photos/{photo_id}", status_code=204)
def delete_foto(vehicle_id: int, photo_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    return delete_photos(db, photo_id)