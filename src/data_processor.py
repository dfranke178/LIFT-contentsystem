import json
import os
from src.utils.data_utils import get_posts_for_training
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prepare_training_data():
    """
    Prepare training data for fine-tuning an AI model
    """
    try:
        # Get the training examples
        logger.info("Fetching training examples...")
        training_examples = get_posts_for_training()
        
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Created output directory: {output_dir}")
        
        # Save the training examples as a JSON file
        output_path = os.path.join(output_dir, 'training_data.json')
        with open(output_path, 'w') as f:
            json.dump(training_examples, f, indent=2)
        
        logger.info(f"Saved {len(training_examples)} training examples to {output_path}")
        if training_examples:
            logger.info(f"Sample example: {training_examples[0]}")
        
        return output_path
    except Exception as e:
        logger.error(f"Error preparing training data: {str(e)}")
        raise

if __name__ == "__main__":
    prepare_training_data()

class DataProcessor:
    """Process LinkedIn post data for analysis"""
    def __init__(self):
        pass 