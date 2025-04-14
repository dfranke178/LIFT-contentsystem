import json
import os
from pathlib import Path
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrandKnowledge:
    """Loads and provides brand knowledge for content generation."""
    
    def __init__(self, brand_brief_path: str = None):
        """
        Initialize the brand knowledge provider.
        
        Args:
            brand_brief_path (str, optional): Path to the brand brief JSON file.
                Defaults to 'brand_knowledge/brand_brief.json'.
        """
        self.brand_brief_path = brand_brief_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'brand_knowledge', 'brand_brief.json'
        )
        self.brand_brief = self._load_brand_brief()
        
    def _load_brand_brief(self) -> Dict[str, Any]:
        """Load the brand brief from the JSON file."""
        try:
            if os.path.exists(self.brand_brief_path):
                with open(self.brand_brief_path, 'r') as f:
                    brand_brief = json.load(f)
                logger.info(f"Successfully loaded brand brief from {self.brand_brief_path}")
                return brand_brief
            else:
                logger.warning(f"Brand brief file not found at {self.brand_brief_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading brand brief: {str(e)}")
            return {}
    
    def get_full_brief(self) -> Dict[str, Any]:
        """Get the complete brand brief."""
        return self.brand_brief
    
    def get_company_info(self) -> Dict[str, Any]:
        """Get company information from the brand brief."""
        return self.brand_brief.get('company_info', {})
    
    def get_brand_voice(self) -> Dict[str, Any]:
        """Get brand voice guidelines from the brand brief."""
        return self.brand_brief.get('brand_voice', {})
    
    def get_target_audience(self) -> Dict[str, Any]:
        """Get target audience information from the brand brief."""
        return self.brand_brief.get('target_audience', {})
    
    def get_key_messages(self) -> list:
        """Get key messages from the brand brief."""
        return self.brand_brief.get('key_messages', [])
    
    def get_content_strategy(self) -> Dict[str, Any]:
        """Get content strategy from the brand brief."""
        return self.brand_brief.get('content_strategy', {})
    
    def get_visual_identity(self) -> Dict[str, Any]:
        """Get visual identity guidelines from the brand brief."""
        return self.brand_brief.get('visual_identity', {})
    
    def get_values(self) -> list:
        """Get company values from the brand brief."""
        return self.brand_brief.get('values', [])
    
    def get_unique_selling_points(self) -> list:
        """Get unique selling points from the brand brief."""
        return self.brand_brief.get('unique_selling_points', [])
    
    def enrich_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich the content generation context with brand information.
        
        Args:
            context (Dict[str, Any]): Original context for content generation
            
        Returns:
            Dict[str, Any]: Enriched context with brand information
        """
        enriched = context.copy()
        
        # Add brand knowledge to context
        enriched['brand'] = {
            'company_name': self.brand_brief.get('company_info', {}).get('name', ''),
            'tagline': self.brand_brief.get('company_info', {}).get('tagline', ''),
            'voice': self.brand_brief.get('brand_voice', {}).get('tone', ''),
            'primary_audience': self.brand_brief.get('target_audience', {}).get('primary', ''),
            'key_messages': self.brand_brief.get('key_messages', []),
            'values': self.brand_brief.get('values', []),
            'unique_selling_points': self.brand_brief.get('unique_selling_points', [])
        }
        
        # Add audience pain points and goals
        enriched['audience'] = {
            'primary': self.brand_brief.get('target_audience', {}).get('primary', ''),
            'pain_points': self.brand_brief.get('target_audience', {}).get('pain_points', []),
            'goals': self.brand_brief.get('target_audience', {}).get('goals', [])
        }
        
        # Add content strategy elements
        if not enriched.get('industry'):
            enriched['industry'] = 'Leadership Development'
            
        if not enriched.get('tone'):
            enriched['tone'] = self.brand_brief.get('brand_voice', {}).get('tone', '')
            
        if not enriched.get('hashtags'):
            enriched['hashtags'] = self.brand_brief.get('content_strategy', {}).get('engagement', {}).get('hashtags', [])
            
        return enriched
    
    def format_brand_prompt(self, base_prompt: str) -> str:
        """
        Format a prompt with brand information.
        
        Args:
            base_prompt (str): Base prompt template
            
        Returns:
            str: Prompt enriched with brand information
        """
        # Extract core brand information
        company_name = self.brand_brief.get('company_info', {}).get('name', '')
        tagline = self.brand_brief.get('company_info', {}).get('tagline', '')
        voice = self.brand_brief.get('brand_voice', {}).get('tone', '')
        audience = self.brand_brief.get('target_audience', {}).get('primary', '')
        
        # Create brand guidance section
        brand_guidance = f"""
        BRAND GUIDANCE:
        Company: {company_name}
        Tagline: {tagline}
        Voice: {voice}
        Primary Audience: {audience}
        
        Key Messages:
        {self._format_list(self.brand_brief.get('key_messages', []))}
        
        Values:
        {self._format_list(self.brand_brief.get('values', []))}
        
        Unique Selling Points:
        {self._format_list(self.brand_brief.get('unique_selling_points', []))}
        
        Audience Pain Points:
        {self._format_list(self.brand_brief.get('target_audience', {}).get('pain_points', []))}
        
        Audience Goals:
        {self._format_list(self.brand_brief.get('target_audience', {}).get('goals', []))}
        """
        
        # Add brand guidance to the prompt
        enriched_prompt = f"{base_prompt}\n\n{brand_guidance}"
        return enriched_prompt
    
    def _format_list(self, items: list) -> str:
        """Format a list of items as a bulleted string."""
        if not items:
            return "None specified"
        return "\n".join([f"- {item}" for item in items])


# Singleton instance for easy import
brand_knowledge = BrandKnowledge() 