#!/usr/bin/env python
"""
Script to run analytics on LinkedIn post data and start the dashboard.
"""
import os
import sys
import logging
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("analytics_runner")

def run_analysis():
    """Run the content analysis."""
    logger.info("Running content analysis...")
    
    # Import and run the analysis module
    try:
        sys.path.append('src')
        from analytics.run_analysis import run_analysis
        run_analysis()
        logger.info("Analysis completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running analysis: {str(e)}")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard."""
    logger.info("Launching dashboard...")
    
    # Get the port from the environment or use default
    port = int(os.environ.get("PORT", 8501))
    
    # Run the dashboard app
    try:
        os.system(f"python dashboard_app.py")
        return True
    except Exception as e:
        logger.error(f"Error launching dashboard: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting analytics and dashboard")
    
    # Create necessary directories
    Path("analysis").mkdir(exist_ok=True)
    
    # Run analysis first
    analysis_success = run_analysis()
    
    # Launch dashboard if analysis was successful
    if analysis_success:
        launch_dashboard()
    else:
        logger.warning("Launching dashboard with potentially outdated analysis results")
        launch_dashboard() 