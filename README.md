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

Production-ready AI Research Agent built with LangGraph + RAG for comprehensive web research.

## Features

* **Multi-stage research pipeline** (search → scrape → synthesize)
* **Vector storage** with ChromaDB for context retrieval
* **Streaming responses** via WebSocket
* **Rate limiting** and input validation
* **Session-based conversation memory**

## Usage

### Health Check
```bash
curl https://YOUR_USERNAME-ai-research-agent.hf.space/health
```

### API Documentation
Visit: `https://YOUR_USERNAME-ai-research-agent.hf.space/docs`

### Research Query
```bash
curl -X POST https://YOUR_USERNAME-ai-research-agent.hf.space/research \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"query":"What is artificial intelligence?","max_results":5}'
```

## Tech Stack

* **LLM**: Groq (Llama)
* **Embeddings**: HuggingFace
* **Vector DB**: ChromaDB
* **Framework**: LangChain + LangGraph
* **API**: FastAPI
* **Deployment**: Hugging Face Spaces (Docker)

## Configuration

Set these secrets in Space Settings:
- `GROQ_API_KEY` - Groq API key
- `TAVILY_API_KEY` - Tavily search API key
- `API_KEY` - Your custom API authentication key

## License

MIT
