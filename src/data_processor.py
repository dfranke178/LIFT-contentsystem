import json
import os
from src.utils.data_utils import get_posts_for_training
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prepare_training_data():
    """Prepare training data for the model"""
    try:
        posts = get_posts_for_training()
        logger.info(f"Retrieved {len(posts)} posts for training")
        return posts
    except Exception as e:
        logger.error(f"Error preparing training data: {str(e)}")
        raise

if __name__ == "__main__":
    prepare_training_data()

class DataProcessor:
    """Class for processing and preparing data"""
    
    def __init__(self):
        """Initialize the data processor"""
        pass 