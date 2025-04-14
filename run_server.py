import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file - this should be first
load_dotenv()

# Import the app after environment variables are loaded
from src.api.minimal_webhook import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 