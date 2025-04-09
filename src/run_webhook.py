import uvicorn
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = str(Path(__file__).parent)
if src_path not in sys.path:
    sys.path.append(src_path)

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment variable or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    # Run the server
    uvicorn.run(
        "src.api.make_webhook:app",
        host="0.0.0.0",
        port=port,
        reload=True
    ) 