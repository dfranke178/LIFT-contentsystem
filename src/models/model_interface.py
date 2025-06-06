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
        agent = self.get_agent(content_type)
        required_fields = self._get_required_fields(content_type)
        missing_fields = [field for field in required_fields if field not in context]
        if missing_fields:
            error_message = f"Missing required context fields: {', '.join(missing_fields)}"
            self.logger.error(error_message)
            return f"Error: {error_message}"

        # --- ENHANCEMENT: Add relevant authentic post examples and brand brief fields ---
        if content_type == "text":
            try:
                from src.utils.retrieval import retrieve_relevant_posts
                try:
                    # Use semantic retrieval for most relevant examples
                    authentic_examples = retrieve_relevant_posts(context.get("topic", ""), top_k=2)
                except ImportError:
                    # Fallback to keyword matching if sentence-transformers not available
                    import json
                    with open("data_store/authentic_posts.json", "r", encoding="utf-8") as f:
                        authentic_data = json.load(f)
                    topic = context.get("topic", "").lower()
                    def score(post):
                        content = post.get("content", "").lower()
                        meta_topic = post.get("metadata", {}).get("topic", "").lower()
                        return int(topic in content or topic in meta_topic)
                    sorted_posts = sorted(authentic_data.get("authentic_posts", []), key=score, reverse=True)
                    authentic_examples = [p["content"] for p in sorted_posts if p.get("content")] [:2]
            except Exception as e:
                authentic_examples = []
                self.logger.error(f"Could not load authentic post examples: {e}")
            from src.utils.brand_knowledge import brand_knowledge
            brand_brief = brand_knowledge.get_full_brief() if hasattr(brand_knowledge, 'get_full_brief') else {}
            context = context.copy()
            context["authentic_examples"] = authentic_examples
            context["brand_mission"] = brand_brief.get("company_overview", {}).get("mission", "")
            context["brand_voice"] = brand_brief.get("voice_and_tone", {})
            context["key_message"] = context.get("key_message", "")
            # Set higher temperature for more creative outputs
            if hasattr(agent, 'temperature'):
                agent.temperature = 0.9
            base_prompt = self.prompts.get_text_post_template(context)
            print("=== PROMPT SENT TO MODEL ===\n", base_prompt)
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