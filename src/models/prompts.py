from typing import Dict, Optional

class PromptTemplates:
    """Collection of prompt templates for different content types and purposes."""
    
    @staticmethod
    def get_text_post_template(context: Optional[Dict] = None) -> str:
        """Template for generating text-only LinkedIn posts using authentic examples and brand brief."""
        safe_context = context or {}
        defaults = {
            "industry": "Leadership Development",
            "target_audience": "Business professionals",
            "purpose": "Thought leadership",
            "tone": "Professional",
            "topic": "Leadership",
            "cta_type": "Ask a question",
            "authentic_examples": [],
            "brand_mission": "",
            "brand_voice": "",
            "key_message": ""
        }
        for key, value in defaults.items():
            if key not in safe_context or not safe_context[key]:
                safe_context[key] = value

        # Prepare authentic examples (few-shot)
        example_section = ""
        if safe_context["authentic_examples"]:
            example_section = "Here are two examples of my authentic LinkedIn posts:\n---\n"
            for ex in safe_context["authentic_examples"][:2]:
                example_section += ex + "\n---\n"

        base_template = f"""
        {example_section}
        Using the same style, tone, and structure as the examples above, write a new LinkedIn post about: {{topic}}
        - Use a {{tone}} tone
        - Speak directly to {{target_audience}}
        - Reference our brand's mission: {{brand_mission}}
        - Key message: {{key_message}}
        - Incorporate our brand voice: {{brand_voice}}
        - Use formatting and structure similar to the examples
        - Make it authentic, specific, and aligned with our brand
        - End with a relevant call-to-action: {{cta_type}}
        """
        try:
            return base_template.format(**safe_context)
        except KeyError as e:
            return f"Error in template formatting: Missing key {e}"
    
    @staticmethod
    def get_media_post_template(context: Optional[Dict] = None) -> str:
        """Template for generating LinkedIn posts with media."""
        # Provide default values for missing context
        safe_context = context or {}
        defaults = {
            "industry": "Leadership Development",
            "media_type": "Image",
            "target_audience": "Business professionals",
            "purpose": "Thought leadership",
            "tone": "Professional",
            "topic": "Leadership",
            "cta_type": "Ask a question"
        }
        
        # Merge defaults with provided context
        for key, value in defaults.items():
            if key not in safe_context or not safe_context[key]:
                safe_context[key] = value
        
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
        
        try:
            return base_template.format(**safe_context)
        except KeyError as e:
            return f"Error in template formatting: Missing key {e}"
    
    @staticmethod
    def get_article_template(context: Optional[Dict] = None) -> str:
        """Template for generating LinkedIn articles."""
        # Provide default values for missing context
        safe_context = context or {}
        defaults = {
            "industry": "Leadership Development",
            "target_audience": "Business professionals",
            "purpose": "Thought leadership",
            "tone": "Professional",
            "topic": "Leadership",
            "key_points": ["Point 1", "Point 2", "Point 3"]
        }
        
        # Merge defaults with provided context
        for key, value in defaults.items():
            if key not in safe_context or not safe_context[key]:
                safe_context[key] = value
        
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
        
        try:
            return base_template.format(**safe_context)
        except KeyError as e:
            return f"Error in template formatting: Missing key {e}"
    
    @staticmethod
    def get_optimization_template(context: Optional[Dict] = None) -> str:
        """Template for optimizing existing content."""
        # Provide default values for missing context
        safe_context = context or {}
        defaults = {
            "content": "This is a sample content that needs optimization.",
            "target_metrics": ["engagement", "readability"],
            "industry": "Leadership Development",
            "target_audience": "Business professionals"
        }
        
        # Merge defaults with provided context
        for key, value in defaults.items():
            if key not in safe_context or not safe_context[key]:
                safe_context[key] = value
        
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
        
        try:
            return base_template.format(**safe_context)
        except KeyError as e:
            return f"Error in template formatting: Missing key {e}"
    
    @staticmethod
    def get_analysis_template(context: Optional[Dict] = None) -> str:
        """Template for analyzing content performance."""
        # Provide default values for missing context
        safe_context = context or {}
        defaults = {
            "content": "This is a sample content that needs analysis.",
            "content_type": "text",
            "industry": "Leadership Development",
            "target_audience": "Business professionals"
        }
        
        # Merge defaults with provided context
        for key, value in defaults.items():
            if key not in safe_context or not safe_context[key]:
                safe_context[key] = value
        
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
        
        try:
            return base_template.format(**safe_context)
        except KeyError as e:
            return f"Error in template formatting: Missing key {e}" 