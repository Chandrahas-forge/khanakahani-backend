import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200

def test_redoc_available():
    response = client.get("/redoc")
    assert response.status_code == 200

# If you have a root endpoint or health check, add tests for them. For example:
def test_health_check():
    # You might consider adding a health check, for example at "/health"
    response = client.get("/health")
    assert response.status_code in (200, 404)  # Adjust based on your implementation