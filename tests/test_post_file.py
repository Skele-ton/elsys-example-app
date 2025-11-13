from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app
from pathlib import Path

client = TestClient(app)
STORAGE_DIR = Path("storage")

def test_post_file_upload():
    filename = "upload_test.txt"
    file_path = STORAGE_DIR / filename
    if file_path.exists():
        file_path.unlink()

    files = {"file": (filename, b"sample data", "text/plain")}
    response = client.post("/files", files=files)
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "File stored successfully"
    assert data["filename"] == filename
    assert data["size"] == len(b"sample data")

    # Verify file was created
    assert file_path.exists()

    # Cleanup
    file_path.unlink()
