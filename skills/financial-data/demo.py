#!/usr/bin/env python3
"""
Quick demo/test of financial data skill
"""

import sys
sys.path.insert(0, '/data/.openclaw/workspace/skills/financial-data')

from fetch import FinancialDataFetcher
from formatters import FinancialFormatter

def demo():
    print("🚀 Financial Data Skill Demo\n")
    
    fetcher = FinancialDataFetcher()
    formatter = FinancialFormatter()
    
    # Check data source
    if fetcher.use_premium:
        print("✅ Using Financial Datasets API (Premium)")
    else:
        print("ℹ️  Using Yahoo Finance (Free - 15-20min delay)")
    
    print("\n" + "="*50 + "\n")
    
    # Demo 1: Stock Price
    print("📊 DEMO 1: Apple (AAPL) Stock Price")
    print("-" * 40)
    data = fetcher.fetch_price("AAPL")
    if "error" not in data:
        print(formatter.format_price(data))
    else:
        print(f"❌ {data['error']}")
        print("💡 Tip: Install yfinance → pip install yfinance")
    
    print("\n" + "="*50 + "\n")
    
    # Demo 2: Full Quote
    print("📊 DEMO 2: Tesla (TSLA) Full Quote")
    print("-" * 40)
    data = fetcher.fetch_quote("TSLA")
    if "error" not in data:
        print(formatter.format_quote(data))
    else:
        print(f"❌ {data['error']}")
    
    print("\n" + "="*50 + "\n")
    
    # Demo 3: Comprehensive Report
    print("📊 DEMO 3: Microsoft (MSFT) Report")
    print("-" * 40)
    try:
        report = fetcher.generate_report("MSFT")
        print(report)
    except Exception as e:
        print(f"❌ {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("✅ Demo complete!")
    print("\nUsage examples:")
    print("  python3 fetch.py AAPL price")
    print("  python3 fetch.py TSLA quote")
    print("  python3 fetch.py BTC crypto")
    print("  python3 fetch.py NVDA report")
    print("  python3 fetch.py SPY history --days 30")

if __name__ == '__main__':
    demo()
