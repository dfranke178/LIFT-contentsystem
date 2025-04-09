from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import json
from datetime import datetime
import os
from pathlib import Path
from src.utils.feedback_loop import FeedbackLoop

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

# Initialize feedback loop
feedback_loop = FeedbackLoop()

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
    return {"message": "LinkedIn Content Analysis API", "status": "running"}

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
        # Add feedback to the system
        feedback_loop.add_feedback(
            content_id=data.post_id,
            metrics={
                **data.metrics,
                "content_type": data.content_type
            },
            comments=data.comments or f"Automatically collected from Make.com at {datetime.now().isoformat()}"
        )
        
        # Run analysis
        analysis = feedback_loop.analyze_feedback()
        patterns = feedback_loop.analyze_patterns()
        
        return {
            "status": "success",
            "message": "Data processed successfully",
            "analysis": {
                "feedback_analysis": analysis,
                "ml_patterns": patterns
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create feedback directory if it doesn't exist
os.makedirs("feedback_data", exist_ok=True) 