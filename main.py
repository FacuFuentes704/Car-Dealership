from fastapi import FastAPI
from app.database import Base, engine
from app.routers.users import users_router, auth_router
from app.routers.clients import clients_router
from app.routers.sales import sales_router
from app.routers.vehicles import vehicles_router
from app.models.user import User
from app.models.sale import Sale
from app.models.client import Client
from app.models.vehicle import Vehicle
from app.models.client_vehicle_interest import ClientVehicleInterest
from app.models.photo import Photo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    )

Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(vehicles_router)
app.include_router(clients_router)
app.include_router(sales_router)