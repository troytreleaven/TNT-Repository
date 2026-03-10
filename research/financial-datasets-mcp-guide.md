# Financial Datasets MCP Server - Integration Guide

**Source:** X/Grok share from Troy Treleaven  
**Tool:** Financial Datasets MCP Server (financialdatasets.ai)  
**Purpose:** Real-time/historical financial data access via natural language  

---

## What It Does

Gives AI direct access to:
- Real-time & historical stock prices
- Income statements
- Balance sheets  
- Cash flow statements
- Company news
- Crypto data

All via natural language queries.

---

## MCP (Model Context Protocol) Explained

**MCP** = Standard protocol that lets Claude (and other AI) connect to external data sources  
**Think of it as:** USB-C for AI tools — universal connector standard

---

## Integration Options (Ranked by Complexity)

### Option 1: Official Remote/Hosted (Easiest)

**Setup:**
1. Sign up at https://www.financialdatasets.ai/
2. Get API key (plans start ~$200/mo)
3. In Claude Desktop:
   - Settings → Connectors → "Add custom connector"
   - URL: `https://mcp.financialdatasets.ai/mcp`
   - Authenticate via OAuth or API key
4. Start chatting — tools appear automatically

**Example Queries:**
- "Show me AAPL income statement for the last 3 years"
- "Compare TSLA and NVDA valuation multiples"  
- "What's the latest Bitcoin news and price movement?"
- "Get SPY historical prices Jan 2025 to now and plot trend"

---

### Option 2: Self-Host (More Control)

**GitHub:** https://github.com/financial-datasets/mcp-server

**Steps:**
```bash
# Clone repo
git clone https://github.com/financial-datasets/mcp-server

# Install dependencies
pip install -r requirements.txt

# Set API key
export FINANCIAL_DATASETS_API_KEY=your_key_here

# Run server
python server.py
```

**Connect to Claude Desktop:**
Edit `~/.config/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "financial-datasets-local": {
      "command": ["python", "/path/to/mcp-server/main.py"]
    }
  }
}
```

---

### Option 3: Free Alternatives (Budget-Friendly)

| Tool | Data Source | Cost |
|------|-------------|------|
| **mcp-yfinance** | Yahoo Finance | Free |
| **Alpha Vantage** | Multiple | Free tier |
| **EODHD** | Global markets | Freemium |
| **Finnhub** | Real-time | Freemium |

Search GitHub: `mcp-server finance` for more options.

---

## Important Notes

- **Not Actually Free:** Server code is open-source (MIT), but underlying data requires paid API key
- **Be Specific:** In prompts, mention "use financial data" to help Claude choose the right tool
- **Troubleshooting:** If tools don't appear, restart app, check console logs, or ask "list available tools"

---

## Use Cases for Dale Carnegie Business

### Personal Finance/Investment Tracking
- Monitor portfolio performance
- Track dividend income
- Analyze REIT investments

### Business Intelligence  
- Track competitor stock performance
- Monitor economic indicators affecting training industry
- Analyze corporate client financial health before sales calls

### Content Creation
- Financial data for podcast episodes
- Market insights for LinkedIn posts
- Industry trends for training content

---

## OpenClaw Integration Potential

See: `/data/.openclaw/workspace/research/openclaw-financial-integration.md` for full technical spec on how to wire this into OpenClaw workflows.

**Quick wins:**
- Create `skills/financial-data/` for OpenClaw
- Use financial data in heartbeat checks (market summary)
- Trigger alerts based on stock movements
- Generate weekly financial briefings

---

*Saved: March 1, 2026*  
*Status: Reference document for integration planning*
