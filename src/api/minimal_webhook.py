import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Dict, Optional, Union
import logging
import json
import re
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class LinkedInPostData(BaseModel):
    post_id: Union[str, int] = Field(..., description="Unique identifier for the post")
    content_type: str = Field(..., description="Type of content (article, media, text)")
    metrics: Dict[str, Union[float, int]] = Field(..., description="Engagement metrics")
    content: Optional[str] = Field(None, description="The actual content of the post")
    content_base64: Optional[str] = Field(None, description="Base64 encoded content of the post")
    comments: Optional[str] = Field(None, description="Comments on the post")
    timestamp: Optional[str] = Field(None, description="When the post was created")

    @validator('content_type')
    def validate_content_type(cls, v):
        valid_types = ['article', 'media', 'text', 'text/image']
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
        raw_text = raw_body.decode('utf-8', errors='replace')
        logger.info(f"Raw request body: {raw_text}")
        
        try:
            # Try standard JSON parsing first
            data = json.loads(raw_text)
        except json.JSONDecodeError as e:
            logger.warning(f"Standard JSON parsing failed: {str(e)}")
            logger.info("Attempting to fix and parse the JSON...")
            
            # Try to fix common JSON issues
            fixed_json = raw_text
            
            # Fix control characters in content field
            content_pattern = r'"content":\s*"([^"]*)'
            match = re.search(content_pattern, fixed_json)
            if match:
                content_text = match.group(1)
                # Replace problematic characters
                sanitized_content = "Content contains special characters (sanitized)"
                fixed_json = re.sub(content_pattern, f'"content": "{sanitized_content}', fixed_json)
            
            # Fix missing commas between fields
            fixed_json = re.sub(r'"\s*"', '", "', fixed_json)
            
            # Try parsing the fixed JSON
            try:
                data = json.loads(fixed_json)
                logger.info("Successfully parsed fixed JSON")
            except json.JSONDecodeError as e2:
                logger.error(f"Could not fix JSON: {str(e2)}")
                # Create minimal valid data
                data = {
                    "post_id": "error",
                    "content_type": "text",
                    "metrics": {"likes": 0, "comments": 0, "shares": 0},
                    "content": "Error parsing content",
                    "timestamp": "0"
                }
                logger.info(f"Created fallback data: {json.dumps(data)}")

        logger.info(f"Parsed JSON data: {json.dumps(data, indent=2)}")
        
        # Handle base64 encoded content if present
        if 'content_base64' in data and data['content_base64']:
            try:
                # Decode the base64 content
                decoded_content = base64.b64decode(data['content_base64']).decode('utf-8')
                logger.info("Successfully decoded base64 content")
                # Replace content with the decoded value
                data['content'] = decoded_content
            except Exception as e:
                logger.error(f"Error decoding base64 content: {str(e)}")
                # If we can't decode, leave the existing content as is
        
        # If content is missing or was sanitized, but we have the raw text,
        # try to extract the content directly
        if ('content' not in data or 
            data.get('content') == "Content contains special characters (sanitized)" or
            not data.get('content')):
            try:
                # Try to extract content from the raw request using regex
                content_match = re.search(r'"content":\s*"(.*?)(?:",|\"\})', raw_text, re.DOTALL)
                if content_match:
                    extracted_content = content_match.group(1)
                    # Replace escaped quotes and newlines
                    extracted_content = extracted_content.replace('\\"', '"').replace('\\n', '\n')
                    data['content'] = extracted_content
                    logger.info("Successfully extracted content from raw request")
            except Exception as e:
                logger.error(f"Error extracting content from raw request: {str(e)}")
        
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
        
        # Prepare the response with the full content
        response_data = {
            "status": "success",
            "message": "Data received successfully",
            "data": {
                "post_id": str(post_data.post_id),
                "content_type": post_data.content_type,
                "metrics": {k: float(v) for k, v in post_data.metrics.items()},
                "content": post_data.content
            }
        }
        
        # Log the size of content being processed
        if post_data.content:
            logger.info(f"Content length: {len(post_data.content)} characters")
        
        return response_data
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid data format",
                "message": str(e),
                "received_data": raw_text if 'raw_text' in locals() else None
            }
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 