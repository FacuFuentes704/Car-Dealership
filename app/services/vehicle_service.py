from fastapi import HTTPException
from app.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate
from app.models.vehicle import Vehicle
from sqlalchemy.orm import Session

def create_vehicle(db: Session, vehicle_data: VehicleCreate):
    resultado = db.query(Vehicle).filter(Vehicle.plate == vehicle_data.plate).first()
    if resultado:
        raise HTTPException(status_code=400, detail="Patente duplicada")
    new_vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle
    
def get_vehicles(db: Session):
    resultado = db.query(Vehicle).all()
    return resultado

def get_vehicles_by_id(db: Session, vehicle_id: int):
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