from src.models.model_interface import ModelInterface
from src.utils.brand_knowledge import brand_knowledge

def main():
    # Initialize the model interface
    model = ModelInterface()
    
    # Print brand brief info
    print(f"Loaded brand brief for: {brand_knowledge.get_company_info().get('name', 'Unknown')}")
    print(f"Key messages: {len(brand_knowledge.get_key_messages())} loaded")
    print()
    
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
    print("\nAnalyzing content...")
    analysis = model.analyze_content(content, "text")
    
    # Print analysis
    print("Content analysis:")
    print("-" * 50)
    print(analysis)
    print("-" * 50)

if __name__ == "__main__":
    main() 