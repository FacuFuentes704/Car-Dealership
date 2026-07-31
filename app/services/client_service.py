from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.client import Client
from app.models.client_vehicle_interest import ClientVehicleInterest
from app.schemas.client import ClientStatus, ClientCreate, ClientResponse, ClientUpdate

def create_client(db: Session, client_data: ClientCreate):
    resultado = db.query(Client).filter(client_data.phone == Client.phone).first()
    if resultado:
        raise HTTPException(status_code=400, detail="Cliente ya registrado")
    new_client = Client(
        name=client_data.name,
        status=client_data.status,
        phone=client_data.phone,
        email=client_data.email,
        notes=client_data.notes
    )
    db.add(new_client)
    db.flush()
    for vehicle_id in client_data.vehicle_ids:
        vehicle_interest = ClientVehicleInterest(client_id = new_client.id, vehicle_id = vehicle_id)
        db.add(vehicle_interest)
    db.commit()
    db.refresh(new_client)
    return new_client

def get_clients(db: Session):
    resultado = db.query(Client).all()
    return resultado

def get_client_by_id(db: Session, client_id: int):
    resultado = db.query(Client).filter(Client.id == client_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return resultado

def update_client(db: Session, client_data: ClientUpdate, client_id:int):
    resultado = db.query(Client).filter(Client.id == client_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    datos = client_data.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(resultado, campo, valor)
    db.commit()
    db.refresh(resultado)
    return resultado

def delete_client(db: Session, client_id: int):
    resultado = db.query(Client).filter(Client.id == client_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(resultado)
    db.commit()
    return