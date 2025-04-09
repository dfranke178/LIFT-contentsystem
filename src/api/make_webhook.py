from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI(title="Make.com Webhook Handler")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

class LinkedInPostData(BaseModel):
    post_id: str
    content_type: str
    metrics: Dict[str, float]
    content: Optional[str] = None
    comments: Optional[str] = None
    timestamp: Optional[str] = None

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify the API key from Make.com"""
    expected_key = os.getenv("MAKE_API_KEY")
    if not expected_key:
        # For development/testing only
        return api_key
    if api_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LinkedIn Content Analysis API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENV", "production")
    }

@app.post("/webhook/linkedin")
async def linkedin_webhook(
    data: LinkedInPostData,
    api_key: str = Depends(verify_api_key)
):
    """Handle incoming LinkedIn post data from Make.com"""
    try:
        # Log the received data
        print(f"Received data for post {data.post_id}")
        
        # For initial testing, just return the received data
        return {
            "status": "success",
            "message": "Data received successfully",
            "data": {
                "post_id": data.post_id,
                "content_type": data.content_type,
                "metrics": data.metrics,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {
            "status": "error",
            "message": "Error processing request",
            "error": str(e)
        } 