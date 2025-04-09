"""
LinkedIn Content Analysis System
"""

# Version information
__version__ = "1.0.0"

# Make classes available for import
from src.data_processor import DataProcessor
from src.utils import save_json, create_timestamp
from src.utils.feedback_loop import FeedbackLoop

__all__ = ['DataProcessor', 'save_json', 'create_timestamp', 'FeedbackLoop']