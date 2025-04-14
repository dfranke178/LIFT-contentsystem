import os
import sys
from dotenv import load_dotenv
import uvicorn
import logging

# Silence any libraries that might print environment variables
os.environ["PYTHONWARNINGS"] = "ignore"
logging.getLogger("anthropic").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

# Load environment variables from .env file (this should be first)
load_dotenv()

# Import the app after environment variables are loaded
from src.api.minimal_webhook import app

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.getenv("PORT", 8000))
    
    # Clear any pending stdout
    sys.stdout.flush()
    
    print(f"Starting server on port {port}")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nServer error: {e}") 