# 🚀 Quick Deploy to Railway

## Step 1: Create GitHub Repo

**Repository Details:**
- **Name**: `ai-research-agent`
- **Description**: `Real-time AI research agent with web search, RAG, and source citations. Built with LangGraph + FastAPI.`
- **Visibility**: Public (code is public, but API requires key)

Go to: https://github.com/new

## Step 2: Push to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-research-agent.git
git push -u origin main
```

## Step 3: Deploy to Railway

1. Visit **https://railway.app** → Login with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select: **`ai-research-agent`**
4. Railway auto-deploys! ✅

## Step 4: Add Environment Variables

In Railway dashboard → Variables tab → Add:

```
GROQ_API_KEY=<your-groq-key>
TAVILY_API_KEY=<your-tavily-key>
API_KEY=<create-your-own-secret-key>
```

**Important:** Create a strong `API_KEY` (at least 32 characters)

Example:
```
API_KEY=sk_research_agent_2026_abc123xyz789
```

## Step 5: Get Your URL

Settings → Generate Domain

Your API will be at: `https://your-app.up.railway.app`

## Step 6: Update Frontend

Edit `frontend/script.js`:

```javascript
const API_URL = 'https://your-app.up.railway.app';
const API_KEY = 'sk_research_agent_2026_abc123xyz789'; // Match Railway
```

## Step 7: Test

```bash
curl -X POST https://your-app.up.railway.app/research \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{"query":"What is AI?","max_results":3}'
```

---

## 🔐 Security Notes

- ✅ API requires `X-API-Key` header (private)
- ✅ Internal docs excluded from GitHub
- ✅ `.env` file never committed
- ✅ Rate limiting: 10 requests/minute

---

**Total time: ~10 minutes** 🚀
