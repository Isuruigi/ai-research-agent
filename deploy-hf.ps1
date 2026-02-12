# Deploy AI Research Agent to Hugging Face Spaces
# Run this script from the ai-research-agent directory

Write-Host "🤗 Deploying to Hugging Face Spaces..." -ForegroundColor Cyan

# Step 1: Clone the Space
Write-Host "`n📥 Cloning HF Space..." -ForegroundColor Yellow
cd "d:\Projects\7 day Strike AI\Day01"
git clone https://huggingface.co/spaces/isuruig/ai-research-agent hf-space

# Step 2: Copy project files
Write-Host "`n📁 Copying project files..." -ForegroundColor Yellow
cd hf-space

# Copy main files
Copy-Item "..\ai-research-agent\Dockerfile" -Destination "." -Force
Copy-Item "..\ai-research-agent\requirements.txt" -Destination "." -Force
Copy-Item "..\ai-research-agent\README_HF.md" -Destination "README.md" -Force

# Copy source code
if (Test-Path "src") { Remove-Item "src" -Recurse -Force }
Copy-Item "..\ai-research-agent\src" -Destination "." -Recurse -Force

# Copy .env.example
Copy-Item "..\ai-research-agent\.env.example" -Destination ".env" -Force

Write-Host "✅ Files copied successfully!" -ForegroundColor Green

# Step 3: Git add and commit
Write-Host "`n📤 Committing changes..." -ForegroundColor Yellow
git add .
git commit -m "Deploy AI Research Agent"

# Step 4: Push to HF Space
Write-Host "`n🚀 Pushing to Hugging Face..." -ForegroundColor Yellow
Write-Host "You will be prompted for your HF token. Generate one at: https://huggingface.co/settings/tokens" -ForegroundColor Cyan
git push

Write-Host "`n✅ Deployment initiated!" -ForegroundColor Green
Write-Host "`n⏱️  Build will take ~5-10 minutes. Check: https://huggingface.co/spaces/isuruig/ai-research-agent" -ForegroundColor Cyan
Write-Host "`n🔑 Next: Add secrets in Space Settings:" -ForegroundColor Yellow
Write-Host "  - GROQ_API_KEY" -ForegroundColor White
Write-Host "  - TAVILY_API_KEY" -ForegroundColor White
Write-Host "  - API_KEY" -ForegroundColor White
