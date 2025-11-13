from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app
import os
from pathlib import Path

client = TestClient(app)
STORAGE_DIR = Path("storage")

def test_get_file_by_name(tmp_path):
    # Create a temporary test file
    filename = "testfile.txt"
    file_path = STORAGE_DIR / filename
    file_path.write_text("hello world")

    # Request the file
    response = client.get(f"/files/{filename}")
    assert response.status_code == 200
    assert response.content == b"hello world"
    assert response.headers["content-type"].startswith("application/octet-stream")

    # Cleanup
    file_path.unlink()
