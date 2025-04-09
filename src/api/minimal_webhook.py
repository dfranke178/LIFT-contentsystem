import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class LinkedInPostData(BaseModel):
    post_id: Union[str, int] = Field(..., description="Unique identifier for the post")
    content_type: str = Field(..., description="Type of content (article, media, text)")
    metrics: Dict[str, Union[float, int]] = Field(..., description="Engagement metrics")
    content: Optional[str] = Field(None, description="The actual content of the post")
    comments: Optional[str] = Field(None, description="Comments on the post")
    timestamp: Optional[str] = Field(None, description="When the post was created")

    @validator('content_type')
    def validate_content_type(cls, v):
        valid_types = ['article', 'media', 'text']
        if v.lower() not in valid_types:
            raise ValueError(f'content_type must be one of {valid_types}')
        return v.lower()

    @validator('metrics')
    def validate_metrics(cls, v):
        required_metrics = ['likes', 'comments', 'shares']
        for metric in required_metrics:
            if metric not in v:
                raise ValueError(f'Missing required metric: {metric}')
        return v

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
        # Log the received data
        logger.info(f"Received webhook data: {data.dict()}")
        
        # Convert post_id to string if it's a number
        post_id = str(data.post_id)
        
        # Convert metrics values to float
        metrics = {k: float(v) for k, v in data.metrics.items()}
        
        return {
            "status": "success",
            "message": "Data received successfully",
            "data": {
                "post_id": post_id,
                "content_type": data.content_type,
                "metrics": metrics
            }
        }
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid data format",
                "message": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 