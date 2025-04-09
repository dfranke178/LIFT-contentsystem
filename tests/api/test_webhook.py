from fastapi.testclient import TestClient
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional

# Create a minimal test app
app = FastAPI()

class LinkedInPostData(BaseModel):
    post_id: str
    content_type: str
    metrics: Dict[str, float]
    content: Optional[str] = None
    comments: Optional[str] = None
    timestamp: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "LinkedIn Content Analysis API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@app.post("/webhook/linkedin")
async def linkedin_webhook(data: LinkedInPostData):
    return {
        "status": "success",
        "message": "Data received successfully",
        "data": {
            "post_id": data.post_id,
            "content_type": data.content_type,
            "metrics": data.metrics
        }
    }

# Create test client
client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LinkedIn Content Analysis API"
    assert response.json()["status"] == "running"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
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
        json=test_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["post_id"] == test_data["post_id"] 