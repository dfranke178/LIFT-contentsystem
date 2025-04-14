from src.models.model_interface import ModelInterface
from src.utils.brand_knowledge import brand_knowledge
import os
import sys
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for required environment variables
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable is not set.")
        print("Please check that your .env file contains the API key.")
        sys.exit(1)
    
    # Initialize the model interface
    model = ModelInterface()
    
    # Print brand brief info
    print(f"Loaded brand brief for: {brand_knowledge.get_company_info().get('name', 'Unknown')}")
    print(f"Key messages: {len(brand_knowledge.get_key_messages())} loaded")
    print()
    
    try:
        # Generate a LinkedIn post using brand knowledge
        context = {
            "content_type": "text",
            "topic": "leadership clarity",
            "purpose": "thought leadership",
            "cta_type": "Ask a question",
        }
        
        print("Generating LinkedIn post with brand knowledge...\n")
        
        content = model.generate_content("text", context)
        
        print("Generated post:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        
        # Analyze the generated content
        print("\nContent analysis available in simplified mode.")
        
    except Exception as e:
        logger.error(f"Error in content generation: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 