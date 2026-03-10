# Financial Data Skill - Quick Start

## ✅ Installation Complete

The financial data skill is now ready to use!

## 🚀 Quick Test

```bash
# Stock price
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py AAPL price

# Full quote
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py TSLA quote

# Comprehensive report
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py MSFT report

# Crypto (Bitcoin)
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py BTC crypto

# Historical data
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py SPY history --days 30

# Company news
python3 /data/.openclaw/workspace/skills/financial-data/fetch.py NVDA news
```

## 📊 Demo Output

Run the demo to see all features:
```bash
python3 /data/.openclaw/workspace/skills/financial-data/demo.py
```

## ⚙️ Configuration

### Current Setup
- **Data Source:** Yahoo Finance (FREE)
- **Delay:** 15-20 minutes (real-time data requires API key)
- **Cost:** $0/month

### Upgrade to Premium (Optional)
For real-time data and more features:
1. Sign up at https://www.financialdatasets.ai/
2. Set API key:
```bash
openclaw secret set FINANCIAL_DATASETS_API_KEY your_key_here
```
3. The skill will automatically use premium data

## 📁 Files

```
skills/financial-data/
├── SKILL.md          # Full documentation
├── fetch.py          # Main data fetching script
├── formatters.py     # Output formatting
├── config.yaml       # Configuration
├── demo.py           # Quick demo
└── logs/             # Log files
```

## 💡 Use Cases

1. **Pre-sales Research:** Check prospect's stock performance before calls
2. **Daily Briefings:** Automated market summaries
3. **Content Creation:** Market insights for LinkedIn/podcast
4. **Personal Tracking:** Portfolio monitoring

## 🎯 Next Steps

- Test it: `python3 demo.py`
- Try fetching your stocks
- Ask Jarvis to integrate it into workflows

**Ready to use!** 🚀
