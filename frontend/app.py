import streamlit as st
import requests
import json
import time

# Premium UI Configuration
st.set_page_config(
    page_title="Intelligence Research Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimalist Google/Claude-style CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0d0d0d;
        color: #f7f7f7;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 600;
        margin-top: 4rem;
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(90deg, #58a6ff, #bc85ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        font-size: 1.1rem;
        color: #8b949e;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    /* Capability Pills */
    .capability-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .capability-pill {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #c9d1d9;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Workspace Input */
    .stTextArea textarea {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #f7f7f7 !important;
        font-size: 1.1rem !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        transition: border-color 0.2s ease;
    }
    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
    }
    
    /* Research Card (Results) */
    .report-card {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2.5rem;
        margin-top: 2rem;
        line-height: 1.6;
    }
    .source-link {
        color: #58a6ff;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .source-link:hover {
        text-decoration: underline;
    }
    
    /* Action Buttons */
    div.stButton > button {
        background-color: #f7f7f7;
        color: #0d0d0d;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #ffffff;
        box-shadow: 0 0 15px rgba(255,255,255,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Advanced Configuration in Sidebar (Hidden by default)
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    API_URL = st.text_input("API URL", "http://localhost:8000")
    PROVIDER = st.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)
    st.markdown("---")
    st.markdown("#### About the Engine")
    st.write("This research agent differs from standard chatbots by performing **Deep Web Retrieval** and **Structured Synthesis** before responding.")

# Main View
st.markdown('<div class="hero-title">Deep Research Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Autonomous AI Agent specialized in real-time information retrieval and comprehensive reporting.</div>', unsafe_allow_html=True)

# Capabilities Row
st.markdown("""
<div class="capability-container">
    <div class="capability-pill">🌐 Web Search Integrated</div>
    <div class="capability-pill">📊 Research Synthesis</div>
    <div class="capability-pill">🔗 Multi-Source Citation</div>
</div>
""", unsafe_allow_html=True)

# Workspace
with st.container():
    query = st.text_area(
        "", 
        placeholder="What would you like to research today?", 
        key="research_query",
        height=120
    )
    
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        if st.button("🚀 Start Research", use_container_width=True):
            if query:
                with st.spinner("Synthesizing research from multiple web sources..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/research",
                            json={"query": query, "provider": PROVIDER},
                            timeout=90
                        )
                        if response.status_code == 200:
                            data = response.json()
                            if "results" not in st.session_state: st.session_state.results = []
                            st.session_state.results.append({
                                "query": query,
                                "report": data.get('answer'),
                                "sources": data.get('sources', []),
                                "timestamp": time.strftime("%H:%M")
                            })
                        else:
                            st.error(f"Engine Error: {response.text}")
                    except Exception as e:
                        st.error(f"Search failed: {e}")

# Display Results
if "results" in st.session_state and st.session_state.results:
    st.markdown("---")
    for res in reversed(st.session_state.results):
        st.markdown(f'<div class="report-card">', unsafe_allow_html=True)
        st.markdown(f"### 📋 Research Report: {res['query']}")
        st.markdown(f"<small style='color:#8b949e'>Generated at {res['timestamp']}</small>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Main Report Content
        st.markdown(res['report'])
        
        # Sources Section
        if res['sources']:
            st.markdown("<br>#### 🔗 Verified Sources", unsafe_allow_html=True)
            for s in res['sources']:
                st.markdown(f"• **{s.get('title', 'Ref')}**: [Read more]({s.get('url', '#')})")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Ready-made Suggestions (Minimalist)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("##### Suggestions")
s_col1, s_col2, s_col3 = st.columns(3)
suggestions = [
    "Competitive analysis of AI research agents 2026",
    "Impact of agentic workflows on enterprise productivity",
    "Technical breakdown of Google's latest Gemini reasoning models"
]
if s_col1.button(f"🔍 {suggestions[0]}"): 
    st.session_state.research_query = suggestions[0]
if s_col2.button(f"🔍 {suggestions[1]}"): 
    st.session_state.research_query = suggestions[1]
if s_col3.button(f"🔍 {suggestions[2]}"): 
    st.session_state.research_query = suggestions[2]
