from typing import Dict, Optional, Union
from .base_agent import BaseAgent
from .content_agents import TextContentAgent, MediaContentAgent, ArticleContentAgent
from .prompts import PromptTemplates
from utils.evaluation import ContentEvaluator
from utils.prompt_tuning import PromptTuner

class ModelInterface:
    """Main interface for coordinating between different agents and prompts."""
    
    def __init__(self):
        self.agents = {
            "text": TextContentAgent(),
            "media": MediaContentAgent(),
            "article": ArticleContentAgent()
        }
        self.prompts = PromptTemplates()
        self.evaluator = ContentEvaluator()
        self.tuner = PromptTuner()
    
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
        agent = self.get_agent(content_type)
        
        # Get the appropriate prompt template
        if content_type == "text":
            base_prompt = self.prompts.get_text_post_template(context)
        elif content_type == "media":
            base_prompt = self.prompts.get_media_post_template(context)
        else:  # article
            base_prompt = self.prompts.get_article_template(context)
        
        # Adapt the prompt using few-shot learning
        adapted_prompt = self.tuner.adapt_prompt(base_prompt, content_type)
        
        # Generate content
        content = agent.generate_content(adapted_prompt, context)
        
        # Evaluate the generated content
        metrics = self.evaluator.evaluate_content(content, content_type)
        
        # Store the example if it meets quality thresholds
        if all(score >= 0.8 for score in metrics.values()):
            self.tuner.add_example(content, content_type, metrics, context)
        
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
        
        # Adapt the prompt using few-shot learning
        adapted_prompt = self.tuner.adapt_prompt(base_prompt, "text")
        
        return agent.generate_content(adapted_prompt, context)
    
    def get_content_analysis(self, content: str, content_type: str, context: Dict) -> Dict:
        """
        Get detailed analysis of content.
        
        Args:
            content (str): Content to analyze
            content_type (str): Type of content
            context (Dict): Analysis context
            
        Returns:
            Dict: Analysis results
        """
        agent = self.get_agent(content_type)
        base_prompt = self.prompts.get_analysis_template({
            "content": content,
            "content_type": content_type,
            **context
        })
        
        # Adapt the prompt using few-shot learning
        adapted_prompt = self.tuner.adapt_prompt(base_prompt, content_type)
        
        return agent.generate_content(adapted_prompt, context)
    
    def add_feedback(self, content: str, content_type: str, feedback: Dict) -> None:
        """
        Add feedback for content improvement.
        
        Args:
            content (str): The content being evaluated
            content_type (str): Type of content
            feedback (Dict): User or system feedback
        """
        # Get current metrics
        metrics = self.evaluator.evaluate_content(content, content_type)
        
        # Add feedback to evaluator
        self.evaluator.add_feedback(content, content_type, feedback, metrics)
        
        # Update prompt templates based on feedback
        self.tuner.update_prompt_templates(content_type, {
            "feedback": feedback,
            "metrics": metrics
        }) 