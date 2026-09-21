from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sale import Sale
from app.models.vehicle import Vehicle, Status
from app.models.client import Client
from app.schemas.sale import SaleCreate, SaleUpdate
from datetime import date
from app.models.client_vehicle_interest import ClientVehicleInterest

def create_sale(db: Session, sale_data: SaleCreate, employee_id: int):
    vehiculo = db.query(Vehicle).filter(Vehicle.id == sale_data.vehicle_id).first()
    if not vehiculo:
        raise HTTPException(status_code= 404, detail="Vehiculo no existente")
    cliente = db.query(Client).filter(Client.id == sale_data.client_id).first()
    if not cliente:
        raise HTTPException(status_code= 404, detail="Cliente no existente")
    if cliente.is_active is False:
        raise HTTPException(status_code= 400, detail="Cliente inactivo")
    if vehiculo.is_active is False:
        raise HTTPException(status_code= 400, detail= "Vehiculo inactivo")
    if vehiculo.status != Status.available:
        raise HTTPException(status_code=400, detail="Vehiculo no disponible")
    new_sale = Sale(**sale_data.model_dump(), employee_id = employee_id)
    db.add(new_sale)
    vehiculo.status = Status.sold
    resultado = db.query(ClientVehicleInterest).filter(ClientVehicleInterest.vehicle_id == sale_data.vehicle_id).all()
    for interes in resultado:
        db.delete(interes)
    db.commit()
    db.refresh(new_sale)
    return new_sale
    
def get_sales(db: Session, search: str = None, fecha_desde: date = None, fecha_hasta: date = None):
    query = db.query(Sale).join(Client).join(Vehicle)

    if search:
        query = query.filter(
            Client.name.ilike(f"%{search}%") |
            Vehicle.brand.ilike(f"%{search}%") |
            Vehicle.model.ilike(f"%{search}%")
        )
    if fecha_desde:
        query = query.filter(Sale.created_at >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Sale.created_at <= fecha_hasta)

    return query.all()

def get_sales_by_id(db: Session, sale_id: int):
    resultado = db.query(Sale).filter(Sale.id == sale_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return resultado

def update_sale(db:Session, sale_data: SaleUpdate, sale_id: int):
    resultado = db.query(Sale).filter(Sale.id == sale_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    datos = sale_data.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(resultado, campo, valor)
    db.commit()
    db.refresh(resultado)
    return resultado

def delete_sale(db: Session, sale_id:int):
    resultado = db.query(Sale).filter(Sale.id == sale_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    db.delete(resultado)
    db.commit()
    return