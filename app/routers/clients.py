from fastapi import Depends, APIRouter
from app.database import get_db
from app.auth.auth import get_current_user
from app.services.client_service import get_client_by_id, get_clients, delete_client, create_client, update_client, add_client_interest, delete_client_interests
from app.schemas.client import ClientCreate, ClientResponse, ClientStatus, ClientUpdate
from app.models.user import User
from app.schemas.Interests import InterestResponse
from sqlalchemy.orm import Session

clients_router = APIRouter(prefix="/clients",
                           tags=["clients"])

@clients_router.get("/", response_model=list[ClientResponse])
def show_clients(db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return get_clients(db)

@clients_router.post("/", response_model=ClientResponse)
def create(client_data: ClientCreate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return create_client(db, client_data)

@clients_router.get("/{client_id}", response_model=ClientResponse)
def show_by_id(client_id: int, db:Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return get_client_by_id(db, client_id)

@clients_router.patch("/{client_id}", response_model=ClientResponse)
def update(client_id: int, client_data: ClientUpdate, db: Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return update_client(db, client_data, client_id)

@clients_router.delete("/{client_id}", status_code=204)
def delete(client_id: int, db:Session = Depends(get_db), user_id: User = Depends(get_current_user)):
    return delete_client(db, client_id)

@clients_router.post("/{client_id}/interests/{vehicle_id}", response_model= InterestResponse)
def create_interest(client_id: int, vehicle_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    return add_client_interest(db, client_id, vehicle_id)

@clients_router.delete("/{client_id}/interests/{vehicle_id}", status_code=204)
def delete_interest(client_id: int, vehicle_id: int, db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    return delete_client_interests(db, client_id, vehicle_id)