# OpenClaw + Financial Data Integration Strategy

**Date:** March 1, 2026  
**Context:** Troy wants to use Financial Datasets MCP server within OpenClaw/Jarvis  
**Goal:** Map MCP capabilities to OpenClaw architecture

---

## The Challenge

**MCP (Model Context Protocol)** is Anthropic's standard for connecting Claude to external tools.  
**OpenClaw** uses a different architecture (skills-based, function calling).

**The Gap:** MCP servers don't plug directly into OpenClaw... but we can bridge them.

---

## Architecture Comparison

| Feature | MCP (Claude) | OpenClaw |
|---------|--------------|----------|
| **Protocol** | Model Context Protocol | Function calling + skills |
| **Discovery** | Automatic tool discovery | Explicit skill definitions |
| **Configuration** | `claude_desktop_config.json` | `SKILL.md` + code |
| **Hosting** | Local or remote | Local (workspace) |
| **Flexibility** | Claude-centric | Multi-agent, multi-model |

---

## Integration Options (3 Approaches)

### Approach 1: Skill Wrapper (Recommended)

**Concept:** Create an OpenClaw skill that calls the Financial Datasets API directly

**Structure:**
```
skills/
└── financial-data/
    ├── SKILL.md
    ├── fetch_stock.py
    ├── fetch_crypto.py
    └── config.json
```

**How it works:**
1. User asks: "What's AAPL trading at?"
2. Jarvis loads `financial-data` skill
3. Skill makes direct API call to financialdatasets.ai
4. Returns formatted data

**Pros:**
- Native OpenClaw integration
- No MCP server needed
- Works with any model (Kimi, GPT, etc.)
- Full control over data flow

**Cons:**
- Need to build the skill
- Manual API integration

**Cost:** Just the API subscription (~$200/mo)

---

### Approach 2: MCP Bridge (Intermediate)

**Concept:** Run MCP server locally, bridge to OpenClaw via HTTP/stdio

**Architecture:**
```
User → OpenClaw → MCP Bridge → MCP Server → Financial Data API
```

**Implementation:**
1. Run `financial-datasets/mcp-server` locally
2. Create OpenClaw skill that spawns MCP server process
3. Communicate via stdin/stdout or HTTP
4. Parse MCP responses back to OpenClaw

**Pros:**
- Leverages existing MCP server code
- Less custom development
- Follows emerging standard

**Cons:**
- More complex architecture
- Process management overhead
- Debugging is harder

**Best for:** When MCP ecosystem matures

---

### Approach 3: Claude Desktop + OpenClaw Hybrid (Immediate)

**Concept:** Use Claude Desktop for financial queries, OpenClaw for everything else

**Workflow:**
1. Financial questions → Claude Desktop with MCP
2. Business tasks → OpenClaw/Jarvis
3. Use sessions_spawn to coordinate between them

**Example:**
```
Troy: "Get TSLA financials and draft a LinkedIn post about it"

Jarvis (OpenClaw):
1. Spawn Claude Desktop session
2. Get TSLA data via MCP
3. Receive results back
4. Draft LinkedIn post
5. Send to Troy
```

**Pros:**
- Works TODAY
- No coding required
- Best of both worlds

**Cons:**
- Two interfaces
- Session coordination complexity
- Not seamless

---

## Recommended: Approach 1 (Direct Skill)

### Phase 1: MVP Skill (Week 1)

**File:** `skills/financial-data/SKILL.md`
```markdown
# Financial Data Skill

## What It Does
Fetch stock prices, financial statements, and crypto data from financialdatasets.ai

## When to Use
- When user asks about stocks, crypto, or financial data
- For investment tracking
- For business intelligence on corporate clients

## How to Use
Run: python3 skills/financial-data/fetch.py <symbol> <data_type>
```

**File:** `skills/financial-data/fetch.py`
```python
#!/usr/bin/env python3
import requests
import os
import sys

API_KEY = os.getenv('FINANCIAL_DATASETS_API_KEY')
BASE_URL = 'https://api.financialdatasets.ai'

def fetch_stock_price(symbol):
    url = f'{BASE_URL}/prices/{symbol}'
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_income_statement(symbol):
    url = f'{BASE_URL}/financials/income/{symbol}'
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

# ... more functions

if __name__ == '__main__':
    symbol = sys.argv[1]
    data_type = sys.argv[2]
    # Route to appropriate function
```

**Setup:**
```bash
# Add API key to OpenClaw secrets
openclaw secret set FINANCIAL_DATASETS_API_KEY your_key_here
```

### Phase 2: Enhanced Features (Week 2-3)

**Add capabilities:**
- Portfolio tracking (save watchlists)
- Alerts (notify when stocks hit thresholds)
- Reports (weekly market summary)
- Visualization (generate charts)

**Integration points:**
- **Cron jobs:** Daily market briefing at 8 AM
- **Heartbeat:** Include portfolio performance check
- **Memory:** Track investment decisions and rationale
- **Sessions:** Spawn financial analysis sub-agents

### Phase 3: Advanced Workflows (Month 2)

**Use cases:**
1. **Pre-sales Research:**
   - Before calling corporate prospect
   - Pull their stock performance, recent news
   - Generate talking points

2. **Content Creation:**
   - "This week's market moves" podcast segment
   - LinkedIn posts tied to financial trends

3. **Personal Finance:**
   - Monthly investment reports
   - Dividend tracking
   - Tax prep assistance

4. **Business Intelligence:**
   - Track competitor performance
   - Industry trend analysis
   - Economic indicator monitoring

---

## Cost Analysis

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Financial Datasets API | ~$200 | Required for real-time data |
| OpenClaw hosting | $0 | Already running |
| Development time | 4-8 hours | One-time skill build |
| **Total Ongoing** | **$200/mo** | Just the API subscription |

**ROI Potential:**
- Better informed sales calls → higher close rates
- Automated content generation → time savings
- Investment insights → better personal finance decisions

---

## Next Steps

1. **Decision:** Which approach? (Recommend: Direct Skill)
2. **API Key:** Sign up at financialdatasets.ai
3. **Development:** Build MVP skill (~2-4 hours)
4. **Testing:** Validate with sample queries
5. **Integration:** Add to daily workflows

**Immediate Action:**
I can start building the skill right now if you:
1. Provide API key (or I can guide signup)
2. Tell me which data types are priority (stocks, crypto, news, etc.)
3. Define first use case (portfolio tracking, sales research, content, etc.)

---

## Alternative: Free Yahoo Finance Skill

If $200/mo is steep for testing, I can build a Yahoo Finance skill first:
- Uses free yfinance Python library
- No API costs
- Good for testing workflows
- Upgrade to Financial Datasets later for better data quality

**Trade-offs:**
- Yahoo data is delayed (15 min)
- Less reliable
- Rate limits
- But: FREE for testing

---

*Ready to build this when you are!* 🚀
