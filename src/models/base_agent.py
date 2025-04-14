from typing import Dict, List, Optional
import logging
from abc import ABC, abstractmethod
from src.utils.brand_knowledge import brand_knowledge

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
        # First enrich context with brand knowledge
        enriched_context = context or {}
        
        # Check if brand_knowledge is available and properly initialized
        if 'brand_knowledge' in globals() and brand_knowledge is not None and hasattr(brand_knowledge, 'get_full_brief'):
            try:
                if brand_knowledge.get_full_brief():
                    enriched_context = brand_knowledge.enrich_context(enriched_context)
                    
                    # Add brand guidance to the prompt
                    if not "BRAND GUIDANCE:" in base_prompt:
                        base_prompt = brand_knowledge.format_brand_prompt(base_prompt)
            except Exception as e:
                self.logger.error(f"Error applying brand knowledge: {str(e)}")
            
        if context is None:
            return base_prompt
            
        try:
            return base_prompt.format(**enriched_context)
        except KeyError as e:
            self.logger.error(f"Missing context key: {e}")
            return base_prompt 