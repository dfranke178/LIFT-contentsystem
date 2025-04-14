import os
import sys
import logging
import subprocess

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("dashboard_app")

def main():
    """
    Main function to run the Streamlit dashboard.
    This script handles the necessary environment setup before launching Streamlit.
    """
    logger.info("Starting Dashboard Application")
    
    # Create necessary directories if they don't exist
    os.makedirs("analysis", exist_ok=True)
    
    # Check if analysis files exist, create placeholders if needed
    if not os.path.exists("analysis/analysis_results.json"):
        import json
        logger.info("Creating placeholder analysis data")
        placeholder_data = {
            "total_posts": 0,
            "average_engagement": {"likes": 0, "comments": 0, "shares": 0},
            "content_type_distribution": {"text": 0, "image": 0, "video": 0},
            "top_topics": [["No data", 0]]
        }
        with open("analysis/analysis_results.json", "w") as f:
            json.dump(placeholder_data, f)
    
    # Get the port from the environment or use default
    port = int(os.environ.get("PORT", 8501))
    logger.info(f"Starting Streamlit dashboard on port {port}")
    
    # Run Streamlit with the correct settings for Heroku
    cmd = [
        "streamlit", "run", 
        "src/dashboard.py", 
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    try:
        # Use check=True to make sure the process waits for Streamlit
        subprocess.run(cmd, check=True)
    except Exception as e:
        logger.error(f"Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 