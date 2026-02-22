import streamlit as st
import requests
import json
import time

# Premium UI Configuration
st.set_page_config(
    page_title="isuru01online | Research Workspace",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #121212;
        border-right: 1px solid #262626;
    }
    
    .sidebar-nav-item {
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.2rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        color: #e5e5e5;
    }
    .sidebar-nav-item:hover {
        background-color: #1a1a1a;
    }
    .active-nav {
        background-color: #262626;
    }
    
    /* Quick Action Cards */
    .quick-action-card {
        background-color: #171717;
        border: 1px solid #262626;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.2s ease;
        cursor: pointer;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
    }
    
    .quick-action-card:hover {
        background-color: #1a1a1a;
        border-color: #404040;
    }
    
    .card-icon {
        font-size: 1.4rem;
    }
    
    .card-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: #d1d1d1;
    }
    
    /* Agent Box */
    .agent-header {
        font-size: 0.95rem;
        font-weight: 500;
        margin-top: 2.5rem;
        margin-bottom: 0.3rem;
    }
    .agent-sub {
        font-size: 0.85rem;
        color: #737373;
        margin-bottom: 1.2rem;
    }
    
    /* Input Workspace */
    .workspace-input {
        background-color: #171717;
        border: 1px solid #262626;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }
    
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        color: #f7f7f7 !important;
        font-size: 1rem !important;
        resize: none !important;
    }
    
    /* Chip Bar */
    .chip-bar {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }
    .chip {
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        background-color: #171717;
        border: 1px solid #262626;
        font-size: 0.82rem;
        color: #a3a3a3;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
    }
    .chip:hover {
        border-color: #404040;
        color: #e5e5e5;
    }
    .chip-active {
        background-color: #1e293b;
        color: #3b82f6;
        border-color: #1e3a8a;
    }
    
    /* Get Started Checklist */
    .checklist-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.5rem 0;
        color: #a3a3a3;
        font-size: 0.9rem;
    }
    .check-icon {
        color: #3b82f6;
        font-size: 1.2rem;
    }
    
    /* Usage Bars */
    .usage-label { font-size: 0.75rem; color: #737373; }
    .usage-metric { font-size: 0.85rem; font-weight: 500; margin-bottom: 2px; }
    .progress-track { height: 4px; background-color: #262626; border-radius: 2px; }
    .progress-fill { height: 100%; border-radius: 2px; }
    
    /* Research Reports */
    .report-card {
        background-color: #171717;
        border: 1px solid #262626;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-nav-item">isuru01online ⌄</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item active-nav">🏠 Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">📚 Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">🤖 Agent</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("##### Private")
    st.markdown('<div class="sidebar-nav-item">📁 Age reversal research</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("##### Plan usage")
    st.markdown('<div class="usage-metric">AI words/day <span style="float:right; color:#737373;">0/1000</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="progress-track"><div class="progress-fill" style="width: 5%; background-color: #238636;"></div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="usage-metric">Imports/day <span style="float:right; color:#737373;">0/5</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="progress-track"><div class="progress-fill" style="width: 10%; background-color: #238636;"></div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Upgrade", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">💬 Feedback</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-nav-item">❓ Support</div>', unsafe_allow_html=True)

    # Advanced Toggle
    with st.expander("Advanced Settings"):
        API_URL = st.text_input("API URL", "http://localhost:8000")
        PROVIDER = st.selectbox("LLM Provider", ["groq", "openai", "anthropic"], index=0)

# Main Workspace
st.markdown("##### Quick actions")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown('<div class="quick-action-card"><span class="card-icon">📤</span><span class="card-label">Upload</span></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="quick-action-card"><span class="card-icon">➕</span><span class="card-label">Create</span></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="quick-action-card"><span class="card-icon">📄</span><span class="card-label">Chat with file</span></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="quick-action-card"><span class="card-icon">📁</span><span class="card-label">Chat with folder</span></div>', unsafe_allow_html=True)

st.markdown('<div class="agent-header">Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="agent-sub">Understand, research and write about anything</div>', unsafe_allow_html=True)

# Input Workspace Container
with st.container():
    # Chip Selection
    st.markdown("""
    <div class="chip-bar">
        <div class="chip chip-active">@ Mention</div>
        <div class="chip">⚙️ GPT OSS</div>
        <div class="chip">📄 250 words ⌄</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text Area
    query_text = st.text_area(
        "Agent Input",
        placeholder="Enter your research query...",
        label_visibility="collapsed",
        key="query_input",
        height=70
    )
    
    # Submit Button
    sc1, sc2, sc3 = st.columns([8, 1, 1.2])
    with sc3:
        if st.button("🚀 Research", use_container_width=True):
            if query_text:
                with st.spinner("Processing deep retrieval..."):
                    try:
                        response = requests.post(f"{API_URL}/research", json={"query": query_text, "provider": PROVIDER}, timeout=90)
                        if response.status_code == 200:
                            data = response.json()
                            if "history" not in st.session_state: st.session_state.history = []
                            st.session_state.history.append({"query": query_text, "response": data.get('answer'), "sources": data.get('sources', []), "provider": PROVIDER})
                        else: st.error(f"API Error: {response.text}")
                    except Exception as e: st.error(f"Search failed: {e}")

# Ready-made Questions
st.markdown("<br>##### Suggested Research", unsafe_allow_html=True)
suggestions = ["Competitive analysis of 7B-class LLMs", "Latest breakthroughs in Agentic AI architecture", "Future of autonomous research systems"]
cols = st.columns(3)
for idx, s in enumerate(suggestions):
    with cols[idx]:
        if st.button(f"🔍 {s}", key=f"s_{idx}", use_container_width=True):
            # This doesn't auto-trigger yet but we show intent
            st.info(f"Setting query to: {s}")

# Get Started Guide
st.markdown("<br>##### Get started", unsafe_allow_html=True)
st.markdown('<div class="checklist-item"><span class="check-icon">✓</span> Chat with a file</div>', unsafe_allow_html=True)
st.markdown('<div class="checklist-item"><span class="check-icon">✓</span> Add files to a folder and chat with them</div>', unsafe_allow_html=True)
st.markdown('<div class="checklist-item"><span class="check-icon">✓</span> Create a new note</div>', unsafe_allow_html=True)
st.markdown('<div class="checklist-item"><span style="color:#737373;">○ Search for papers with agent</span></div>', unsafe_allow_html=True)
st.markdown('<div class="checklist-item"><span style="color:#737373;">○ Connect Zotero or Mendeley and import a file</span></div>', unsafe_allow_html=True)

# Reports History
if "history" in st.session_state and st.session_state.history:
    st.markdown("---")
    st.markdown("#### 📑 Intelligence Reports")
    for item in reversed(st.session_state.history):
        with st.container():
            st.markdown(f'<div class="report-card">', unsafe_allow_html=True)
            st.markdown(f"**Research Target:** {item['query']}")
            st.markdown("---")
            st.markdown(item['response'])
            if item['sources']:
                st.markdown("**Sources:** " + ", ".join([f"[{s.get('title', 'Ref')}]({s.get('url', '#')})" for s in item['sources'][:5]]))
            st.markdown('</div>', unsafe_allow_html=True)
