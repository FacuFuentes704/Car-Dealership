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
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.models.company_settings import CompanySettings 
from app.routers.company_settings import company_settings_router

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    )

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(vehicles_router)
app.include_router(clients_router)
app.include_router(sales_router)
app.include_router(company_settings_router)