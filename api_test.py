import anthropic
import os
from dotenv import load_dotenv

# Add debug print statements
print("Starting API test script...")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.environ.get("ANTHROPIC_API_KEY")
print(f"API Key found: {'Yes' if api_key else 'No'}")

# Add some error handling
if not api_key:
    print("ERROR: No API key found in .env file. Please check your .env file.")
    print("Current directory:", os.getcwd())
    print("Files in directory:", os.listdir())
    exit(1)

try:
    # Create the client using the API key from environment
    print("Creating Anthropic client...")
    client = anthropic.Anthropic(api_key=api_key)
    
    print("Sending message to Claude...")
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0.5,
        system="You are a helpful assistant.",
        messages=[
            {"role": "user", "content": "Hello, Claude! Please confirm this API key is working."}
        ]
    )
    
    print("\n--- Response received. Content: ---")
    print(message.content[0].text)
    print("--- End of response ---\n")
    
    print("API key is working correctly!")
    
except Exception as e:
    print(f"\nAn error occurred: {e}")
    import traceback
    traceback.print_exc()

print("Script execution complete.")