import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db

# 1. Configuration de la base de données de test en mémoire (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Surcharge de la dépendance get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Création du client de test
client = TestClient(app)

# 4. Création des tables avant chaque test, destruction après
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- DEBUT DES TESTS ---

def test_create_order_success():
    response = client.post(
        "/api/orders",
        headers={"Idempotency-Key": "test-key-1"},
        json={
            "customer_id": "cust_123", 
            "items": [{"product_id": "prod_1", "quantity": 1}]
        }
    )
    assert response.status_code == 202
    assert response.json()["status"] == "PENDING"
    assert "order_id" in response.json()

def test_create_order_validation_error():
    response = client.post(
        "/api/orders",
        headers={"Idempotency-Key": "test-key-2"},
        json={
            "customer_id": "cust_123", 
            "items": [{"product_id": "prod_1", "quantity": 0}] # Quantité 0 invalide
        }
    )
    assert response.status_code == 422 # Unprocessable Entity

def test_create_order_idempotency():
    payload = {
        "customer_id": "cust_123", 
        "items": [{"product_id": "prod_1", "quantity": 1}]
    }
    
    # Première requête
    response1 = client.post("/api/orders", headers={"Idempotency-Key": "test-key-3"}, json=payload)
    assert response1.status_code == 202
    
    # Deuxième requête identique avec la même clé
    response2 = client.post("/api/orders", headers={"Idempotency-Key": "test-key-3"}, json=payload)
    assert response2.status_code == 409 # Conflict