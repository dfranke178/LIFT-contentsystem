from typing import Dict, Optional
from .base_agent import BaseAgent
import os
import logging
from dotenv import load_dotenv

# Load environment variables at module level
load_dotenv()

# Try to import anthropic, but don't fail if it's not available
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("Anthropic package not available. Using fallback mode.")

class TextContentAgent(BaseAgent):
    """Agent specialized in generating text-only LinkedIn posts."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        # Get API key from environment variables
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            self.logger.warning("ANTHROPIC_API_KEY not found in environment variables. API calls will fail.")
        
        if ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            self.logger.warning("Anthropic client not initialized - package missing")
        
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        formatted_prompt = self.format_prompt(prompt, context)
        
        if not ANTHROPIC_AVAILABLE:
            self.logger.error("Cannot generate content: Anthropic package not available")
            return "Error: Anthropic package not available. Please install it with 'pip install anthropic'."
        
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            self.logger.error(f"Error generating content with Anthropic API: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def analyze_content(self, content: str) -> Dict:
        """Simple analysis without external dependencies."""
        return {
            "analysis": "Content analysis available without external libraries. Install additional dependencies for comprehensive analysis."
        }

class MediaContentAgent(BaseAgent):
    """Agent specialized in generating posts with media (images, videos)."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        # Get API key from environment variables
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            self.logger.warning("ANTHROPIC_API_KEY not found in environment variables. API calls will fail.")
        
        if ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            self.logger.warning("Anthropic client not initialized - package missing")
        
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        formatted_prompt = self.format_prompt(prompt, context)
        
        if not ANTHROPIC_AVAILABLE:
            self.logger.error("Cannot generate content: Anthropic package not available")
            return "Error: Anthropic package not available. Please install it with 'pip install anthropic'."
        
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            self.logger.error(f"Error generating content with Anthropic API: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def analyze_content(self, content: str) -> Dict:
        """Simple analysis without external dependencies."""
        return {
            "analysis": "Content analysis available without external libraries. Install additional dependencies for comprehensive analysis."
        }

class ArticleContentAgent(BaseAgent):
    """Agent specialized in generating long-form articles and thought leadership pieces."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        # Get API key from environment variables
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            self.logger.warning("ANTHROPIC_API_KEY not found in environment variables. API calls will fail.")
        
        if ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
            self.logger.warning("Anthropic client not initialized - package missing")
        
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        formatted_prompt = self.format_prompt(prompt, context)
        
        if not ANTHROPIC_AVAILABLE:
            self.logger.error("Cannot generate content: Anthropic package not available")
            return "Error: Anthropic package not available. Please install it with 'pip install anthropic'."
        
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                temperature=self.temperature,
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt
                    }
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            self.logger.error(f"Error generating content with Anthropic API: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def analyze_content(self, content: str) -> Dict:
        """Simple analysis without external dependencies."""
        return {
            "analysis": "Content analysis available without external libraries. Install additional dependencies for comprehensive analysis."
        } 