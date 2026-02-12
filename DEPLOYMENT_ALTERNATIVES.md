# Alternative Deployment Options

Beyond Google Cloud Run, here are **free and low-cost** alternatives to deploy your AI Research Agent.

---

## 🚀 Option 1: Render.com (Easiest!)

**Pros:**
- ✅ Free tier available (750 hrs/month)
- ✅ Auto-deploy from GitHub
- ✅ Free SSL certificates
- ✅ Simple UI, no command line needed

**Cons:**
- ⚠️ Free tier spins down after 15 min of inactivity
- ⚠️ Limited to 512MB RAM on free tier

**Steps:**

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Name**: ai-research-agent
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
   - **Add Environment Variables**:
     - `GROQ_API_KEY`
     - `TAVILY_API_KEY`
6. Click "Create Web Service"

**URL**: `https://ai-research-agent.onrender.com`

---

## 🚀 Option 2: Railway.app

**Pros:**
- ✅ $5 free credit/month
- ✅ Auto-deploy from GitHub
- ✅ Great for Docker
- ✅ Built-in Redis support

**Cons:**
- ⚠️ Requires credit card for free tier
- ⚠️ Limited free credits

**Steps:**

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "Start a New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Railway auto-detects Dockerfile and deploys!
6. Add environment variables in dashboard:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`

**URL**: Auto-generated (e.g., `https://ai-research-agent-production.up.railway.app`)

---

## 🚀 Option 3: Hugging Face Spaces

**Pros:**
- ✅ 100% FREE forever
- ✅ Great for ML/AI projects
- ✅ Community visibility
- ✅ Gradio/Streamlit support

**Cons:**
- ⚠️ Better for frontends than APIs
- ⚠️ Limited to 16GB RAM

**Steps:**

1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space → Select "Docker"
3. Push your code to the Space repo
4. Add secrets in Space settings:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
5. Create `Dockerfile` (you already have it!)

**Alternative**: Use Gradio/Streamlit frontend instead of FastAPI

**URL**: `https://huggingface.co/spaces/yourusername/ai-research-agent`

---

## 🚀 Option 4: Fly.io

**Pros:**
- ✅ Generous free tier (3 VMs)
- ✅ Great for Docker
- ✅ Good performance
- ✅ Persistent volumes

**Cons:**
- ⚠️ Requires credit card
- ⚠️ Command-line based

**Steps:**

```bash
# Install flyctl
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
flyctl auth login

# Launch app
flyctl launch
# Answer prompts:
# - App name: ai-research-agent
# - Region: closest to you
# - Database: No

# Set secrets
flyctl secrets set GROQ_API_KEY=your_key
flyctl secrets set TAVILY_API_KEY=your_key

# Deploy
flyctl deploy
```

**URL**: `https://ai-research-agent.fly.dev`

---

## 🚀 Option 5: Heroku

**Pros:**
- ✅ Easy deployment
- ✅ Good documentation
- ✅ Add-ons ecosystem

**Cons:**
- ❌ No free tier anymore (starts at $7/month)
- ⚠️ More expensive than alternatives

**Steps:**

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create ai-research-agent

# Set environment variables
heroku config:set GROQ_API_KEY=your_key
heroku config:set TAVILY_API_KEY=your_key

# Deploy
git push heroku main
```

---

## 🚀 Option 6: DigitalOcean App Platform

**Pros:**
- ✅ $200 free credit for 60 days
- ✅ Auto-scaling
- ✅ Good for production

**Cons:**
- ⚠️ Costs $5/month after free trial
- ⚠️ Requires credit card

**Steps:**

1. Sign up at [digitalocean.com](https://www.digitalocean.com/)
2. Go to "App Platform"
3. Connect GitHub repo
4. Configure build:
   - **Resource Type**: Web Service
   - **Build Command**: Auto-detected
5. Add environment variables
6. Launch

---

## 🚀 Option 7: AWS Lightsail (Traditional VPS)

**Pros:**
- ✅ Full control
- ✅ $3.50/month
- ✅ 3 months free trial

**Cons:**
- ⚠️ Manual setup required
- ⚠️ Need to manage server

**Quick setup:**

```bash
# SSH into Lightsail instance
ssh ubuntu@your-instance-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repo
git clone https://github.com/yourusername/ai-research-agent
cd ai-research-agent

# Run with Docker
docker-compose up -d
```

---

## 📊 Comparison Table

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Render** | ✅ 750hrs/mo | ⭐⭐⭐⭐⭐ | Quick demos |
| **Railway** | $5/mo credit | ⭐⭐⭐⭐ | Docker apps |
| **Hugging Face** | ✅ Unlimited | ⭐⭐⭐⭐ | ML projects |
| **Fly.io** | ✅ 3 VMs | ⭐⭐⭐ | Production |
| **Heroku** | ❌ $7/mo | ⭐⭐⭐⭐⭐ | Paid option |
| **GCP Cloud Run** | ✅ 2M req/mo | ⭐⭐⭐ | Auto-scaling |
| **AWS Lightsail** | ✅ 3mo trial | ⭐⭐ | Full control |

---

## 🎯 My Recommendation

**For your use case (portfolio/demo):**

1. **Best FREE option**: **Render.com**
   - Easiest to set up
   - Good for demos
   - Free custom domain support

2. **Best for PRODUCTION**: **GCP Cloud Run**
   - Auto-scales to zero (cost-effective)
   - 2M free requests/month
   - Professional infrastructure

3. **Best for ML COMMUNITY**: **Hugging Face Spaces**
   - Great exposure
   - 100% free forever
   - Built for AI/ML projects

---

## 🚀 Quick Deploy to Render (5 minutes)

1. **Push to GitHub** (if not already)
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/ai-research-agent.git
   git push -u origin main
   ```

2. **Go to Render.com** → Sign up with GitHub

3. **Create Web Service** → Connect repo

4. **Configure**:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

5. **Add env vars** → Deploy!

Done! You'll have a live URL in ~5 minutes.

---

## 💡 Next Steps

1. ✅ Test locally first (run `python test_local.py`)
2. Choose deployment platform
3. Deploy
4. Test live URL
5. Add to portfolio with live demo link!

**Need help with any specific platform? Let me know!**
