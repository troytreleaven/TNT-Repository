# Financial Data Skill

## What It Does
Fetches real-time and historical financial data including stock prices, crypto, financial statements, and company news. Integrates with financialdatasets.ai API (or free Yahoo Finance for testing).

## When to Use
- User asks about stock prices or market data
- Need financial data for sales research (pre-call prep)
- Content creation (podcast, LinkedIn posts with market insights)
- Personal investment tracking
- Business intelligence on corporate prospects

## How to Use

### Quick Fetch
```bash
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py <symbol> <data_type> [options]
```

### Examples
```bash
# Stock price
python3 skills/financial-data/fetch.py AAPL price

# Income statement
python3 skills/financial-data/fetch.py TSLA income

# Crypto price
python3 skills/financial-data/fetch.py BTC crypto

# Company news
python3 skills/financial-data/fetch.py NVDA news --days 7

# Historical prices
python3 skills/financial-data/fetch.py SPY history --days 30

# Full report
python3 skills/financial-data/fetch.py AAPL report
```

### Available Data Types
- `price` - Current stock price
- `quote` - Full quote (price, change, volume, etc.)
- `income` - Income statement
- `balance` - Balance sheet
- `cashflow` - Cash flow statement
- `history` - Historical prices
- `news` - Company news
- `crypto` - Cryptocurrency data
- `report` - Comprehensive summary

## Configuration

### Option 1: Financial Datasets API (Recommended)
1. Sign up at https://www.financialdatasets.ai/
2. Get API key
3. Set in OpenClaw:
```bash
openclaw secret set FINANCIAL_DATASETS_API_KEY your_key_here
```

### Option 2: Free Yahoo Finance (Testing)
No API key needed! Uses yfinance library.
```bash
pip install yfinance
```

## Data Sources

| Provider | Cost | Data Quality | Delay |
|----------|------|--------------|-------|
| Financial Datasets | ~$200/mo | Premium | Real-time |
| Yahoo Finance | Free | Good | 15-20 min |

## Output Formats

Default: Pretty-printed text for chat
Options: `--json` for raw data, `--csv` for spreadsheet export

## Integration with OpenClaw

### Cron Jobs
Daily market briefing:
```json
{
  "schedule": {"kind": "cron", "expr": "0 8 * * 1-5"},
  "payload": {
    "kind": "systemEvent",
    "text": "Run financial briefing"
  }
}
```

### Heartbeat Checks
Include portfolio performance in morning briefings.

### Memory Tracking
Save investment decisions and rationale to MEMORY.md.

## Files
- `fetch.py` - Main data fetching script
- `formatters.py` - Output formatting
- `config.yaml` - Configuration
- `SKILL.md` - This file

## Author
Built for Troy Treleaven / Dale Carnegie GTA
Date: March 2026
