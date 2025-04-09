import os
import json
import csv
from typing import Any, Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_posts_for_training() -> List[Dict[str, Any]]:
    """
    Fetch and prepare posts for training the AI model from the data file.
    """
    try:
        # Get the path to the data file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.join(current_dir, 'data')
        
        training_examples = []
        
        # Read the CSV data
        with open(data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows
                if not any(row.values()):
                    continue
                    
                # Create training example
                example = {
                    "content": row.get('POST_TEXT', ''),
                    "metadata": {
                        "post_id": row.get('POST_ID', ''),
                        "likes": int(row.get('LIKES', 0)),
                        "comments": int(row.get('COMMENTS', 0)),
                        "shares": int(row.get('SHARES', 0)),
                        "date": row.get('DATE', ''),
                        "content_type": row.get('CONTENT_TYPE', ''),
                        "industry": row.get('INDUSTRY', ''),
                        "post_length": row.get('POST_LENGTH', ''),
                        "purpose": row.get('PURPOSE', ''),
                        "tone": row.get('TONE', ''),
                        "topic": row.get('TOPIC', ''),
                        "cta_type": row.get('CTA_TYPE', ''),
                        "hashtags": row.get('HASHTAGS', ''),
                        "engagement_rate": float(row.get('ENGAGEMENT_RATE', 0)),
                        "account_size": row.get('ACCOUNT_SIZE', ''),
                        "success_rating": row.get('SUCCESS_RATING', '')
                    }
                }
                training_examples.append(example)
        
        logger.info(f"Successfully fetched {len(training_examples)} training examples from data file")
        return training_examples
    except Exception as e:
        logger.error(f"Error fetching training examples: {str(e)}")
        raise

def save_json(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Successfully saved data to {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON: {str(e)}")
        raise

def load_json(file_path: str) -> Dict[str, Any]:
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {file_path}")
        return data
    except Exception as e:
        logger.error(f"Error loading JSON: {str(e)}")
        raise

def create_timestamp() -> str:
    """Create a formatted timestamp."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def ensure_directory(directory_path: str) -> None:
    """Ensure a directory exists, create it if it doesn't."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.info(f"Directory ensured: {directory_path}")
    except Exception as e:
        logger.error(f"Error creating directory: {str(e)}")
        raise 