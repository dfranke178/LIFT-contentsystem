import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Dict, Optional, Union
import logging
import json

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
async def linkedin_webhook(request: Request):
    try:
        # Log the raw request body
        raw_body = await request.body()
        logger.info(f"Raw request body: {raw_body.decode()}")
        
        # Parse the JSON data
        data = await request.json()
        logger.info(f"Parsed JSON data: {json.dumps(data, indent=2)}")
        
        # Validate the data
        try:
            post_data = LinkedInPostData(**data)
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            logger.error(f"Failed data: {json.dumps(data, indent=2)}")
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "Validation error",
                    "message": str(e),
                    "received_data": data
                }
            )
        
        return {
            "status": "success",
            "message": "Data received successfully",
            "data": {
                "post_id": str(post_data.post_id),
                "content_type": post_data.content_type,
                "metrics": {k: float(v) for k, v in post_data.metrics.items()}
            }
        }
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid JSON",
                "message": str(e),
                "raw_body": raw_body.decode() if 'raw_body' in locals() else None
            }
        )
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid data format",
                "message": str(e),
                "received_data": data if 'data' in locals() else None
            }
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 