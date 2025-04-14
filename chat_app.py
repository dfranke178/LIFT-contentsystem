import os
import sys
import logging
import streamlit as st
import json
from pathlib import Path
from dotenv import load_dotenv
from src.models.model_interface import ModelInterface
from src.utils.brand_knowledge import brand_knowledge

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("chat_app")

# Load environment variables
load_dotenv()

# Check for API key
if not os.environ.get("ANTHROPIC_API_KEY"):
    logger.error("ANTHROPIC_API_KEY not set in environment variables")

# Initialize the model interface
model = None
try:
    model = ModelInterface()
    logger.info("Model interface initialized successfully")
except Exception as e:
    logger.error(f"Error initializing model interface: {e}")

# Create directory for storing chat history
os.makedirs("chat_history", exist_ok=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    
    # Available agents
    agent_types = {
        "LinkedIn Content Creator": "text",
        "Media Post Creator": "media",
        "Article Writer": "article"
    }
    
    if "agent_types" not in st.session_state:
        st.session_state.agent_types = agent_types
    
    if "current_agent" not in st.session_state:
        st.session_state.current_agent = next(iter(agent_types.keys()))
    
    # Initialize messages for each agent
    for agent in agent_types:
        if agent not in st.session_state.messages:
            st.session_state.messages[agent] = []

def handle_agent_selection():
    """Handle agent selection from the sidebar"""
    st.session_state.current_agent = st.session_state.selected_agent

def generate_agent_response(agent_type, user_message):
    """Generate a response from the selected agent"""
    try:
        # Map the friendly agent name to the content type
        content_type = st.session_state.agent_types[agent_type]
        
        # Create context based on the agent type
        context = {
            "topic": "General inquiry",
            "purpose": "user assistance"
        }
        
        # Add required fields based on agent type
        if content_type == "text":
            context["cta_type"] = "Respond directly"
        elif content_type == "media":
            context["media_type"] = "general"
        elif content_type == "article":
            context["key_points"] = ["Respond to user inquiry"]
        
        # Custom prompt for chat interaction
        prompt = f"""
        You are a helpful AI assistant specializing in {agent_type.lower()}.
        
        Answer the following question or request from the user:
        
        {user_message}
        
        Provide a helpful, concise response. If asked to generate content, do so based on the user's request.
        """
        
        # Get agent and generate response
        agent = model.get_agent(content_type)
        response = agent.generate_content(prompt, context)
        
        return response
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main function to run the Streamlit chat interface"""
    st.set_page_config(page_title="LIFT AI Chat", page_icon="💬", layout="wide")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for agent selection
    with st.sidebar:
        st.title("LIFT AI Agents")
        st.selectbox(
            "Select an Agent to Chat With",
            options=list(st.session_state.agent_types.keys()),
            index=list(st.session_state.agent_types.keys()).index(st.session_state.current_agent),
            key="selected_agent",
            on_change=handle_agent_selection
        )
        
        st.divider()
        
        # Agent description
        st.subheader(f"About {st.session_state.current_agent}")
        if st.session_state.current_agent == "LinkedIn Content Creator":
            st.write("Specializes in creating engaging LinkedIn text posts with your brand voice.")
        elif st.session_state.current_agent == "Media Post Creator":
            st.write("Creates compelling captions for images, videos, and other media content.")
        elif st.session_state.current_agent == "Article Writer":
            st.write("Writes professional long-form content and thought leadership articles.")
        
        # Add clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages[st.session_state.current_agent] = []
            st.rerun()
    
    # Main chat area
    st.title(f"Chat with {st.session_state.current_agent}")
    
    # Brand info
    with st.expander("Brand Information"):
        if brand_knowledge and hasattr(brand_knowledge, 'get_company_info'):
            company_info = brand_knowledge.get_company_info()
            st.write(f"**Company:** {company_info.get('name', 'Unknown')}")
            st.write(f"**Tagline:** {company_info.get('tagline', 'N/A')}")
            st.write(f"**Mission:** {company_info.get('mission', 'N/A')}")
        else:
            st.write("Brand information not available")
    
    # Display chat messages
    for message in st.session_state.messages[st.session_state.current_agent]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if model is None:
        st.error("Error: AI model not initialized. Please check logs.")
    else:
        if prompt := st.chat_input(f"Message {st.session_state.current_agent}..."):
            # Add user message to chat history
            st.session_state.messages[st.session_state.current_agent].append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_agent_response(st.session_state.current_agent, prompt)
                    st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages[st.session_state.current_agent].append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main() 