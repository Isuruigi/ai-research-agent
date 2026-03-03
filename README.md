---
title: AI Research Agent API
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# 🔬 AI Research Agent API

An AI Research Agent built with **LangGraph** and **Retrieval-Augmented Generation (RAG)** for web research.

The agent searches the web, scrapes content, stores it in a local vector database for semantic retrieval, and synthesizes answers, streaming the results back via WebSocket.

---

## 🏗️ Architecture & Features

* **Multi-stage Research Pipeline (LangGraph):** The agent decides when to search, what to read, and how to synthesize the final answer.
* **Web Search Integration:** Uses [Tavily](https://tavily.com) for web search results.
* **Vector Storage (RAG):** Uses [ChromaDB](https://www.trychroma.com/) and HuggingFace embeddings (`all-MiniLM-L6-v2`) to chunk, store, and retrieve context from scraped web pages.
* **Real-time Streaming:** Uses WebSockets (`FastAPI`) to stream the LLM's thought process and response tokens to the frontend.
* **Memory & State:** Maintains session-based conversational memory, allowing for follow-up questions on the research context.
* **Rate Limiting:** Built-in IP-based rate limiting.

---

## 🛠️ Tech Stack

* **LLM Engine:** Groq (Llama 3 / Mixtral), OpenAI (GPT-4o), or Anthropic (Claude 3.5 Sonnet) depending on config
* **Framework:** LangChain + LangGraph
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`sentence-transformers`)
* **Backend Backend:** FastAPI + Uvicorn + WebSockets
* **Deployment:** Hugging Face Spaces (Docker)

---

## 📁 Project Structure

```
ai-research-agent/
├── src/
│   ├── agent/                 # Core LangGraph state machine & logic
│   │   ├── graph.py           # The LangGraph workflow definitions
│   │   ├── nodes.py           # Individual steps (search, scrape, generate)
│   │   └── state.py           # State management for the graph
│   ├── api/                   # FastAPI backend
│   │   ├── main.py            # Entry point & WebSocket handling
│   │   ├── dependencies.py    # Rate limiting & Auth
│   │   └── routes.py          # REST endpoints
│   ├── core/                  # Configuration & common utilities
│   │   ├── config.py          # Environment variables parsing
│   │   └── llm.py             # Groq LLM initialization
│   ├── database/              # Vector DB management
│   │   └── vector_store.py    # ChromaDB integration
│   ├── memory/                # Conversation history
│   │   └── conversation.py    # SQLite/In-memory chat history
│   └── tools/                 # External integrations
│       ├── web_search.py      # Tavily search wrapper
│       └── web_scraper.py     # BeautifulSoup HTML extraction
├── frontend/                  # Simple HTML/JS/CSS streaming UI
├── Dockerfile                 # Container configuration for deployment
├── requirements.txt           # Python dependencies
└── .env.example               # Template for environment secrets
```

---

## 🚀 Local Development Setup

### 1. Prerequisites
You need Python 3.10+ installed on your machine.

### 2. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/7-day-strike-ai.git
cd "7-day-strike-ai/Day01/ai-research-agent"

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Fill in the API keys in your `.env` file depending on which provider you want to use:

**Choose Your LLM Provider:**
- `OPENAI_API_KEY`: Get from [platform.openai.com](https://platform.openai.com/) (For ChatGPT)
- `ANTHROPIC_API_KEY`: Get from [console.anthropic.com](https://console.anthropic.com/) (For Claude)
- `GROQ_API_KEY`: Get from [console.groq.com](https://console.groq.com/) (For extremely fast Llama inference)

**Required Core Keys:**
- `TAVILY_API_KEY`: Get from [tavily.com](https://tavily.com/)
- `API_KEY`: Create your own secret string (e.g., `my-super-secret-key`) to secure your API endpoints.

### 4. Run the Server
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`. You can test the frontend by opening `http://localhost:8000` in your web browser.

---

## ☁️ Deployment (Hugging Face Spaces)

This project can be deployed to **Hugging Face Spaces (Docker)**.

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces) and select **Docker** as the SDK.
2. Push this repository to the Space.
3. Go to the Space **Settings** -> **Variables and secrets**.
4. Add your API Keys as **Secrets** (depending on your choice of LLM):
   - `OPENAI_API_KEY` (if using ChatGPT models)
   - `ANTHROPIC_API_KEY` (if using Claude models)
   - `GROQ_API_KEY` (if using Groq models)
   - `TAVILY_API_KEY` (Required for web search)
   - `API_KEY` (Required to secure your API endpoint)

The Dockerfile will build and start the FastAPI server on port `7860`.

---

## 📖 API Usage Example

If you want to integrate this agent into another application via REST instead of WebSockets:

```bash
curl -X POST https://YOUR_USERNAME-ai-research-agent.hf.space/research \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"query":"What are the latest advancements in solid-state batteries?","max_results":5}'
```

## License
MIT
