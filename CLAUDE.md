# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an agentic chatbot project built with LangChain, LangGraph, and Streamlit. The project is in early development stages and aims to create an AI agent-powered conversational interface.

## Key Technologies

- **LangChain**: Framework for building LLM applications
- **LangGraph**: Orchestration layer for building stateful, multi-actor applications with LLMs
- **LangChain OpenAI**: OpenAI integration for LangChain
- **LangChain Groq**: Groq LLM integration for LangChain
- **Streamlit**: Web UI framework for the chatbot interface
- **FAISS**: Vector database for similarity search and retrieval
- **Tavily**: Search API integration
- **Python-dotenv**: Environment variable management

## Development Setup

### Environment Setup
```bash
# Create and activate virtual environment (using uv or standard venv)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# OR using uv
uv pip install -r requirements.txt
```

### Running the Application
```bash
# Run the main application
python main.py

# Run Streamlit UI (when implemented)
streamlit run <streamlit_app_file>.py
```

## Environment Variables

Create a `.env` file in the project root with necessary API keys:
- OpenAI API key for LangChain OpenAI
- Groq API key for Groq LLM integration
- Tavily API key for search functionality

## Architecture Notes

### LangGraph Agent Structure
When implementing agents with LangGraph:
- Define state schemas for managing conversation and agent state
- Use StateGraph to create nodes representing different agent actions
- Implement conditional edges for routing between agent states
- Tools should be registered and bound to the LLM model

### Vector Store Integration
FAISS is used for vector storage:
- Embeddings should be generated for document chunks
- Use appropriate distance metrics for similarity search
- Consider index persistence for production deployments

### Streamlit UI Patterns
- Use session state to maintain conversation history
- Implement streaming responses for better UX
- Handle async LangChain calls properly within Streamlit's execution model