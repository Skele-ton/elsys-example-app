from fastapi.testclient import TestClient
from main import app
from pathlib import Path

client = TestClient(app)
STORAGE_DIR = Path("storage")

def test_list_files():
    # Ensure at least one file exists
    filename = "sample.txt"
    file_path = STORAGE_DIR / filename
    file_path.write_text("abc")

    response = client.get("/files")
    data = response.json()
    assert response.status_code == 200
    assert "files" in data
    assert filename in data["files"]
    assert "count" in data and isinstance(data["count"], int)

    # Cleanup
    file_path.unlink()
