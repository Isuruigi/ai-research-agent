"""Streamlit frontend for AI Research Agent — HF Spaces / local dev"""
import os
import random
import requests
import streamlit as st
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ─────────────────────────────────────────────────────────────
for _k, _v in [("results", []), ("theme", "light"), ("input_query", "")]:
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Theme palette ─────────────────────────────────────────────────────────────
themes = {
    "dark": {
        "bg": "#0d0d0d", "bg_sidebar": "#161616", "text": "#f5f5f7",
        "card_bg": "#1c1c1e", "border": "#2c2c2e", "sub_text": "#a1a1a6",
        "input_bg": "#2c2c2e", "btn_primary": "#58a6ff", "accent": "#409fff",
        "shadow": "rgba(0,0,0,0.6)"
    },
    "light": {
        "bg": "#fcfaf8", "bg_sidebar": "#ffffff", "text": "#1d1d1f",
        "card_bg": "#ffffff", "border": "#e5e5e7", "sub_text": "#86868b",
        "input_bg": "#ffffff", "btn_primary": "#d97757", "accent": "#c66d4f",
        "shadow": "rgba(0,0,0,0.08)"
    }
}
t = themes[st.session_state.theme]

# ── Rotating quotes (no static greeting) ─────────────────────────────────────
QUOTES = [
    "Research is to see what everybody else has seen, and to think what nobody else has thought. — Albert Szent-Györgyi",
    "The important thing is not to stop questioning. — Albert Einstein",
    "An investment in knowledge pays the best interest. — Benjamin Franklin",
    "The goal is to turn data into information, and information into insight. — Carly Fiorina",
    "Without data, you're just another person with an opinion. — W. Edwards Deming",
    "Somewhere, something incredible is waiting to be known. — Sharon Begley",
    "Research is formalized curiosity. It is poking and prying with a purpose. — Zora Neale Hurston",
    "Information is not knowledge. — Albert Einstein",
    "Knowledge is of no value unless you put it into practice. — Anton Chekhov",
    "In God we trust; all others must bring data. — W. Edwards Deming",
]
if "current_quote" not in st.session_state:
    st.session_state.current_quote = random.choice(QUOTES)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', -apple-system, sans-serif; }}
.stApp {{ background-color: {t['bg']} !important; color: {t['text']} !important; }}
[data-testid="stHeader"] {{ background-color: transparent !important; }}
[data-testid="stSidebar"] {{ background-color: {t['bg_sidebar']} !important; border-right: 1px solid {t['border']}; }}
[data-testid="stSidebar"] * {{ color: {t['text']} !important; }}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span {{ color: {t['sub_text']} !important; }}
.stTextArea textarea {{
    background-color: {t['input_bg']} !important; color: {t['text']} !important;
    border: 1px solid {t['border']} !important; border-radius: 20px !important;
    padding: 1.5rem !important; font-size: 1.15rem !important;
    box-shadow: 0 4px 25px {t['shadow']} !important;
}}
[data-testid="stTextInput"] input {{
    background-color: {t['input_bg']} !important; color: {t['text']} !important;
    border: 1px solid {t['border']} !important; border-radius: 12px !important;
    padding-right: 3.5rem !important;
}}
button[aria-label="Show password"], button[aria-label="Hide password"] {{
    color: {t['sub_text']} !important; background: transparent !important; right: 10px !important;
}}
[data-testid="stSelectbox"] > div, [data-baseweb="select"] > div, [data-baseweb="select"] * {{
    background-color: {t['input_bg']} !important; color: {t['text']} !important;
    border-color: {t['border']} !important;
}}
[data-baseweb="popover"] *, [data-baseweb="menu"] * {{
    background-color: {t['input_bg']} !important; color: {t['text']} !important;
}}
label, .stLabel, [data-testid="stWidgetLabel"] {{ color: {t['text']} !important; }}
.stMarkdown a {{ color: {t['accent']} !important; text-decoration: underline; }}
/* Radio chip style */
[data-testid="stRadio"] [role="radiogroup"] {{ display: flex; justify-content: center; gap: 15px; margin-top: 10px; }}
[data-testid="stRadio"] [role="radiogroup"] label {{
    background-color: {t['card_bg']} !important; border: 1.5px solid {t['border']} !important;
    padding: 10px 24px !important; border-radius: 40px !important; cursor: pointer;
    transition: all 0.3s ease; color: {t['sub_text']} !important; font-weight: 500 !important;
}}
[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {{
    background-color: {t['btn_primary']} !important; border-color: {t['btn_primary']} !important;
    color: white !important; transform: translateY(-2px);
}}
/* Buttons */
div.stButton > button {{
    border-radius: 50px; font-weight: 600; padding: 0.8rem 2rem;
    background-color: {t['card_bg']} !important; color: {t['text']} !important;
    border: 1px solid {t['border']} !important; transition: all 0.2s ease;
}}
div.stButton > button:hover {{ border-color: {t['btn_primary']} !important; transform: translateY(-1px); }}
.main-btn div.stButton > button {{
    background-color: {t['btn_primary']} !important; color: white !important;
    border: none !important; padding: 1.2rem 4rem !important;
    font-size: 1.3rem !important; margin-top: 2rem;
    box-shadow: 0 10px 30px {t['btn_primary']}33 !important;
}}
/* Report card */
.report-card {{
    background-color: {t['card_bg']}; border: 1px solid {t['border']};
    border-radius: 30px; padding: 4rem; margin: 3rem 0;
    box-shadow: 0 20px 60px {t['shadow']};
}}
/* Status pill */
.status-pill {{
    display: inline-flex; align-items: center; padding: 6px 14px;
    border-radius: 100px; font-size: 0.85rem; font-weight: 600; margin-bottom: 2rem;
}}
.status-online {{ background: rgba(46,204,113,0.1); color: #2ecc71; border: 1px solid rgba(46,204,113,0.2); }}
.status-offline {{ background: rgba(231,76,60,0.1); color: #e74c3c; border: 1px solid rgba(231,76,60,0.2); }}
#MainMenu, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
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

    # Reads from env var — works on HF Spaces when API_URL secret is set
    API_URL = st.text_input(
        "Backend URL",
        value=os.getenv("API_URL", "http://localhost:8000"),
        help=(
            "The URL where your AI research engine is running. "
            "Use http://localhost:8000 for local dev. "
            "On HF Spaces, set the API_URL secret in Space settings."
        ),
    )

    API_KEY = st.text_input(
        "Access Key (X-API-Key)",
        value=os.getenv("API_KEY", "your-secret-api-key-change-this"),
        type="password",
        help=(
            "Security token sent with every request to authenticate with the backend. "
            "Must match the API_KEY environment variable on your server. "
            "On HF Spaces, set it as a Space secret."
        ),
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

# ── Hero — rotating quote only, no personal greeting ──────────────────────────
st.markdown(f"""
<div style='text-align:center; margin-top:4rem; margin-bottom:2rem;'>
    <p style='font-size:1.2rem; font-style:italic; color:{t['sub_text']};
              max-width:700px; margin:0 auto; line-height:1.6;'>
        "{st.session_state.current_quote}"
    </p>
</div>
""", unsafe_allow_html=True)

# ── Prebuilt question chips ───────────────────────────────────────────────────
st.markdown(f"<p style='text-align:center; color:{t['sub_text']}; font-size:0.9rem; font-weight:600; letter-spacing:0.08em;'>QUICK STARTERS</p>", unsafe_allow_html=True)

PRESET_QUERIES = [
    "Latest AI agent trends for Q1 2026",
    "Progress in quantum computing 2025",
    "LangGraph vs CrewAI for production agents",
    "Current state of commercial fusion energy",
    "Future of AI in healthcare diagnostics",
]

preset_cols = st.columns(len(PRESET_QUERIES))
for i, p in enumerate(PRESET_QUERIES):
    with preset_cols[i]:
        if st.button(p, key=f"pre_{i}", use_container_width=True):
            st.session_state.input_query = p
            st.rerun()

# ── Research input ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    query = st.text_area(
        label="Research Query",
        label_visibility="collapsed",
        value=st.session_state.input_query,
        placeholder="What topic should I investigate today?",
        key="research_area",
        height=120,
    )

    # Answer length — maps to backend schema Literal["short","medium","long"]
    st.markdown(
        f"<div style='text-align:center; color:{t['sub_text']}; font-size:0.95rem; "
        f"margin-top:2.5rem; font-weight:600; letter-spacing:0.1em;'>REPORT FIDELITY</div>",
        unsafe_allow_html=True,
    )
    length_map = {"⚡ Brief": "short", "📄 Detailed": "medium", "🔬 Deep Dive": "long"}
    length_choice = st.radio(
        "Length",
        options=list(length_map.keys()),
        index=1,
        horizontal=True,
        label_visibility="collapsed",
    )
    answer_length = length_map[length_choice]

    st.markdown('<div class="main-btn" style="text-align:center;">', unsafe_allow_html=True)
    if st.button("🚀 Synthesize Insights", key="go_btn"):
        if not query or len(query.strip()) < 10:
            st.warning("⚠️ Please enter a research question with at least 10 characters.")
        else:
            st.session_state.input_query = query.strip()
            with st.spinner(f"Scanning web for '{query.strip()}'…"):
                try:
                    resp = requests.post(
                        f"{API_URL}/research",
                        json={
                            "query": query.strip(),
                            "max_results": 5,
                            "answer_length": answer_length,   # ← matches backend schema
                        },
                        headers={"X-API-Key": API_KEY},
                        timeout=300,
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.results.append({
                            "query": query.strip(),
                            "report": data.get("response", ""),    # ← correct field name
                            "sources": data.get("sources", []),    # ← list of URL strings
                            "timestamp": datetime.now().strftime("%H:%M"),
                            "depth": answer_length,
                        })
                        # Rotate quote after each successful search
                        st.session_state.current_quote = random.choice(QUOTES)
                        st.rerun()
                    elif resp.status_code == 403:
                        st.error("🔒 Access Key invalid — check the sidebar.")
                    elif resp.status_code == 422:
                        st.error(f"❌ Validation error: {resp.json().get('detail', resp.text)}")
                    elif resp.status_code == 429:
                        st.error("❌ Rate limit hit — wait a moment and try again.")
                    else:
                        st.error(f"❌ Backend error {resp.status_code}: {resp.text[:300]}")
                except requests.exceptions.ConnectionError:
                    st.error("📡 Cannot connect to backend — check the Backend URL in the sidebar.")
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out (300 s). Backend may be overloaded.")
                except Exception as exc:
                    st.error(f"❌ Unexpected error: {exc}")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    st.markdown("<br><br><hr style='opacity:0.1'><br>", unsafe_allow_html=True)
    for res in reversed(st.session_state.results):
        depth_label = {"short": "BRIEF", "medium": "DETAILED", "long": "DEEP DIVE"}.get(res["depth"], res["depth"].upper())
        st.markdown(f"""
<div class="report-card">
    <div style="display:flex; justify-content:space-between; align-items:top;">
        <div>
            <h2 style="margin:0; font-size:2.2rem; font-weight:700;">📋 Research Report</h2>
            <p style="color:{t['sub_text']}; font-size:1.2rem; margin:0.5rem 0 0 0;">🔍 {res['query']}</p>
        </div>
        <div style="text-align:right;">
            <span style="background:{t['btn_primary']}22; color:{t['btn_primary']}; padding:6px 15px;
                         border-radius:20px; font-size:0.8rem; font-weight:700;">{depth_label}</span>
            <div style="color:{t['sub_text']}; font-size:0.9rem; margin-top:8px;">{res['timestamp']}</div>
        </div>
    </div>
    <hr style="border-color:{t['border']}; margin:2.5rem 0;">
    <div style="font-size:1.1rem; line-height:1.8;">
""", unsafe_allow_html=True)

        st.markdown(res["report"])

        if res.get("sources"):
            st.markdown("### 🔗 Sources")
            for i, src in enumerate(res["sources"]):
                if src:  # sources are plain URL strings from the backend
                    st.markdown(f"{i + 1}. [{src}]({src})")

        st.markdown("</div></div>", unsafe_allow_html=True)
