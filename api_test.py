import anthropic
import os
from dotenv import load_dotenv

# Add debug print statements
print("Starting API test script...")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("ANTHROPIC_API_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No - Key not found'}")

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
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=0.5,
        system="You are a helpful assistant.",
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    
    print("Response received. Content:")
    print(message.content)
    
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()

print("Script execution complete.")