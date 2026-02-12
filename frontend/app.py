"""Simple Streamlit frontend for demo"""
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Research Agent")
st.markdown("Production-ready AI agent with RAG and web search")

# API endpoint
API_URL = st.text_input(
    "API URL",
    value="http://localhost:8000",
    help="Cloud Run URL or localhost for testing"
)

# Session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None

if 'history' not in st.session_state:
    st.session_state.history = []

# Query input
query = st.text_area(
    "Enter your research question:",
    height=100,
    placeholder="e.g., What are the latest advancements in LangGraph?"
)

col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("🔍 Research", type="primary")
with col2:
    clear_button = st.button("🗑️ Clear History")

if clear_button:
    st.session_state.history = []
    st.session_state.session_id = None
    st.rerun()

if search_button and query:
    with st.spinner("Researching..."):
        try:
            response = requests.post(
                f"{API_URL}/research",
                json={
                    "query": query,
                    "session_id": st.session_state.session_id
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.session_id = data.get('session_id')
                
                # Add to history
                st.session_state.history.append({
                    "query": query,
                    "response": data.get('response'),
                    "sources": data.get('sources', [])
                })
                
                st.success("Research complete!")
            else:
                st.error(f"Error: {response.text}")
                
        except Exception as e:
            st.error(f"Request failed: {e}")

# Display history
if st.session_state.history:
    st.markdown("---")
    st.subheader("Research History")
    
    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Q: {item['query'][:100]}...", expanded=(i==0)):
            st.markdown("**Response:**")
            st.write(item['response'])
            
            if item['sources']:
                st.markdown("**Sources:**")
                for source in item['sources']:
                    st.markdown(f"- {source}")
