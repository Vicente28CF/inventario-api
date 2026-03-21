import os

os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "test_secret_key_local"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def usuario_token(client):
    client.post("/auth/registro", json={
        "nombre": "Vicente",
        "email": "vicente@test.com",
        "password": "123456"
    })
    response = client.post("/auth/login", data={
        "username": "vicente@test.com",
        "password": "123456"
    })
    return response.json()["access_token"]

@pytest.fixture(scope="function")
def admin_token(client):
    from app.models.usuario import Usuario
    from app.core.security import hash_password
    db = TestingSessionLocal()
    admin = Usuario(
        nombre="Admin",
        email="admin@test.com",
        password=hash_password("admin123"),
        rol="admin"
    )
    db.add(admin)
    db.commit()
    db.close()
    response = client.post("/auth/login", data={
        "username": "admin@test.com",
        "password": "admin123"
    })
    return response.json()["access_token"]
