import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan manager for FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up webhook server...")
    yield
    logger.info("Shutting down webhook server...")

app = FastAPI(lifespan=lifespan)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request data", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

async def process_webhook_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process the webhook data asynchronously."""
    # Add your webhook processing logic here
    return {"status": "processed", "data": data}

@app.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        logger.info(f"Received webhook data: {data}")

        # Process with timeout
        async with asyncio.timeout(10):  # 10 second timeout
            result = await process_webhook_data(data)
            return result

    except asyncio.TimeoutError:
        logger.error("Webhook processing timed out")
        raise HTTPException(status_code=504, detail="Processing timeout")
    except ValueError as e:
        logger.error(f"Invalid JSON data: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 