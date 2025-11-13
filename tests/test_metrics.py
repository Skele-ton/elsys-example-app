from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200

    data = response.json()
    # Check for expected metric fields
    for key in [
        "files_stored_total",
        "files_current",
        "total_storage_bytes",
        "total_storage_mb",
        "timestamp",
    ]:
        assert key in data

    # Types and ranges
    assert isinstance(data["files_stored_total"], int)
    assert isinstance(data["files_current"], int)
    assert data["total_storage_bytes"] >= 0
    assert data["total_storage_mb"] >= 0.0
