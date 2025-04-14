import os
import sys
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI, HTTPException, Request
import logging
import json

# Configure minimal logging
logging.basicConfig(level=logging.ERROR)

# Load environment variables first
load_dotenv()

# Create a fresh FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "LIFT LinkedIn Content API - SECURE SERVER",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/webhook/linkedin")
async def webhook(request: Request):
    """Simple webhook endpoint that acknowledges all requests"""
    try:
        # Get raw body but don't log it
        body = await request.body()
        
        # Try to parse as JSON
        try:
            data = json.loads(body)
            return {
                "status": "success",
                "message": "Data received successfully"
            }
        except json.JSONDecodeError:
            return {
                "status": "warning",
                "message": "Received non-JSON data"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    # Hardcode port 8005 to avoid conflicts
    port = 8005
    
    print(f"Starting secure server on port {port}")
    print(f"Server is running at: http://localhost:{port}")
    print("Press CTRL+C to stop")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nServer error: {e}") 