import os
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API key found: {'Yes' if api_key else 'No'}")
print(f"API key format check: {'Correct format - starts with sk-ant-api' if api_key and api_key.startswith('sk-ant-api') else 'WRONG FORMAT'}")
print(f"API key length: {len(api_key) if api_key else 'N/A'} characters")

# Create client - simplest version
client = anthropic.Anthropic(api_key=api_key)

# Send a simple message
try:
    message = client.messages.create(
        model="claude-3-haiku-20240307",  # Using the latest model that's less likely to be deprecated
        max_tokens=300,
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print("\nResponse from Claude:")
    print(message.content[0].text)
    print("\nAPI key is working correctly!")
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc() 