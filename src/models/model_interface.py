from typing import Dict, Optional, Union
from .base_agent import BaseAgent
from .content_agents import TextContentAgent, MediaContentAgent, ArticleContentAgent
from .prompts import PromptTemplates
import logging

class ModelInterface:
    """Main interface for coordinating between different agents and prompts."""
    
    def __init__(self):
        self.agents = {
            "text": TextContentAgent(),
            "media": MediaContentAgent(),
            "article": ArticleContentAgent()
        }
        self.prompts = PromptTemplates()
        self.logger = logging.getLogger(__name__)
    
    def get_agent(self, content_type: str) -> BaseAgent:
        """Get the appropriate agent for the content type."""
        if content_type not in self.agents:
            raise ValueError(f"Unsupported content type: {content_type}")
        return self.agents[content_type]
    
    def generate_content(self, content_type: str, context: Dict) -> str:
        """
        Generate content using the appropriate agent and prompt template.
        
        Args:
            content_type (str): Type of content to generate ("text", "media", or "article")
            context (Dict): Context for content generation
            
        Returns:
            str: Generated content
        """
        # Validate content type
        agent = self.get_agent(content_type)
        
        # Validate required context fields
        required_fields = self._get_required_fields(content_type)
        missing_fields = [field for field in required_fields if field not in context]
        
        if missing_fields:
            error_message = f"Missing required context fields: {', '.join(missing_fields)}"
            self.logger.error(error_message)
            return f"Error: {error_message}"
        
        # Get the appropriate prompt template
        if content_type == "text":
            base_prompt = self.prompts.get_text_post_template(context)
        elif content_type == "media":
            base_prompt = self.prompts.get_media_post_template(context)
        else:  # article
            base_prompt = self.prompts.get_article_template(context)
        
        # Generate content
        content = agent.generate_content(base_prompt, context)
        
        return content
    
    def analyze_content(self, content: str, content_type: str) -> Dict:
        """
        Analyze content using the appropriate agent.
        
        Args:
            content (str): Content to analyze
            content_type (str): Type of content ("text", "media", or "article")
            
        Returns:
            Dict: Analysis results
        """
        agent = self.get_agent(content_type)
        return agent.analyze_content(content)
    
    def optimize_content(self, content: str, context: Dict) -> str:
        """
        Optimize existing content.
        
        Args:
            content (str): Content to optimize
            context (Dict): Optimization context
            
        Returns:
            str: Optimized content
        """
        # Use the text agent for optimization as it's most versatile
        agent = self.get_agent("text")
        base_prompt = self.prompts.get_optimization_template({
            "content": content,
            **context
        })
        
        return agent.generate_content(base_prompt, context)
    
    def _get_required_fields(self, content_type: str) -> list:
        """Get required context fields for a specific content type."""
        common_fields = ["topic", "purpose"]
        
        if content_type == "text":
            return common_fields + ["cta_type"]
        elif content_type == "media":
            return common_fields + ["media_type"]
        elif content_type == "article":
            return common_fields + ["key_points"]
        
        return common_fields 