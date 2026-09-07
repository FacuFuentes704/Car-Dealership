import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
from app.auth.auth import hash_password
from app.models.user import User
from app.models.vehicle import Vehicle, Status
from app.models.client import Client, ClientStatus
from app.models.client_vehicle_interest import ClientVehicleInterest
from app.models.sale import Sale, PaymentMethod

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit = False, 
                                   autoflush= False, 
                                   bind= engine,
                                   expire_on_commit= False)

@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def usuario_de_prueba(db):
    hashed = hash_password("password123")
    usuario = User(name="Test User", email="test@test.com", password = hashed, is_active = True)
    db.add(usuario)
    db.commit()
    return usuario

@pytest.fixture
def usuario_inactivo(db):
    hashed = hash_password("password123")
    usuario = User(name="Test Inactivo", email="test2@test.com", password = hashed, is_active = False)
    db.add(usuario)
    db.commit()
    return usuario


@pytest.fixture()
def token_usuario(client, usuario_de_prueba):
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

@pytest.fixture()
def vehiculo_creado(db):
    vehiculo = Vehicle(fuel_type ="gasoline", 
                       transmission = "manual", 
                       status = Status.available, 
                       color = "negro", 
                       brand = "Toyota", 
                       model = "Corolla", 
                       year = 2026, 
                       plate = "AI 111 111", 
                       km = 1000, 
                       price = 40000000, 
                       description = "descripcion de prueba", 
                       condition = "used", 
                       is_active = True)    
    db.add(vehiculo)
    db.commit()
    return vehiculo

@pytest.fixture()
def vehiculo_inactivo(db):
    vehiculo = Vehicle(
        fuel_type="diesel",
        transmission="automatic",
        status="available",
        color="blanco",
        brand="Ford",
        model="Ranger",
        year=2020,
        plate="AB123CD",
        km=50000,
        price=22000000,
        description="vehiculo inactivo de prueba",
        condition="used",
        is_active=False
    )
    db.add(vehiculo)
    db.commit()
    return vehiculo

@pytest.fixture()
def cliente_creado(db):
    cliente = Client(name = "Test", 
                     status = ClientStatus.negotiating, 
                     phone = "12313", 
                     email = "test_cliente@test.com", 
                     notes= "abc", 
                     is_active = True)
    db.add(cliente)
    db.commit()
    return cliente

@pytest.fixture()
def client_interest(db, vehiculo_creado, cliente_creado):
    interes = ClientVehicleInterest(client_id = cliente_creado.id, vehicle_id = vehiculo_creado.id)
    db.add(interes)
    db.commit()
    return interes

@pytest.fixture()
def venta_creada(db, cliente_creado, vehiculo_creado, usuario_de_prueba):
    venta = Sale(vehicle_id = vehiculo_creado.id, 
                 client_id = cliente_creado.id, 
                 employee_id = usuario_de_prueba.id, 
                 sale_price = 2000, 
                 payment_method = PaymentMethod.cash)
    db.add(venta)
    db.commit()
    return venta

@pytest.fixture()
def vehiculo_no_disponible(db):
    vehiculo = Vehicle(
        fuel_type="diesel",
        transmission="automatic",
        status= Status.sold,
        color="blanco",
        brand="Ford",
        model="Ranger",
        year=2020,
        plate="AB123CD",
        km=50000,
        price=22000000,
        description="vehiculo inactivo de prueba",
        condition="used",
        is_active=True
    )
    db.add(vehiculo)
    db.commit()
    return vehiculo