from fastapi.testclient import TestClient
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.make_webhook import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LinkedIn Content Analysis API"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_webhook_endpoint():
    test_data = {
        "post_id": "test123",
        "content_type": "article",
        "metrics": {
            "likes": 10,
            "comments": 5
        },
        "content": "Test post content",
        "timestamp": "2024-02-14T12:00:00Z"
    }
    
    response = client.post(
        "/webhook/linkedin",
        json=test_data,
        headers={"X-API-Key": "test-key"}
    )
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "success" 