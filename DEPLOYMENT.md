# Production Deployment Guide - GCP Cloud Run

This guide will help you deploy your AI Research Agent to Google Cloud Run with production-grade configuration.

## 🎯 Why This is Production-Ready

Unlike typical student projects, this includes:
- ✅ **Auto-scaling infrastructure** (0 to N instances based on load)
- ✅ **Monitoring & Logging** (Cloud Logging, Prometheus metrics)
- ✅ **CI/CD Pipeline** (Automated builds on git push)
- ✅ **Rate limiting & Security** (Input validation, CORS, API key restrictions)
- ✅ **Cost optimization** (Free tier eligible, scales to zero)
- ✅ **WebSocket support** for streaming responses
- ✅ **Vector database** for semantic search (ChromaDB)
- ✅ **Production error handling** with retries and fallbacks

---

## 📋 Prerequisites

1. **Google Cloud Account** (free tier includes $300 credit)
2. **gcloud CLI** installed
3. **Docker** installed (for local testing)
4. **GitHub repo** (for CI/CD)

---

## 🚀 Step-by-Step Deployment

### Step 1: Set Up GCP Project

```bash
# Install gcloud CLI if not already installed
# Download from: https://cloud.google.com/sdk/docs/install

# Login to GCP
gcloud auth login

# Create new project (or use existing)
gcloud projects create ai-research-agent-prod --name="AI Research Agent"

# Set as active project
gcloud config set project ai-research-agent-prod

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 2: Store API Keys Securely

```bash
# Store Groq API key
echo -n "gsk_your_actual_groq_key" | gcloud secrets create groq-api-key --data-file=-

# Store Tavily API key
echo -n "tvly-your_actual_tavily_key" | gcloud secrets create tavily-api-key --data-file=-

# Grant Cloud Run access to secrets
PROJECT_NUMBER=$(gcloud projects describe ai-research-agent-prod --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding groq-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding tavily-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Step 3: Build and Push Docker Image

```bash
# Navigate to project directory
cd "d:\Projects\7 day Strike AI\Day01\ai-research-agent"

# Build the image
docker build -t gcr.io/ai-research-agent-prod/ai-research-agent:latest .

# Configure Docker to use gcloud
gcloud auth configure-docker

# Push to Google Container Registry
docker push gcr.io/ai-research-agent-prod/ai-research-agent:latest
```

### Step 4: Deploy to Cloud Run

```bash
gcloud run deploy ai-research-agent \
  --image gcr.io/ai-research-agent-prod/ai-research-agent:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --concurrency 80 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars REDIS_URL=redis://your-redis-instance:6379 \
  --set-secrets GROQ_API_KEY=groq-api-key:latest,TAVILY_API_KEY=tavily-api-key:latest
```

**You'll get a URL like:** `https://ai-research-agent-abcd1234-uc.a.run.app`

### Step 5: Set Up Custom Domain (Professional Touch!)

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service ai-research-agent \
  --domain api.yourcompany.com \
  --region us-central1
```

Follow the DNS configuration instructions provided.

### Step 6: Enable Cloud Logging & Monitoring

```bash
# Logs are automatically sent to Cloud Logging
# View real-time logs
gcloud run services logs tail ai-research-agent --region=us-central1

# Set up alerts (via GCP Console)
# Navigation: Cloud Monitoring > Alerting > Create Policy
# Alert on:
# - Error rate > 5%
# - Response time > 2s
# - Memory usage > 80%
```

---

## 🔧 CI/CD Setup (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

env:
  PROJECT_ID: ai-research-agent-prod
  SERVICE_NAME: ai-research-agent
  REGION: us-central1

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Cloud SDK
      uses: google-github-actions/setup-gcloud@v0
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ${{ env.PROJECT_ID }}
    
    - name: Configure Docker
      run: gcloud auth configure-docker
    
    - name: Build
      run: |
        docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA .
        docker tag gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
    
    - name: Push
      run: |
        docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA
        docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
    
    - name: Deploy
      run: |
        gcloud run deploy $SERVICE_NAME \
          --image gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
          --platform managed \
          --region $REGION \
          --allow-unauthenticated
```

---

## 📊 Production Enhancements

### 1. Add Redis for Session State (Optional but Professional)

```bash
# Use Google Cloud Memorystore
gcloud redis instances create ai-agent-redis \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_6_x

# Get the IP address
gcloud redis instances describe ai-agent-redis --region=us-central1 --format="value(host)"

# Update REDIS_URL in Cloud Run deployment
```

### 2. Add API Key Authentication

Create `src/api/auth.py`:

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import os

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    correct_api_key = os.getenv("API_KEY", "your-secure-api-key")
    if api_key != correct_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
```

Update `src/api/main.py`:

```python
from .auth import verify_api_key

@app.post("/research", dependencies=[Depends(verify_api_key)])
async def research_endpoint(...):
    ...
```

### 3. Add Health Check Endpoint (Already included!)

Your `/health` endpoint returns:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-11T12:00:00Z"
}
```

### 4. Add Prometheus Metrics Endpoint

Already included at `/metrics`! Exposes:
- Request count
- Request duration
- Error rates
- Active connections

---

## 🎨 Professional Frontend Deployment

Deploy the Streamlit frontend to **Streamlit Cloud** (free):

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo
4. Point to `frontend/app.py`
5. Add environment variables:
   - `API_URL=https://your-cloud-run-url.run.app`

---

## 💰 Cost Optimization

**Free Tier Eligible:**
- 2 million requests/month FREE
- 360,000 GB-seconds compute/month FREE
- 180,000 vCPU-seconds compute/month FREE

**Estimated costs after free tier:**
- ~$0.00002 per request
- ~$24/month for 100K requests

**Cost-saving tips:**
- Set `--min-instances 0` (scales to zero when idle)
- Use `--memory 1Gi` if 2Gi is overkill
- Clean up old container images regularly

---

## 🔒 Security Best Practices

1. **Never commit API keys** - Use Secret Manager
2. **Enable CORS properly** - Already configured in `main.py`
3. **Input validation** - Already implemented with Pydantic
4. **Rate limiting** - Already configured with SlowAPI
5. **HTTPS only** - Cloud Run enforces this automatically

---

## 📈 Monitoring Dashboard

Access via GCP Console:
- **Cloud Run Metrics**: Request count, latency, CPU, memory
- **Cloud Logging**: Search queries, filter errors
- **Trace**: Request traces for debugging slow queries

---

## 🎯 Going Beyond "Student Project"

**What makes this production-grade:**

1. ✅ **Scalable Infrastructure** - Auto-scales 0→N instances
2. ✅ **Observability** - Structured logging + metrics
3. ✅ **Error Handling** - Retries, circuit breakers, fallbacks
4. ✅ **Security** - Input validation, rate limiting, CORS
5. ✅ **CI/CD** - Automated deployments
6. ✅ **Documentation** - OpenAPI/Swagger docs
7. ✅ **Testing** - Unit + integration tests
8. ✅ **Professional API Design** - RESTful + WebSocket
9. ✅ **Cost-Effective** - Free tier eligible
10. ✅ **Custom Domain** - api.yourcompany.com

---

## 🚨 Troubleshooting

**Build fails:**
```bash
# Check logs
gcloud builds log --region=us-central1

# Test locally first
docker build -t test .
docker run -p 8000:8000 test
```

**Deployment fails:**
```bash
# Check service logs
gcloud run services logs read ai-research-agent --region=us-central1

# Check service details
gcloud run services describe ai-research-agent --region=us-central1
```

**High costs:**
```bash
# Check request count
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"'

# Reduce min instances
gcloud run services update ai-research-agent --min-instances=0
```

---

## 📝 Next Steps

1. ✅ Deploy to Cloud Run
2. Set up custom domain
3. Configure CI/CD with GitHub Actions
4. Deploy frontend to Streamlit Cloud
5. Set up monitoring alerts
6. Add API key authentication
7. Create professional README with architecture diagram
8. Record demo video
9. Add to portfolio with live link
10. Share on LinkedIn with Cloud Run metrics screenshot

**Your deployed API will look like:**
`https://api.yourcompany.com/docs` ← Professional & production-ready! 🚀
