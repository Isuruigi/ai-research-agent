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
if "results" not in st.session_state:
    st.session_state.results = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "input_query" not in st.session_state:
    st.session_state.input_query = ""

# Theme Palette Definition
themes = {
    "dark": {
        "bg": "#0d0d0d",
        "text": "#f7f7f7",
        "card_bg": "#161b22",
        "border": "#30363d",
        "sub_text": "#8b949e",
        "input_bg": "#161b22",
        "btn_primary": "#58a6ff",
        "chip_bg": "#1c2128",
    },
    "light": {
        "bg": "#f9f8f6",      # Claude-style cream/ivory
        "text": "#1a1a1a",
        "card_bg": "#ffffff",
        "border": "#e1e4e8",
        "sub_text": "#6a737d",
        "input_bg": "#ffffff",
        "btn_primary": "#d97757", # Claude-style accent
        "chip_bg": "#f0f0f0",
    }
}

# Theme Toggle in Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    current_theme = st.selectbox("Appearance", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
    if current_theme != st.session_state.theme:
        st.session_state.theme = current_theme
        st.rerun()
    
    API_URL = st.text_input("API URL", "http://localhost:8000")
    PROVIDER = st.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)
    
    st.markdown("---")
    st.markdown("#### About the Engine")
    st.write("Specialized in Deep Web Retrieval and Structured Synthesis.")

t = themes[st.session_state.theme]

# Minimalist Premium CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
    }}
    
    .main {{
        background-color: {t['bg']} !important;
        color: {t['text']} !important;
    }}
    
    /* Hero Style */
    .hero-container {{
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 2rem;
    }}
    .hero-title {{
        font-family: 'Inter', serif;
        font-size: 3.2rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
        color: {t['text']};
    }}
    .hero-sub {{
        font-size: 1.2rem;
        color: {t['sub_text']};
        margin-bottom: 1.5rem;
    }}
    
    /* Workspace Input - High Fidelity */
    .stTextArea textarea {{
        background-color: {t['input_bg']} !important;
        border: 1px solid {t['border']} !important;
        color: {t['text']} !important;
        font-size: 1.15rem !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        line-height: 1.5 !important;
    }}
    
    /* Buttons / Chips */
    div.stButton > button {{
        background-color: {t['card_bg']};
        color: {t['text']};
        border: 1px solid {t['border']};
        border-radius: 24px;
        font-size: 0.9rem;
        padding: 0.4rem 1rem;
        transition: all 0.2s ease;
    }}
    div.stButton > button:hover {{
        background-color: {t['chip_bg']};
        border-color: {t['sub_text']};
    }}
    
    .research-btn > div.stButton > button {{
        background-color: {t['btn_primary']} !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.7rem 2.5rem !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 12px rgba(217, 119, 87, 0.2) !important;
    }}
    
    /* Report Card */
    .report-card {{
        background-color: {t['card_bg']};
        border: 1px solid {t['border']};
        border-radius: 18px;
        padding: 3rem;
        margin-top: 1.5rem;
        color: {t['text']};
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        line-height: 1.7;
    }}
    
    /* Capabilities Row */
    .cap-pill {{
        background: {t['chip_bg']};
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        color: {t['sub_text']};
        border: 1px solid {t['border']};
    }}
    </style>
    """, unsafe_allow_html=True)

# Main View - Minimalist Modern Header
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">Good afternoon, Isuru</div>
    <div class="hero-sub">Where should we focus our research today?</div>
</div>
""", unsafe_allow_html=True)

# Suggested Research Chips (Minimalist row)
suggestions = [
    "Latest breakthroughs in AI Agentic workflows 2026",
    "Technical comparison of Gemini 1.5 vs Claude 3.5",
    "Future of autonomous scientific discovery"
]

s_cols = st.columns([1, 1, 1, 1, 1])
if s_cols[1].button(suggestions[0]):
    st.session_state.input_query = suggestions[0]
    st.rerun()
if s_cols[2].button(suggestions[1]):
    st.session_state.input_query = suggestions[1]
    st.rerun()
if s_cols[3].button(suggestions[2]):
    st.session_state.input_query = suggestions[2]
    st.rerun()

# Research Input Workspace
with st.container():
    query = st.text_area(
        "", 
        value=st.session_state.input_query,
        placeholder="Enter your research query...", 
        key="research_input_area",
        height=120
    )
    
    st.markdown('<div class="research-btn" style="text-align: center; margin-top: 15px;">', unsafe_allow_html=True)
    if st.button("🚀 Start Deep Research", use_container_width=True):
        if query:
            st.session_state.input_query = query
            with st.spinner("Analyzing web sources and synthesizing report..."):
                try:
                    response = requests.post(
                        f"{API_URL}/research",
                        json={"query": query, "provider": PROVIDER},
                        timeout=120
                    )
                    if response.status_code == 200:
                        data = response.json()
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

# Minimalist Progress Indicators
st.markdown(f"""
<div style="display: flex; justify-content: center; gap: 15px; margin-top: 2rem;">
    <div class="cap-pill">🌐 Live Retrieval</div>
    <div class="cap-pill">📑 Structured Synthesis</div>
    <div class="cap-pill">🔍 Citation Check</div>
</div>
""", unsafe_allow_html=True)

# Results Display
if st.session_state.results:
    st.markdown("<br><br>", unsafe_allow_html=True)
    for res in reversed(st.session_state.results):
        with st.container():
            st.markdown(f'<div class="report-card">', unsafe_allow_html=True)
            st.markdown(f"### 📋 Research Report: {res['query']}")
            st.markdown(f"<small style='color:{t['sub_text']}'>Synthesized at {res['timestamp']}</small>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(res['report'])
            if res['sources']:
                st.markdown("<br>#### Verified Sources", unsafe_allow_html=True)
                for s in res['sources']:
                    st.markdown(f"• **{s.get('title', 'Ref')}**: [Read Full Context]({s.get('url', '#')})")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
