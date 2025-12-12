from fastapi.testclient import TestClient
from src.api.main import app
import os

client = TestClient(app)

def test_docs_page():
    response = client.get("/docs")
    assert response.status_code == 200

def test_ingest_missing_file():
    response = client.post("/ingest")
    assert response.status_code == 422

# Note: Further testing requires a real PDF file or mocking.
