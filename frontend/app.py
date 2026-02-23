import os
import streamlit as st
import requests
import time
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

# ── THEME PALETTE (Claude/Gemini Aesthetic) ───────────────────────────────────
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
        "bg": "#fcfaf8",        # warm ivory (Claude signature)
        "bg_sidebar": "#ffffff",
        "text": "#1d1d1f",
        "card_bg": "#ffffff",
        "border": "#e5e5e7",
        "sub_text": "#86868b",
        "input_bg": "#ffffff",
        "btn_primary": "#d97757", # burnt orange accent
        "accent": "#c66d4f",
        "shadow": "rgba(0,0,0,0.08)"
    }
}

# Dynamic Greeting
def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good morning"
    elif hour < 17: return "Good afternoon"
    else: return "Good evening"

t = themes[st.session_state.theme]

# ── EXHAUSTIVE CSS (The "No Bullshit" Version) ───────────────────────────────
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
    padding-right: 3.5rem !important; /* Extra room for eye icon */
}}

/* Fix the eye icon position/color */
button[aria-label="Show password"], button[aria-label="Hide password"] {{
    color: {t['sub_text']} !important;
    background: transparent !important;
    right: 10px !important;
}}

/* ── RADIO BUTTONS (Premium Chip Style) ── */
/* Hide the default radio circle/dot */
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

/* Hero Typography */
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
    transition: all 0.3s ease;
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
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px {t['btn_primary']}55 !important;
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
    
    current_theme = st.selectbox("Appearance", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
    if current_theme != st.session_state.theme:
        st.session_state.theme = current_theme
        st.rerun()

    API_URL = st.text_input("API URL", "http://localhost:8000")
    
    API_KEY = st.text_input(
        "API Key",
        value=os.environ.get("API_KEY", "your-secret-api-key-change-this"),
        type="password",
        help="Paste your API key here. It will not overlap with the eye icon."
    )
    
    PROVIDER = st.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)

    st.markdown("---")
    st.markdown("#### Engine Status")
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=2)
        if health_resp.status_code == 200:
            st.markdown('<div class="status-pill status-online">● Core Engine: Online</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-pill status-offline">● Error: {health_resp.status_code}</div>', unsafe_allow_html=True)
    except Exception:
        st.markdown('<div class="status-pill status-offline">● Engine: Offline</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.info("Recursive search & synthesis powered by LangGraph.")

# ── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='text-align: center; margin-top: 5rem;'>
    <h1 class='hero-title'>{get_greeting()}</h1>
    <h2 style='font-size: 2.5rem; font-weight: 400; color: {t['sub_text']}; margin-top: -10px;'>
        I'm <span style='color:{t['btn_primary']}; font-weight: 700;'>Isuru</span>. Your intelligence layer.
    </h2>
    <p style='font-size: 1.3rem; color: {t['sub_text']}; max-width: 600px; margin: 2rem auto; font-weight: 400; line-height: 1.5;'>
        I synthesize the web into verifiable, high-fidelity research reports. 
        Scanning, verifying, and reporting in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# ── RESEARCH INPUT ──────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.container():
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        query = st.text_area(
            label="Research Query",
            label_visibility="collapsed",
            value=st.session_state.get("input_query", ""),
            placeholder="What would you like to research deeply?",
            key="research_area",
            height=150
        )

        st.markdown(f"<div style='text-align:center; color:{t['sub_text']}; font-size:0.95rem; margin-top:2.5rem; font-weight:500;'>SELECT REPORT FIDELITY</div>", unsafe_allow_html=True)
        depth_map = {"⚡ Brief": "brief", "📄 Detailed": "detailed", "🔬 Comprehensive": "comprehensive"}
        depth_choice = st.radio("Depth", options=list(depth_map.keys()), index=1, horizontal=True, label_visibility="collapsed")
        DEPTH = depth_map[depth_choice]
        
        st.markdown('<div class="main-btn" style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🚀 Start Deep Research", key="go_btn"):
            if query:
                st.session_state.input_query = query
                with st.spinner(f"Investigating '{query}'..."):
                    try:
                        headers = {"X-API-Key": API_KEY} if API_KEY else {}
                        resp = requests.post(f"{API_URL}/research", json={"query": query, "provider": PROVIDER, "depth": DEPTH}, headers=headers, timeout=300)
                        if resp.status_code == 200:
                            data = resp.json()
                            st.session_state.results.append({
                                "query": query, "report": data.get('answer'), "sources": data.get('sources', []),
                                "timestamp": datetime.now().strftime("%H:%M"), "depth": DEPTH
                            })
                        elif resp.status_code == 403: st.error("🔒 Auth Token Invalid.")
                        else: st.error(f"❌ Engine Error: {resp.text}")
                    except Exception as e: st.error(f"📡 Connection Failed.")
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
            for s in res['sources']:
                st.markdown(f"- **{s.get('title', 'Source')}**: [{s.get('url', '#')}]({s.get('url', '#')})")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
