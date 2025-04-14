import anthropic
import requests

# Test API key - replace this with your actual key when running
API_KEY = "YOUR_API_KEY_HERE"  # Change this to your actual key before running

print("Testing API key:", "sk-ant-api**************" + API_KEY[-6:])

# First try a simple API v1 authentication check
try:
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }
    response = requests.get(
        "https://api.anthropic.com/v1/models",
        headers=headers
    )
    if response.status_code == 200:
        print("✅ API key authenticated successfully with simple models API")
        print("Available models:", [m["id"] for m in response.json()["models"]])
    else:
        print(f"❌ API authentication failed: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Error with direct request: {str(e)}")

# Try with the Anthropic client 
try:
    client = anthropic.Anthropic(api_key=API_KEY)
    
    # List available models
    models = client.models.list()
    print("\nModels available with your API key:")
    for model in models.models:
        print(f"- {model.id}")
        
    # Send a simple message
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print("\nResponse received from Claude:")
    print(message.content[0].text)
except Exception as e:
    print(f"❌ Error with Anthropic client: {str(e)}") 