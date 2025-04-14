import os
import anthropic
from dotenv import load_dotenv
import time

# Wait a moment for server to fully start
time.sleep(1)

# Load environment variables fresh
load_dotenv(override=True)

# Get API key
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API key found: {'Yes' if api_key else 'No'}")
print(f"API key format: {'Valid' if api_key and api_key.startswith('sk-ant-api') else 'Invalid'}")
print(f"API key length: {len(api_key) if api_key else 0} characters")

try:
    print("\nTesting with Anthropic API...")
    client = anthropic.Anthropic(api_key=api_key)
    
    # First try listing models
    try:
        models = client.models.list()
        print("✅ Authentication successful!")
        print("Available models:")
        for model in models.models:
            print(f"- {model.id}")
    except Exception as e:
        print(f"❌ Error listing models: {str(e)}")
    
    # Try a simple message
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print("\n✅ Message generation successful!")
        print(f"Response: {message.content[0].text}")
    except Exception as e:
        print(f"❌ Error generating message: {str(e)}")
        
except Exception as e:
    print(f"❌ Error initializing client: {str(e)}") 