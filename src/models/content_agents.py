from typing import Dict, Optional
from .base_agent import BaseAgent
import anthropic

class TextContentAgent(BaseAgent):
    """Agent specialized in generating text-only LinkedIn posts."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        self.client = anthropic.Anthropic()
        
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        formatted_prompt = self.format_prompt(prompt, context)
        
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
    
    def analyze_content(self, content: str) -> Dict:
        analysis_prompt = f"""
        Analyze this LinkedIn post for the following metrics:
        1. Engagement potential
        2. Clarity and readability
        3. Professional tone
        4. Value proposition
        5. Call-to-action effectiveness
        
        Post: {content}
        """
        
        analysis = self.generate_content(analysis_prompt)
        return {"analysis": analysis}

class MediaContentAgent(BaseAgent):
    """Agent specialized in generating posts with media (images, videos)."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        self.client = anthropic.Anthropic()
        
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        formatted_prompt = self.format_prompt(prompt, context)
        
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
    
    def analyze_content(self, content: str) -> Dict:
        analysis_prompt = f"""
        Analyze this LinkedIn post with media for the following metrics:
        1. Media relevance and quality
        2. Caption effectiveness
        3. Visual storytelling
        4. Engagement potential
        5. Brand consistency
        
        Post: {content}
        """
        
        analysis = self.generate_content(analysis_prompt)
        return {"analysis": analysis}

class ArticleContentAgent(BaseAgent):
    """Agent specialized in generating long-form articles and thought leadership pieces."""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", temperature: float = 0.7):
        super().__init__(model_name, temperature)
        self.client = anthropic.Anthropic()
        
    def generate_content(self, prompt: str, context: Optional[Dict] = None) -> str:
        formatted_prompt = self.format_prompt(prompt, context)
        
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
    
    def analyze_content(self, content: str) -> Dict:
        analysis_prompt = f"""
        Analyze this LinkedIn article for the following metrics:
        1. Depth of insight
        2. Structure and flow
        3. Research quality
        4. Thought leadership value
        5. Engagement potential
        
        Article: {content}
        """
        
        analysis = self.generate_content(analysis_prompt)
        return {"analysis": analysis} 