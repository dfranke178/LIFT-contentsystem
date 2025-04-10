from typing import Dict, List, Optional
import logging
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Base class for all AI agents in the LIFT system."""
    
    def __init__(self, model_name: str, temperature: float = 0.7):
        """
        Initialize the base agent.
        
        Args:
            model_name (str): Name of the model to use
            temperature (float): Temperature for generation (0.0 to 1.0)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        
    @abstractmethod
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Generate content based on the prompt and context.
        
        Args:
            prompt (str): The input prompt
            context (Optional[Dict]): Additional context for generation
            
        Returns:
            str: Generated content
        """
        pass
    
    @abstractmethod
    def analyze_content(self, content: str) -> Dict:
        """
        Analyze the given content.
        
        Args:
            content (str): Content to analyze
            
        Returns:
            Dict: Analysis results
        """
        pass
    
    def format_prompt(self, base_prompt: str, context: Optional[Dict] = None) -> str:
        """
        Format the prompt with context.
        
        Args:
            base_prompt (str): Base prompt template
            context (Optional[Dict]): Context to include in prompt
            
        Returns:
            str: Formatted prompt
        """
        if context is None:
            return base_prompt
            
        try:
            return base_prompt.format(**context)
        except KeyError as e:
            self.logger.error(f"Missing context key: {e}")
            return base_prompt 