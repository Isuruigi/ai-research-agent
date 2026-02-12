# 🎬 Quick Demo Recording Script

## FASTEST PATH: 2-Minute Portfolio Video

### Before Recording

1. **Start the server:**
   ```bash
   cd "d:\Projects\7 day Strike AI\Day01\ai-research-agent"
   venv\Scripts\activate
   uvicorn src.api.main:app --reload
   ```

2. **Open frontend:**
   - Double-click `frontend\index.html` in browser
   - Test with query: "What are the latest breakthroughs in quantum computing?"

3. **Recording tool options:**
   - **Easiest**: Press `Win + G` (Windows Game Bar) → Click Record
   - **Best free**: Download [OBS Studio](https://obsproject.com/)
   - **Quick online**: [Loom](https://loom.com) (5 min free)

---

## 📝 Exact Script to Say

```
[0:00-0:15 - INTRO]
"Hi, I'm [Name]. This is my AI Research Agent. 

Unlike ChatGPT which uses pre-trained data from months ago,
this searches the web in real-time and provides verifiable sources."

[0:15-0:25 - SHOW INTERFACE]
"Here's the interface - clean, minimal design.
It clearly states: this is a Web Research Agent."

[Click example prompt or type your own]

[0:25-1:00 - WATCH IT WORK]
"Watch it work - you can see the three stages:
First, searching the web with Tavily API...
Then extracting content from multiple sources...
Finally, synthesizing the research report..."

[Wait for response - about 15-20 seconds]

[1:00-1:30 - SHOW RESPONSE]
"And here's the comprehensive response.
Notice the sources at the bottom - every answer
includes citations so you can verify the information."

[Click one source link to show it opens]

[1:30-1:55 - TECHNICAL]
"Technically, I built this with:
- LangGraph for the multi-stage orchestration
- Tavily API for real-time web search  
- ChromaDB for vector storage and RAG
- FastAPI backend with rate limiting
- Deployed on Google Cloud Run"

[1:55-2:00 - OUTRO]
"Full code is on GitHub - link in the description.
Thanks for watching!"
```

---

## 🎯 Three Demo Queries to Use

Pick ONE that sounds natural to you:

1. **Current Events** (shows it's really live):
   > "What are the most recent developments in artificial intelligence this week?"

2. **Technical Topic** (shows depth):
   > "What are the latest breakthroughs in quantum computing?"

3. **Trending** (relatable):
   > "What are the key features of LangGraph for building AI agents?"

---

## ⏱️ Recording Timeline

```
0:00 ────────┐
             │ [INTRO - 15s]
0:15 ────────┤
             │ [SHOW UI - 10s]
0:25 ────────┤
             │ [WATCH SEARCH - 35s]
1:00 ────────┤
             │ [SHOW RESULTS - 30s]
1:30 ────────┤
             │ [TECH STACK - 25s]
1:55 ────────┤
             │ [OUTRO - 5s]
2:00 ────────┘
```

---

## ✅ Pre-Recording Checklist

- [ ] Server running (`http://localhost:8000/health` returns 200)
- [ ] Frontend opens without errors
- [ ] Test query works (DO A DRY RUN!)
- [ ] Close all personal apps/tabs
- [ ] Good audio (test mic)
- [ ] Practice script 2-3 times
- [ ] Have water nearby

---

## 🎥 Recording Steps (Windows Game Bar - Easiest)

1. Press `Win + G`
2. Click the record button (white circle)
3. Do your demo
4. Press `Win + G` again, click stop
5. Video saved to: `%USERPROFILE%\Videos\Captures\`

---

## 🎬 Recording Steps (OBS Studio - Professional)

1. Download: https://obsproject.com/
2. Install and open OBS
3. Sources → Add → Display Capture
4. Settings → Output → Recording Quality: "High Quality, Medium File Size"
5. Click "Start Recording"
6. Do your demo
7. Click "Stop Recording"
8. Videos saved to: `%USERPROFILE%\Videos\`

---

## 📤 After Recording

### Quick Edits (Optional)
- Trim beginning/end (use Windows Photos app)
- Add title card with your name
- Speed up 1.5x during the 15s research wait

### Where to Upload
1. **YouTube** (unlisted) - Put link on resume
2. **LinkedIn Video Post** (native upload)
3. **Portfolio website** (embed YouTube)
4. **Google Drive** (share link with recruiters)

---

## 💼 LinkedIn Post Template

```
🚀 Just built an AI Research Agent that searches the web in real-time

Most AI relies on training data that's months old.
Mine searches the internet NOW and provides verifiable sources.

Watch the demo 👇
[Attach your video]

Tech stack:
✅ LangGraph (multi-agent orchestration)
✅ Tavily API (real-time web search)
✅ ChromaDB (vector storage for RAG)
✅ FastAPI backend
✅ Google Cloud Run deployment

Processing time: ~15 seconds per query
Use case: Research requiring current information

GitHub: [your link]

#AI #MachineLearning #LangChain #Portfolio
```

---

## 🎤 If You Don't Want to Record Your Voice

**Option A: Text Overlays**
- Record without audio
- Add text captions explaining each step
- Add background music

**Option B: AI Voice**
- Use [ElevenLabs](https://elevenlabs.io/) (free tier)
- Type your script → Generate voice
- Add to video in editing

---

## ⚡ SPEEDRUN: 30-Minute Version

```
✅ [5 min] Practice demo 2-3 times
✅ [2 min] Record (Win + G)
✅ [3 min] Watch & re-record if needed
✅ [5 min] Quick trim in Windows Photos
✅ [5 min] Upload to YouTube (unlisted)
✅ [10 min] Write LinkedIn post & publish
```

**Total: 30 minutes from zero to LinkedIn post!**

---

## 🆘 Troubleshooting

**"Server not responding during recording"**
→ Do a test run first. Make sure API keys are set.

**"Recording is laggy"**
→ Close other apps. Lower OBS quality to "Indistinguishable Quality, Small File Size"

**"I messed up mid-recording"**
→ Just pause, take a breath, continue. Edit out the pause later.

**"Voice sounds bad"**
→ Use phone earbuds as mic. Way better than laptop mic.

---

**Ready? Let's do this! 🎬**

1. Start server
2. Open frontend  
3. Press Win+G
4. Hit record
5. Follow script
6. Upload

You got this! 💪
