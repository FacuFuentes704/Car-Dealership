from fastapi import HTTPException
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, FuelType, Status, Transmission
from app.models.vehicle import Vehicle
from sqlalchemy.orm import Session

def create_vehicle(db: Session, vehicle_data: VehicleCreate):
    if vehicle_data.plate:
        resultado = db.query(Vehicle).filter(Vehicle.plate == vehicle_data.plate).first()
        if resultado:
            raise HTTPException(status_code=400, detail="Patente duplicada")
    new_vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

def get_vehicles(db: Session, page: int = 1, limit: int = 20, brand: str = None, model: str = None, year: int = None, price_min: int = None, price_max: int = None, fuel_type: FuelType = None, transmission: Transmission = None, status: Status = None, km_max: int = None, search: str = None):
    query = db.query(Vehicle)
    filtros = {
        Vehicle.brand: brand,
        Vehicle.model: model,
        Vehicle.year: year,
        Vehicle.fuel_type: fuel_type,
        Vehicle.transmission: transmission,
        Vehicle.status: status,
    }
    for campo, valor in filtros.items():
        if valor:
            query = query.filter(campo == valor)
    if price_min:
        query = query.filter(Vehicle.price >= price_min)

    if price_max:
        query = query.filter(Vehicle.price <= price_max)

    if km_max:
        query = query.filter(Vehicle.km <= km_max)

    if search:
        query = query.filter(
            Vehicle.brand.ilike(f"%{search}%") |
            Vehicle.model.ilike(f"%{search}%")
        )
    query = query.offset((page - 1) * limit).limit(limit)
    return query.all()
    
def get_vehicles_by_id(db: Session, vehicle_id: int, ):
    resultado = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return resultado

def update_vehicle(db: Session, vehicle_data: VehicleUpdate, vehicle_id:int):
    resultado = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    datos = vehicle_data.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr (resultado, campo, valor)
    db.commit()
    db.refresh(resultado)
    return resultado

def delete_vehicle(db: Session, vehicle_id: int):
    resultado = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail= "Vehiculo no encontrado")
    db.delete(resultado)
    db.commit()
    return