from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import json
from datetime import datetime
import os
from pathlib import Path

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

def get_feedback_loop():
    """Lazy initialization of FeedbackLoop"""
    try:
        from src.utils.feedback_loop import FeedbackLoop
        return FeedbackLoop()
    except Exception as e:
        print(f"Warning: Could not initialize FeedbackLoop: {str(e)}")
        return None

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
        # Initialize feedback loop
        feedback_loop = get_feedback_loop()
        
        if not feedback_loop:
            return {
                "status": "success",
                "message": "Data received but feedback system is not available",
                "data": {
                    "post_id": data.post_id,
                    "content_type": data.content_type,
                    "timestamp": datetime.now().isoformat()
                }
            }
        
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
        print(f"Error processing webhook: {str(e)}")
        return {
            "status": "error",
            "message": "Data received but processing failed",
            "error": str(e),
            "data": {
                "post_id": data.post_id,
                "content_type": data.content_type,
                "timestamp": datetime.now().isoformat()
            }
        }

# Ensure the feedback directory exists
try:
    os.makedirs("feedback_data", exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create feedback directory: {str(e)}") 