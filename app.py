"""
Weather & News Agent Application

A Streamlit-based application that answers questions about weather and news
using intelligent agent orchestration with MCP servers.

Run with: streamlit run app.py
"""

import streamlit as st
import asyncio
from datetime import datetime
import json
from typing import Optional
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.orchestrator import answer_question, OrchestratorAgent

# Page configuration
st.set_page_config(
    page_title="🌤️📰 Weather & News Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .agent-response {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    .news-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
    }
    .tool-call {
        background-color: #e8f4f8;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.3rem 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = OrchestratorAgent()


def format_agent_response(response: dict) -> str:
    """Format agent response for display"""
    message = response.get("message", "")
    agent = response.get("agent", "Unknown")
    query_type = response.get("query_type", "unknown")
    
    return f"**{agent}** (Type: {query_type})\n\n{message}"


def display_execution_details(response: dict):
    """Display tool execution details in an expander"""
    if response.get("responses"):
        with st.expander("📋 Execution Details"):
            for i, agent_resp in enumerate(response["responses"], 1):
                st.subheader(f"Agent {i}: {agent_resp.get('agent_type', 'Unknown')}")
                
                # Display tool calls
                if agent_resp.get("tool_calls"):
                    st.write("**Tools Called:**")
                    for tool_call in agent_resp["tool_calls"]:
                        st.code(
                            f"{tool_call['tool_name']}({json.dumps(tool_call['parameters'], indent=2)})",
                            language="json"
                        )
                
                # Display execution results
                if agent_resp.get("execution_results"):
                    st.write("**Results:**")
                    with st.expander("View Raw Data"):
                        st.json(agent_resp["execution_results"])


def main():
    """Main Streamlit application"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.title("🌤️📰 Weather & News Agent")
        st.markdown(
            "An intelligent agent that answers questions about weather and news using MCP servers."
        )
    
    with col2:
        st.info("""
        **Agent Types:**
        - 🌤️ Weather
        - 📰 News
        - 🤖 Orchestrator
        """)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("## About This Application")
        st.markdown("""
        This application demonstrates:
        
        ✅ **Agent Orchestration**: The orchestrator intelligently routes your queries to specialized agents
        
        ✅ **MCP Servers**: 
        - Open-Meteo API for real-time weather data
        - GNews API for the latest news (no API key required)
        
        ✅ **Multi-Agent System**:
        - WeatherAgent: Handles weather queries
        - NewsAgent: Handles news queries
        - OrchestratorAgent: Routes and combines results
        
        🎯 **Example Queries**:
        - "What's the weather in New York?"
        - "Tell me about the latest AI news"
        - "Weather forecast for London and top tech news"
        - "Is it going to rain in Seattle?"
        - "Get business news headlines"
        """)
        
        st.markdown("---")
        st.markdown("### Quick Query Templates")
        
        # Preset queries
        preset_queries = {
            "🌤️ Current Weather": "What's the current weather in New York?",
            "📅 Weather Forecast": "What's the weather forecast for Paris?",
            "📰 Tech News": "Tell me the latest technology news",
            "📊 Business News": "Get top business news headlines",
            "🔄 Combined Query": "What's the weather in London and latest entertainment news?"
        }
        
        for label, query_text in preset_queries.items():
            if st.button(label, key=f"preset_{label}"):
                st.session_state.current_query = query_text
    
    # Main chat interface
    st.markdown("---")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.write(message["content"])
            else:
                st.markdown(message["content"])
                if "response_data" in message:
                    display_execution_details(message["response_data"])
    
    # User input
    st.markdown("---")
    col1, col2 = st.columns([0.85, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Ask me about weather or news...",
            placeholder="e.g., 'What's the weather in Tokyo?' or 'Latest AI news'",
            key="user_input"
        )
    
    with col2:
        submit_button = st.button("🚀 Ask", use_container_width=True)
    
    # Process user input
    if submit_button and user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Show processing indicator
        with st.spinner("🤔 Thinking..."):
            try:
                # Process the query
                response = asyncio.run(answer_question(user_input))
                
                # Format and display response
                formatted_response = format_agent_response(response)
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": formatted_response,
                    "response_data": response
                })
                
                # Rerun to display new message
                st.rerun()
            
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                st.error(error_message)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
    
    # Clear history button
    if st.session_state.messages:
        if st.sidebar.button("🔄 Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: gray; font-size: 0.9rem;">
        <p>🤖 Powered by Agent Framework with MCP Servers</p>
        <p>Weather data: Open-Meteo | News data: GNews API</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
