# Claude API Configuration (Alternative to Groq)

If you want to use Claude API instead of Groq (good for testing with remaining credits!):

## Setup

1. Add your Claude API key to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
# Comment out or remove GROQ_API_KEY to use Claude instead
```

2. Install Anthropic SDK:
```bash
pip install anthropic langchain-anthropic
```

3. Update `src/agent/nodes.py` to support both:

```python
import os
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic

# Auto-detect which API to use
if os.getenv("ANTHROPIC_API_KEY"):
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",  # or claude-3-haiku for cheaper
        temperature=0.7,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    print("✅ Using Claude API")
elif os.getenv("GROQ_API_KEY"):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )
    print("✅ Using Groq API")
else:
    raise ValueError("No API key found! Set ANTHROPIC_API_KEY or GROQ_API_KEY")
```

## Cost Comparison

**Claude API:**
- Claude 3.5 Sonnet: $3/M input tokens, $15/M output tokens
- Claude 3 Haiku: $0.25/M input tokens, $1.25/M output tokens
- Your $3 credit = ~1M tokens with Haiku

**Groq (Current):**
- FREE tier available
- Very fast inference

**Recommendation:** Use Claude for testing if you have credits, then switch to Groq for production (free + fast).

## Quick Switch

Just set the env var and restart:

```bash
# Use Claude
ANTHROPIC_API_KEY=your-key

# Use Groq  
GROQ_API_KEY=your-key
```

The code will auto-detect which to use!
