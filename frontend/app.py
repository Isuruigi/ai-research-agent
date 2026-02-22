import streamlit as st
import requests
import json
import time

# Premium UI Configuration
st.set_page_config(
    page_title="Deep Research Engine",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "research_query" not in st.session_state:
    st.session_state.research_query = ""
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Theme Toggle in Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    st.session_state.theme = st.selectbox("Appearance", ["dark", "light"], index=0 if st.session_state.theme == "dark" else 1)
    
    API_URL = st.text_input("API URL", "http://localhost:8000")
    PROVIDER = st.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)
    
    st.markdown("---")
    st.markdown("#### About the Engine")
    st.write("This research agent performs Deep Web Retrieval and Structured Synthesis to provide comprehensive reports.")

# Dynamic CSS based on Theme
bg_color = "#0d0d0d" if st.session_state.theme == "dark" else "#ffffff"
text_color = "#f7f7f7" if st.session_state.theme == "dark" else "#0d0d0d"
card_bg = "#161b22" if st.session_state.theme == "dark" else "#f0f2f6"
border_color = "#30363d" if st.session_state.theme == "dark" else "#d1d5da"
sub_text = "#8b949e" if st.session_state.theme == "dark" else "#586069"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    .main {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Hero Section */
    .hero-title {{
        font-size: 2.8rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        text-align: center;
        background: linear-gradient(90deg, #58a6ff, #bc85ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-sub {{
        font-size: 1.1rem;
        color: {sub_text};
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    /* Capability Pills */
    .capability-container {{
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }}
    .capability-pill {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        color: {text_color};
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
    }}
    
    /* Workspace Input */
    .stTextArea textarea {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        color: {text_color} !important;
        font-size: 1.1rem !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
    }}
    
    /* Suggestions Buttons Styling */
    div.stButton > button {{
        background-color: {card_bg};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 20px;
        font-size: 0.85rem;
        padding: 0.3rem 0.8rem;
    }}
    
    /* Research Button */
    .research-btn > div.stButton > button {{
        background-color: #58a6ff !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        border: none !important;
    }}
    
    /* Report Card */
    .report-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 2.5rem;
        margin-top: 1.5rem;
        color: {text_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# Main View
st.markdown('<div class="hero-title">Deep Research Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Autonomous AI specialized in deep retrieval and synthesis.</div>', unsafe_allow_html=True)

# Suggestions (ABOVE the chat window)
st.markdown("<div style='text-align: center; color: #8b949e; font-size: 0.9rem; margin-bottom: 10px;'>Suggested Research</div>", unsafe_allow_html=True)
suggestions = [
    "Competitive analysis of AI research agents 2026",
    "Technical breakdown of Gemini reasoning models",
    "Impact of agentic workflows on productivity"
]

# Layout suggestions in columns
s_cols = st.columns([1, 1.5, 1.5, 1.5, 1])
if s_cols[1].button(suggestions[0]): st.session_state.research_query = suggestions[0]
if s_cols[2].button(suggestions[1]): st.session_state.research_query = suggestions[1]
if s_cols[3].button(suggestions[2]): st.session_state.research_query = suggestions[2]

# Research Input
with st.container():
    query = st.text_area(
        "", 
        value=st.session_state.research_query,
        placeholder="What would you like to research today?", 
        key="main_query",
        height=100
    )
    
    st.markdown('<div class="research-btn">', unsafe_allow_html=True)
    if st.button("🚀 Start Deep Research", use_container_width=True):
        if query:
            with st.spinner("Analyzing multiple web sources..."):
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
    st.markdown('</div>', unsafe_allow_html=True)

# Capabilities Row
st.markdown("""
<div class="capability-container">
    <div class="capability-pill">🌐 Live Web Access</div>
    <div class="capability-pill">📊 Data Synthesis</div>
    <div class="capability-pill">🔗 Source Verification</div>
</div>
""", unsafe_allow_html=True)

# Display Results
if "results" in st.session_state and st.session_state.results:
    st.markdown("---")
    for res in reversed(st.session_state.results):
        st.markdown(f'<div class="report-card">', unsafe_allow_html=True)
        st.markdown(f"### 📋 {res['query']}")
        st.markdown(f"<small style='color:#8b949e'>Generated at {res['timestamp']}</small>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(res['report'])
        if res['sources']:
            st.markdown("<br>#### Sources", unsafe_allow_html=True)
            for s in res['sources']:
                st.markdown(f"• **{s.get('title', 'Ref')}**: [Read link]({s.get('url', '#')})")
        st.markdown('</div>', unsafe_allow_html=True)
