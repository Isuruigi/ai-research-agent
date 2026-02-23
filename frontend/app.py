import os
import streamlit as st
import requests
import time
from datetime import datetime

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
        "bg": "#fcfaf8",
        "text": "#1a1a1a",
        "card_bg": "#ffffff",
        "border": "#e1e4e8",
        "sub_text": "#6a737d",
        "input_bg": "#ffffff",
        "btn_primary": "#d97757",
        "chip_bg": "#f0f0f0",
    }
}

# Dynamic Greeting based on time
def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good morning"
    elif hour < 17: return "Good afternoon"
    else: return "Good evening"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")

    current_theme = st.selectbox(
        "Appearance", ["light", "dark"],
        index=0 if st.session_state.theme == "light" else 1
    )
    if current_theme != st.session_state.theme:
        st.session_state.theme = current_theme
        st.rerun()

    API_URL = st.text_input("API URL", "http://localhost:8000")
    PROVIDER = st.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)

    # API Key — read from HF Secret first, allow override locally
    API_KEY = st.text_input(
        "API Key",
        value=os.environ.get("API_KEY", ""),
        type="password",
        help="Set API_KEY in HF Space secrets. Leave blank if auth is disabled."
    )

    # Live backend status
    try:
        import urllib.request as _ur
        _ur.urlopen(f"{API_URL}/health", timeout=3)
        st.success("Backend: Online")
    except Exception:
        st.warning("Backend: Starting up — wait ~30s then retry.")

    st.markdown("---")
    st.markdown("#### The Agent Difference")
    st.info("Unlike standard chatbots, this engine performs real-time web retrieval, cross-references sources, and synthesizes long-form reports.")

t = themes[st.session_state.theme]
sidebar_bg = "#111111" if st.session_state.theme == "dark" else "#ffffff"

# ── CSS — full theme coverage ─────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
}}
.stApp {{
    background-color: {t['bg']} !important;
    color: {t['text']} !important;
}}
[data-testid="stHeader"] {{
    background-color: {t['bg']} !important;
}}
section.main {{
    background-color: {t['bg']} !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {sidebar_bg} !important;
    border-right: 1px solid {t['border']};
}}
[data-testid="stSidebar"] * {{
    color: {t['text']} !important;
}}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li {{
    color: {t['text']} !important;
}}

/* ── Labels & Markdown ── */
label {{
    color: {t['text']} !important;
}}
.stMarkdown p, .stMarkdown li, .stMarkdown h1,
.stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
    color: {t['text']} !important;
}}

/* ── Text inputs ── */
.stTextInput input, .stTextInput textarea {{
    background-color: {t['input_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
}}
.stTextArea textarea {{
    background-color: {t['input_bg']} !important;
    border: 1px solid {t['border']} !important;
    color: {t['text']} !important;
    font-size: 1.1rem !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
}}

/* ── Select boxes ── */
[data-testid="stSelectbox"] > div {{
    background-color: {t['input_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['border']} !important;
    border-radius: 8px !important;
}}
[data-baseweb="select"] {{
    background-color: {t['input_bg']} !important;
}}
[data-baseweb="select"] * {{
    background-color: {t['input_bg']} !important;
    color: {t['text']} !important;
}}
[data-baseweb="popover"] * {{
    background-color: {t['card_bg']} !important;
    color: {t['text']} !important;
}}

/* ── Radio buttons ── */
.stRadio label, .stRadio div {{
    color: {t['text']} !important;
}}
[data-baseweb="radio"] * {{
    color: {t['text']} !important;
}}

/* ── Spinner ── */
.stSpinner > div {{
    border-top-color: {t['btn_primary']} !important;
}}
.stSpinner p, [data-testid="stSpinner"] p {{
    color: {t['text']} !important;
}}

/* ── Buttons ── */
div.stButton > button {{
    background-color: {t['card_bg']};
    color: {t['text']};
    border: 1px solid {t['border']};
    border-radius: 20px;
    font-size: 0.85rem;
    padding: 0.4rem 1.2rem;
    transition: all 0.2s ease;
}}
.research-btn > div.stButton > button {{
    background-color: {t['btn_primary']} !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.7rem 2.5rem !important;
    border-radius: 12px !important;
}}

/* ── Alert / Info boxes ── */
.stAlert {{
    background-color: {t['card_bg']} !important;
    color: {t['text']} !important;
    border: 1px solid {t['border']} !important;
}}

/* ── Hero ── */
.hero-container {{
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 2rem;
}}
.hero-title {{
    font-size: 3.2rem;
    font-weight: 500;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
    color: {t['text']};
}}
.hero-sub {{
    font-size: 1.1rem;
    color: {t['sub_text']};
    margin-bottom: 1rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}}

/* ── Report Card ── */
.report-card {{
    background-color: {t['card_bg']};
    border: 1px solid {t['border']};
    border-radius: 16px;
    padding: 2.5rem;
    margin-top: 1rem;
    color: {t['text']};
    box-shadow: 0 4px 24px rgba(0,0,0,0.03);
}}
</style>
""", unsafe_allow_html=True)

# ── Main View ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">{get_greeting()}</div>
    <div class="hero-sub">Experimental Research Agent — Built for deep retrieval, synthesized reporting, and multi-source verification.</div>
</div>
""", unsafe_allow_html=True)

# Suggested Research
suggestions = [
    "Competitive analysis of AI research agents 2026",
    "Technical comparison of Gemini 1.5 vs Claude 3.5",
    "Future of autonomous scientific discovery"
]

st.markdown("<div style='text-align: center; color: #8b949e; font-size: 0.85rem; margin-bottom: 12px;'>Start with a suggested topic</div>", unsafe_allow_html=True)
s_cols = st.columns([1, 1, 1, 1, 1])
if s_cols[1].button(suggestions[0]): st.session_state.input_query = suggestions[0]; st.rerun()
if s_cols[2].button(suggestions[2]): st.session_state.input_query = suggestions[2]; st.rerun()
if s_cols[3].button(suggestions[1]): st.session_state.input_query = suggestions[1]; st.rerun()

# Research Input
with st.container():
    query = st.text_area(
        "",
        value=st.session_state.get("input_query", ""),
        placeholder="What would you like to research deeply?",
        key="research_input",
        height=100
    )

    st.markdown(f"<div style='text-align:center; color:{t['sub_text']}; font-size:0.8rem; margin: 8px 0 4px 0;'>Report Depth</div>", unsafe_allow_html=True)
    depth_map = {
        "⚡ Brief": "brief",
        "📄 Detailed": "detailed",
        "🔬 Comprehensive": "comprehensive"
    }
    depth_choice = st.radio(
        "",
        options=list(depth_map.keys()),
        index=1,
        horizontal=True,
        key="depth_selector",
        label_visibility="collapsed"
    )
    DEPTH = depth_map[depth_choice]

    depth_hints = {
        "brief": "~300 words · fast · key facts only",
        "detailed": "~600 words · balanced · insights + sources",
        "comprehensive": "~1200 words · deep dive · full analysis"
    }
    st.markdown(f"<div style='text-align:center; color:{t['sub_text']}; font-size:0.75rem; margin-bottom:10px;'>{depth_hints[DEPTH]}</div>", unsafe_allow_html=True)

    st.markdown('<div class="research-btn" style="text-align: center; margin-top: 10px;">', unsafe_allow_html=True)
    if st.button("🚀 Start Deep Research", use_container_width=True):
        if query:
            st.session_state.input_query = query
            spinner_labels = {
                "brief": "Fetching key facts...",
                "detailed": "Analyzing web sources and synthesizing report...",
                "comprehensive": "Running deep research across all sources — this may take a moment..."
            }
            with st.spinner(spinner_labels[DEPTH]):
                try:
                    headers = {}
                    if API_KEY:
                        headers["X-API-Key"] = API_KEY

                    response = requests.post(
                        f"{API_URL}/research",
                        json={"query": query, "provider": PROVIDER, "depth": DEPTH},
                        headers=headers,
                        timeout=180
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if "results" not in st.session_state:
                            st.session_state.results = []
                        st.session_state.results.append({
                            "query": query,
                            "report": data.get('answer'),
                            "sources": data.get('sources', []),
                            "timestamp": time.strftime("%H:%M"),
                            "depth": DEPTH
                        })
                    elif response.status_code == 403:
                        st.error("403 Forbidden — API key is required. Set it in the sidebar or add API_KEY to HF Space secrets.")
                    elif response.status_code == 429:
                        st.error("Rate limit reached. Please wait a minute before trying again.")
                    else:
                        st.error(f"Engine Error ({response.status_code}): {response.text}")
                except Exception as e:
                    err = str(e)
                    if "Connection refused" in err or "Failed to establish" in err or "Cannot connect" in err:
                        st.error("Cannot connect to the research engine. The backend may still be starting — please wait 30 seconds and retry.")
                    else:
                        st.error(f"Search failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# Differentiator Section
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div style='text-align:center; font-size:0.85rem; color:{t['sub_text']}'>🌐 **Live Retrieval**<br>Scans the web in real-time</div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div style='text-align:center; font-size:0.85rem; color:{t['sub_text']}'>📊 **Deep Synthesis**<br>Connects dots across sources</div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div style='text-align:center; font-size:0.85rem; color:{t['sub_text']}'>🔗 **Source Verified**<br>Every claim includes a link</div>", unsafe_allow_html=True)

# Results Display
if "results" in st.session_state and st.session_state.results:
    st.markdown("<br><br>", unsafe_allow_html=True)
    for res in reversed(st.session_state.results):
        st.markdown(f"""
        <div class="report-card">
            <h3>📋 Research Report</h3>
            <p style="color:{t['sub_text']}; font-size:0.85rem; margin-bottom:0.5rem;">
                🔍 {res['query']}
            </p>
            <small style='color:{t['sub_text']}'>Synthesized at {res['timestamp']}</small>
            <hr style="border-color:{t['border']}; margin: 1rem 0;">
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown(res['report'])

        if res['sources']:
            st.markdown("#### 🔗 Verified Sources")
            for s in res['sources']:
                title = s.get('title', 'Source')
                url = s.get('url', '#')
                st.markdown(f"- **{title}**: [{url[:60]}...]({url})")

        st.markdown("<br>", unsafe_allow_html=True)
