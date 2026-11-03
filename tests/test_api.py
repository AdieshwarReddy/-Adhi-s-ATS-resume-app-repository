from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_endpoint_no_file():
    response = client.post("/api/analyze", data={"job_description": "test"})
    # 422 because UploadFile is required
    assert response.status_code == 422 
