import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 