from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    try:
        logger.info(f"Received webhook data: {data}")
        return {
            "status": "success",
            "message": "Data received successfully",
            "data": {
                "post_id": data.post_id,
                "content_type": data.content_type,
                "metrics": data.metrics
            }
        }
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 