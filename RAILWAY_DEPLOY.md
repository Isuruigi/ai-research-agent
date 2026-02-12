# 🚂 Railway Deployment Guide - AI Research Agent

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ Local app working (test with `python test_demo.py`)
- ✅ GROQ_API_KEY from your `.env` file
- ✅ TAVILY_API_KEY from your `.env` file
- ✅ GitHub account (for easiest deployment)

---

## 🚀 Method 1: Deploy via GitHub (Recommended - Easiest)

### Step 1: Push to GitHub

```bash
cd "d:\Projects\7 day Strike AI\Day01\ai-research-agent"

# Initialize git if not already
git init

# Add all files (excluding .env thanks to .gitignore)
git add .

# Commit
git commit -m "Initial commit: AI Research Agent"

# Create GitHub repo (via web):
# 1. Go to https://github.com/new
# 2. Name it: ai-research-agent
# 3. Don't initialize with README (we already have code)
# 4. Create repository

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-research-agent.git

# Push
git branch -M main
git push -u origin main
```

### Step 2: Create Railway Account

1. Visit **https://railway.app**
2. Click **"Login"**
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your GitHub

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: **`ai-research-agent`**
4. Railway will automatically detect the `Dockerfile` ✅

### Step 4: Configure Environment Variables

1. In Railway dashboard, click on your service
2. Click **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these variables:

```
GROQ_API_KEY = <paste your key from .env>
TAVILY_API_KEY = <paste your key from .env>
```

> **Important:** Don't include quotes, just paste the raw key

### Step 5: Deploy!

1. Railway will **automatically start building**
2. Watch the **"Deployments"** tab for progress
3. Build takes ~3-5 minutes
4. Look for **"Success"** ✅

### Step 6: Generate Public URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"**
3. Click **"Generate Domain"**
4. You'll get a URL like: `https://ai-research-agent-production-xxxx.up.railway.app`

### Step 7: Test Deployment

**Test Health Endpoint:**
```bash
curl https://your-app.up.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-12T..."
}
```

**Test API Docs:**
Visit in browser: `https://your-app.up.railway.app/docs`

**Test Research Query:**
```powershell
$body = @{
    query = "What is artificial intelligence?"
    max_results = 3
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-app.up.railway.app/research" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

---

## 🚀 Method 2: Deploy via Railway CLI (No GitHub needed)

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

Or download from: https://docs.railway.app/develop/cli

### Step 2: Login

```bash
railway login
```

This opens browser for authentication.

### Step 3: Initialize Project

```bash
cd "d:\Projects\7 day Strike AI\Day01\ai-research-agent"
railway init
```

Choose: **"Create new project"**

### Step 4: Set Environment Variables

```bash
railway variables set GROQ_API_KEY=your_actual_key_here
railway variables set TAVILY_API_KEY=your_actual_key_here
```

### Step 5: Deploy

```bash
railway up
```

This uploads your code and starts deployment.

### Step 6: Get URL

```bash
railway domain
```

This generates and shows your public URL.

---

## 🔧 Update Frontend to Use Deployed API

### Edit `frontend/script.js`

**Find line 2:**
```javascript
const API_URL = 'http://localhost:8000';
```

**Change to:**
```javascript
const API_URL = 'https://your-app.up.railway.app'; // Replace with your Railway URL
```

### Update CORS in Backend

**Edit `src/api/main.py`**

Find the CORS middleware (around line 40):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this
    ...
)
```

**Change to:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://your-app.up.railway.app",  # Your Railway URL
        "file://",  # For local file:// access
    ],
    ...
)
```

**Commit and push:**
```bash
git add .
git commit -m "Update CORS for production"
git push
```

Railway will auto-deploy the update!

---

## ✅ Verification Checklist

After deployment, test these:

- [ ] **Health Check**: `curl https://your-app.up.railway.app/health` returns 200
- [ ] **API Docs**: `https://your-app.up.railway.app/docs` loads Swagger UI
- [ ] **Metrics**: `https://your-app.up.railway.app/metrics` shows metrics
- [ ] **Research Query**: POST to `/research` returns response with sources
- [ ] **Frontend Works**: Local `frontend/index.html` can call deployed API

---

## 🐛 Troubleshooting

### Build Fails

**Error: "requirements.txt not found"**
- Make sure `requirements.txt` is in root directory
- Check Railway logs for specific error

**Error: "Docker build failed"**
- Verify `Dockerfile` is valid
- Check Railway build logs (click "Deployments" → latest build → "View Logs")

### Runtime Errors

**Error: "GROQ_API_KEY not found"**
- Check environment variables in Railway dashboard
- Make sure there are no quotes around the key
- Redeploy: Click "Deployments" → "⋯" → "Redeploy"

**Error: "Application crashed"**
- Check Runtime logs in Railway
- Common issue: Missing dependency in `requirements.txt`

### CORS Errors from Frontend

**Error: "blocked by CORS policy"**
- Update `allow_origins` in `main.py` with your Railway URL
- Commit and push changes
- Railway will auto-redeploy

**Quick fix:**
```python
allow_origins=["*"]  # Allow all (not recommended for production, but works for testing)
```

### No Response / Timeout

**Issue: Query takes too long**
- Railway free tier has 512MB RAM limit
- Large responses might timeout
- Try reducing `max_results` to 3

---

## 💰 Railway Pricing

- **Hobby Plan**: $5/month
- **First 500 hours**: Free trial credit
- **What you get**:
  - Auto-scaling
  - 512MB RAM (Hobby)
  - Public HTTPS URL
  - Automatic SSL
  - GitHub auto-deploy

**Monitoring usage:**
- Railway Dashboard → "Usage" tab
- Shows compute hours, network egress

---

## 🎯 Post-Deployment Steps

### 1. Update Your Resume/Portfolio

```
AI Research Agent
Live Demo: https://your-app.up.railway.app/docs
GitHub: https://github.com/YOUR_USERNAME/ai-research-agent
```

### 2. Share on LinkedIn

```
🚀 Just deployed my AI Research Agent to production!

Live at: https://your-app.up.railway.app/docs

Try asking it any research question - it searches the web in real-time
and provides citations.

Built with LangGraph, FastAPI, deployed on Railway.

#AI #MachineLearning #LangChain
```

### 3. Update README.md

Add deployment section:
```markdown
## 🚀 Live Demo

- **API Documentation**: https://your-app.up.railway.app/docs
- **Health Check**: https://your-app.up.railway.app/health
```

---

## 📊 Monitoring Your Deployment

### View Logs

**Railway Dashboard:**
1. Click on your service
2. Click "Deployments"
3. Click on latest deployment
4. Click "View Logs"

**Watch for:**
- `INFO:     Application startup complete.` ✅
- `INFO:     Uvicorn running on http://0.0.0.0:8000` ✅
- Any errors or warnings

### Metrics

Visit: `https://your-app.up.railway.app/metrics`

Shows:
- Request counts
- Response times
- Error rates

---

## 🔄 Redeployment

### Automatic (with GitHub)

Just push changes:
```bash
git add .
git commit -m "Updated feature"
git push
```

Railway automatically rebuilds and deploys! 🎉

### Manual (with CLI)

```bash
railway up
```

---

## 🎉 Success!

Your AI Research Agent is now:
- ✅ Deployed to production
- ✅ Publicly accessible via HTTPS
- ✅ Auto-scaling
- ✅ Monitored
- ✅ Ready to demo!

**Next Steps:**
1. Test the deployed API
2. Update frontend
3. Share with the world!
4. Add to portfolio

---

**Need help?** Check Railway docs: https://docs.railway.app
