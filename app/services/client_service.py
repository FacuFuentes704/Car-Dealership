from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import HTTPException
from app.models.client import Client
from app.models.client_vehicle_interest import ClientVehicleInterest
from app.schemas.client import ClientStatus, ClientCreate, ClientResponse, ClientUpdate

def create_client(db: Session, client_data: ClientCreate):
    resultado = db.query(Client).filter(client_data.phone == Client.phone).first()
    if resultado:
        raise HTTPException(status_code=401, detail="Cliente ya registrado")
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