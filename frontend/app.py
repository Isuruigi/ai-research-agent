import os
import streamlit as st
import requests
import random
from datetime import datetime

# ── PREMIUM UI CONFIGURATION ──────────────────────────────────────────────────
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

# ── THEME PALETTE ─────────────────────────────────────────────────────────────
themes = {
    "dark": {
        "bg": "#0d0d0d",
        "bg_sidebar": "#161616",
        "text": "#f5f5f7",
        "card_bg": "#1c1c1e",
        "border": "#2c2c2e",
        "sub_text": "#a1a1a6",
        "input_bg": "#2c2c2e",
        "btn_primary": "#58a6ff",
        "accent": "#409fff",
        "shadow": "rgba(0,0,0,0.6)"
    },
    "light": {
        "bg": "#fcfaf8",
        "bg_sidebar": "#ffffff",
        "text": "#1d1d1f",
        "card_bg": "#ffffff",
        "border": "#e5e5e7",
        "sub_text": "#86868b",
        "input_bg": "#ffffff",
        "btn_primary": "#d97757",
        "accent": "#c66d4f",
        "shadow": "rgba(0,0,0,0.08)"
    }
}

t = themes[st.session_state.theme]

# ── QUOTE ENGINE ──────────────────────────────────────────────────────────────
QUOTES = [
    "“The goal of research is not to find facts, but to understand truth.”",
    "“Intelligence is the ability to adapt to change.” — Stephen Hawking",
    "“The beautiful thing about learning is that nobody can take it away from you.” — B.B. King",
    "“In a world of data, insights are the ultimate currency.”",
    "“Research is formalized curiosity. It is poking and prying with a purpose.” — Zora Neale Hurston",
    "“The important thing is not to stop questioning.” — Albert Einstein",
    "“Information is not knowledge.” — Albert Einstein",
    "“The essence of the independent mind lies not in what it thinks, but in how it thinks.” — Christopher Hitchens"
]
if "current_quote" not in st.session_state:
    st.session_state.current_quote = random.choice(QUOTES)

# ── EXHAUSTIVE CSS (Premium Theming) ──────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Base Overrides */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
}}
.stApp {{
    background-color: {t['bg']} !important;
    color: {t['text']} !important;
}}
[data-testid="stHeader"] {{
    background-color: transparent !important;
}}

/* Sidebar Styling */
[data-testid="stSidebar"] {{
    background-color: {t['bg_sidebar']} !important;
    border-right: 1px solid {t['border']};
}}

/* Inputs & Overlap Fixes */
.stTextArea textarea {{
    background-color: {t['input_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 20px !important;
    padding: 1.5rem !important;
    font-size: 1.15rem !important;
    box-shadow: 0 4px 25px {t['shadow']} !important;
}}

/* API Key Input - Fix overlap with eye icon */
[data-testid="stTextInput"] input {{
    background-color: {t['input_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 12px !important;
    padding-right: 3.5rem !important;
}}

/* Eye icon fix */
button[aria-label="Show password"], button[aria-label="Hide password"] {{
    color: {t['sub_text']} !important;
    background: transparent !important;
    right: 10px !important;
}}

/* ── RADIO BUTTONS (Premium Chip Style) ── */
[data-testid="stRadio"] [role="radiogroup"] div[data-testid="stMarkdownContainer"] {{
    display: none !important;
}}
[data-testid="stRadio"] [role="radiogroup"] {{
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 10px;
}}
[data-testid="stRadio"] [role="radiogroup"] label {{
    background-color: {t['card_bg']} !important;
    border: 1.5px solid {t['border']} !important;
    padding: 10px 24px !important;
    border-radius: 40px !important;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: {t['sub_text']} !important;
    font-weight: 500 !important;
}}
[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {{
    background-color: {t['btn_primary']} !important;
    border-color: {t['btn_primary']} !important;
    color: white !important;
    box-shadow: 0 4px 15px {t['btn_primary']}44 !important;
    transform: translateY(-2px);
}}

/* Hero Section */
.hero-quote {{
    font-size: 1.2rem;
    font-style: italic;
    color: {t['sub_text']};
    margin-bottom: 2rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
    line-height: 1.6;
}}
.hero-title {{
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, {t['text']}, {t['sub_text']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* Preset Chips */
.preset-chip {{
    display: inline-block;
    padding: 8px 18px;
    background: {t['card_bg']};
    border: 1px solid {t['border']};
    border-radius: 50px;
    margin: 5px;
    cursor: pointer;
    font-size: 0.9rem;
    color: {t['text']};
    transition: all 0.2s;
}}
.preset-chip:hover {{
    border-color: {t['btn_primary']};
    background: {t['btn_primary']}11;
}}

/* Backend Status Pill */
.status-pill {{
    display: inline-flex;
    align-items: center;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 2rem;
}}
.status-online {{
    background-color: rgba(46, 204, 113, 0.1);
    color: #2ecc71;
    border: 1px solid rgba(46, 204, 113, 0.2);
}}
.status-offline {{
    background-color: rgba(231, 76, 60, 0.1);
    color: #e74c3c;
    border: 1px solid rgba(231, 76, 60, 0.2);
}}

/* Main Button */
div.stButton > button {{
    border-radius: 50px;
    font-weight: 600;
    padding: 0.8rem 2rem;
}}
.main-btn div.stButton > button {{
    background-color: {t['btn_primary']} !important;
    color: white !important;
    border: none !important;
    padding: 1.2rem 4rem !important;
    font-size: 1.3rem !important;
    margin-top: 2rem;
    box-shadow: 0 10px 30px {t['btn_primary']}33 !important;
}}
.main-btn div.stButton > button:hover {{
    transform: translateY(-3px);
}}

/* Report Card */
.report-card {{
    background-color: {t['card_bg']};
    border: 1px solid {t['border']};
    border-radius: 30px;
    padding: 4rem;
    margin: 3rem 0;
    box-shadow: 0 20px 60px {t['shadow']};
}}

#MainMenu, footer {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    current_theme = st.selectbox(
        "Appearance", 
        ["light", "dark"], 
        index=0 if st.session_state.theme == "light" else 1,
        help="Switch between Light (Ivory) and Dark themes."
    )
    if current_theme != st.session_state.theme:
        st.session_state.theme = current_theme
        st.rerun()

    API_URL = st.text_input(
        "Backend URL", 
        "http://localhost:8000",
        help="The endpoint where your AI research engine is running (e.g., http://localhost:8000 or a specific HF Space URL)."
    )
    
    API_KEY = st.text_input(
        "Access Key (X-API-Key)",
        value=os.environ.get("API_KEY", "your-secret-api-key-change-this"),
        type="password",
        help="The security token used to authenticate your requests to the backend."
    )
    
    PROVIDER = st.selectbox(
        "LLM Model Provider", 
        ["groq", "openai", "anthropic"], 
        index=0,
        help="Choose which AI brain to use for synthesizing the research. Groq is typically fastest."
    )

    st.markdown("---")
    st.markdown("#### Connectivity")
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=2)
        if health_resp.status_code == 200:
            st.markdown('<div class="status-pill status-online">● Core Engine: Ready</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-pill status-offline">● Error: {health_resp.status_code}</div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="status-pill status-offline">● Engine: Offline</div>', unsafe_allow_html=True)

# ── HERO CONTENT ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align: center; margin-top: 5rem;'>
    <div class='hero-quote'>{st.session_state.current_quote}</div>
    <h2 style='font-size: 3.5rem; font-weight: 800; letter-spacing: -0.05em; color: {t['text']}'>
        I'm <span style='color:{t['btn_primary']}; font-weight: 800;'>Isuru</span>.
    </h2>
</div>
""", unsafe_allow_html=True)

# ── PREBUILT QUESTIONS ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
presets = [
    "Latest AI agent trends for Q1 2026",
    "Progress in room-temperature superconductors",
    "Current state of commercial fusion energy",
    "NVIDIA's PersonaPlex architecture details",
    "Top 5 cybersecurity threats for financial apps"
]

cols = st.columns(len(presets))
for i, p in enumerate(presets):
    with cols[i]:
        if st.button(p, key=f"pre_{i}", use_container_width=True):
            st.session_state.input_query = p
            st.rerun()

# ── RESEARCH INPUT ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        query = st.text_area(
            label="Research Query",
            label_visibility="collapsed",
            value=st.session_state.input_query,
            placeholder="What mission-critical topic should I investigate today?",
            key="research_area",
            height=120
        )

        st.markdown(f"<div style='text-align:center; color:{t['sub_text']}; font-size:0.95rem; margin-top:2.5rem; font-weight:600; letter-spacing:0.1em;'>REPORT FIDELITY</div>", unsafe_allow_html=True)
        depth_map = {"⚡ Brief": "brief", "📄 Detailed": "detailed", "🔬 Deep Dive": "comprehensive"}
        depth_choice = st.radio("Depth", options=list(depth_map.keys()), index=1, horizontal=True, label_visibility="collapsed")
        DEPTH = depth_map[depth_choice]
        
        st.markdown('<div class="main-btn" style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🚀 Synthesize Insights", key="go_btn"):
            if query:
                st.session_state.input_query = query
                with st.spinner(f"Scanning web for '{query}'..."):
                    try:
                        headers = {"X-API-Key": API_KEY} if API_KEY else {}
                        resp = requests.post(f"{API_URL}/research", json={"query": query, "provider": PROVIDER, "depth": DEPTH}, headers=headers, timeout=300)
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state.results.append({
                                "query": query, "report": data.get('answer'), "sources": data.get('sources', []),
                                "timestamp": datetime.now().strftime("%H:%M"), "depth": DEPTH
                            })
                            # Change quote for next search
                            st.session_state.current_quote = random.choice(QUOTES)
                        elif resp.status_code == 403: st.error("🔒 Auth Token Invalid.")
                        else: st.error(f"❌ Backend Error: {resp.text}")
                    except Exception as e: st.error(f"📡 Backend Connection Failed.")
        st.markdown('</div>', unsafe_allow_html=True)

# ── RESULTS ──────────────────────────────────────────────────────────────────
if st.session_state.results:
    st.markdown("<br><br><br><hr style='opacity:0.1'><br>", unsafe_allow_html=True)
    for res in reversed(st.session_state.results):
        st.markdown(f"""
<div class="report-card">
    <div style="display: flex; justify-content: space-between; align-items: top;">
        <div>
            <h2 style="margin:0; font-size:2.2rem; font-weight:700;">📋 Research Report</h2>
            <p style="color:{t['sub_text']}; font-size:1.2rem; margin: 0.5rem 0 0 0;">🔍 {res['query']}</p>
        </div>
        <div style="text-align: right;">
            <span style="background:{t['btn_primary']}22; color:{t['btn_primary']}; padding: 6px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">{res['depth'].upper()}</span>
            <div style="color:{t['sub_text']}; font-size: 0.9rem; margin-top: 8px;">{res['timestamp']}</div>
        </div>
    </div>
    <hr style="border-color:{t['border']}; margin: 2.5rem 0;">
    <div style="font-size: 1.2rem; line-height: 1.8; font-weight: 400;">
""", unsafe_allow_html=True)

        st.markdown(res['report'])
        
        if res.get('sources'):
            st.markdown("<br><br>### 🔗 Verified Sources", unsafe_allow_html=True)
            for i, s in enumerate(res['sources']):
                st.markdown(f"{i+1}. **{s.get('title', 'Source')}**: [{s.get('url', '#')}]({s.get('url', '#')})")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
