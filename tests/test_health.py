from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "File Storage API"
    assert "timestamp" in data
