"""
LinkedIn Content Analysis System
"""

import os
import sys

# Only import data processor if not running tests
if not any(arg.endswith('pytest') for arg in sys.argv):
    from src.data_processor import DataProcessor

# Version information
__version__ = "1.0.0"

# Make functions available for import
from src.utils import save_json, create_timestamp, get_posts_for_training
from src.utils.feedback_loop import FeedbackLoop

__all__ = ['DataProcessor', 'save_json', 'create_timestamp', 'FeedbackLoop']