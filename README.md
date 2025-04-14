# LIFT Leadership AI Content System

A comprehensive AI system for generating LinkedIn content that incorporates brand knowledge and follows LIFT Leadership Group's voice and messaging.

## Setup

1. **Install dependencies**

```bash
pip install anthropic python-dotenv
```

2. **Environment Variables**

Your Anthropic API key is already set up in the `.env` file in the project root.

3. **Brand Knowledge**

The system loads brand information from `brand_knowledge/brand_brief.json`. This file contains comprehensive information about the LIFT Leadership Group's brand, voice, audience, and messaging.

## Usage

### Quick Start

Run the example script to generate content using the AI agents:

```bash
python brand_knowledge_example.py
```

### Interacting with Agents

Create a custom script to interact with different content agents:

```python
from src.models.model_interface import ModelInterface
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the model interface
model = ModelInterface()

# Generate text-only content
text_post = model.generate_content("text", {
    "topic": "leadership clarity",
    "purpose": "thought leadership",
    "cta_type": "Ask a question"
})
print(text_post)

# Generate media post content
media_post = model.generate_content("media", {
    "topic": "sales acceleration",
    "media_type": "infographic",
    "purpose": "educational"
})
print(media_post)

# Generate article content
article = model.generate_content("article", {
    "topic": "The LIFT Framework",
    "key_points": ["Listen & Learn", "Initiate & Inspire", "Focus & Framework", "Transform the Team"]
})
print(article)
```

## AI Agents

The system includes three specialized AI agents:

1. **TextContentAgent**: Generates text-only LinkedIn posts
2. **MediaContentAgent**: Creates posts designed to accompany visual content
3. **ArticleContentAgent**: Generates long-form thought leadership content

All agents leverage Claude 3 Opus by default, with temperature 0.7 for balanced creativity.

## Brand Knowledge Integration

The AI system automatically enriches all content with brand knowledge through:

1. Context enrichment with brand voice, messaging, and audience information
2. Addition of brand guidance to prompts

## Troubleshooting

If you encounter errors:

1. Ensure the `.env` file exists with your ANTHROPIC_API_KEY
2. Verify the brand_knowledge/brand_brief.json file exists and is valid JSON
3. Try running with Python 3.9-3.11 for best compatibility

## Development

To extend the system:

1. **Add new agent types**: Create new classes that inherit from BaseAgent
2. **Customize prompts**: Modify templates in src/models/prompts.py
3. **Update brand information**: Edit brand_knowledge/brand_brief.json