import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
from app.auth.auth import hash_password
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

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