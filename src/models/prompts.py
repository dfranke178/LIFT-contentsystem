from typing import Dict, Optional

class PromptTemplates:
    """Collection of prompt templates for different content types and purposes."""
    
    @staticmethod
    def get_text_post_template(context: Optional[Dict] = None) -> str:
        """Template for generating text-only LinkedIn posts."""
        base_template = """
        You are an expert LinkedIn content creator. Create a professional LinkedIn post with the following specifications:
        
        Industry: {industry}
        Target Audience: {target_audience}
        Post Purpose: {purpose}
        Desired Tone: {tone}
        Key Topic: {topic}
        Call-to-Action: {cta_type}
        
        The post should be:
        - Professional and engaging
        - Clear and concise
        - Value-driven
        - Include relevant hashtags
        - Optimized for LinkedIn's algorithm
        
        Generate a post that follows these guidelines.
        """
        return base_template.format(**(context or {}))
    
    @staticmethod
    def get_media_post_template(context: Optional[Dict] = None) -> str:
        """Template for generating LinkedIn posts with media."""
        base_template = """
        You are an expert LinkedIn content creator specializing in visual content. Create a LinkedIn post with media using these specifications:
        
        Industry: {industry}
        Media Type: {media_type}
        Target Audience: {target_audience}
        Post Purpose: {purpose}
        Desired Tone: {tone}
        Key Topic: {topic}
        Call-to-Action: {cta_type}
        
        The post should include:
        - A compelling caption
        - Description of the visual content
        - Clear value proposition
        - Relevant hashtags
        - Optimized for LinkedIn's algorithm
        
        Generate a post that effectively combines text and visual elements.
        """
        return base_template.format(**(context or {}))
    
    @staticmethod
    def get_article_template(context: Optional[Dict] = None) -> str:
        """Template for generating LinkedIn articles."""
        base_template = """
        You are an expert LinkedIn thought leader. Create a comprehensive LinkedIn article with these specifications:
        
        Industry: {industry}
        Target Audience: {target_audience}
        Article Purpose: {purpose}
        Desired Tone: {tone}
        Main Topic: {topic}
        Key Points: {key_points}
        
        The article should:
        - Provide deep insights
        - Be well-structured
        - Include data and examples
        - Offer actionable takeaways
        - Maintain professional tone
        - Be optimized for LinkedIn's algorithm
        
        Generate a thought-provoking article that establishes authority in the field.
        """
        return base_template.format(**(context or {}))
    
    @staticmethod
    def get_optimization_template(context: Optional[Dict] = None) -> str:
        """Template for optimizing existing content."""
        base_template = """
        You are a LinkedIn content optimization expert. Review and enhance this content:
        
        Original Content: {content}
        Target Metrics: {target_metrics}
        Industry: {industry}
        Audience: {target_audience}
        
        Optimize the content for:
        - Higher engagement
        - Better readability
        - Improved SEO
        - Stronger call-to-action
        - Better alignment with LinkedIn's algorithm
        
        Provide the optimized version of the content.
        """
        return base_template.format(**(context or {}))
    
    @staticmethod
    def get_analysis_template(context: Optional[Dict] = None) -> str:
        """Template for analyzing content performance."""
        base_template = """
        Analyze this LinkedIn content for performance potential:
        
        Content: {content}
        Content Type: {content_type}
        Industry: {industry}
        Target Audience: {target_audience}
        
        Evaluate:
        - Engagement potential
        - Professional tone
        - Value proposition
        - Call-to-action effectiveness
        - Algorithm optimization
        - Areas for improvement
        
        Provide a detailed analysis with specific recommendations.
        """
        return base_template.format(**(context or {})) 