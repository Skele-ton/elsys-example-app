from locust import HttpUser, task, between
import random
import string
from pathlib import Path
from io import BytesIO

STORAGE_DIR = Path("storage")

def random_filename(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length)) + ".txt"

class FileStorageUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1-3 seconds between tasks

    @task(3)
    def get_random_file(self):
        """GET /files/{filename}"""
        files = [f.name for f in STORAGE_DIR.iterdir() if f.is_file()]
        if files:
            filename = random.choice(files)
        else:
            # If no file exists yet, try a placeholder
            filename = "nonexistent.txt"
        self.client.get(f"/files/{filename}", name="/files/{filename}")

    @task(2)
    def post_file(self):
        """POST /files"""
        # Generate a small random file in memory
        filename = random_filename()
        content = BytesIO(f"Test content for {filename}".encode("utf-8"))
        files = {"file": (filename, content, "text/plain")}
        self.client.post("/files", files=files)

    @task(5)
    def list_files(self):
        """GET /files"""
        self.client.get("/files")
