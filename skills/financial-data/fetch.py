#!/usr/bin/env python3
"""
Financial Data Fetcher
Fetches stock, crypto, and financial data from multiple sources
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, Optional

# Try to import financialdatasets client
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Try to import yfinance (free alternative)
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

class FinancialDataFetcher:
    def __init__(self):
        self.api_key = os.getenv('FINANCIAL_DATASETS_API_KEY')
        self.base_url = 'https://api.financialdatasets.ai'
        self.use_premium = bool(self.api_key)
        
    def fetch_price(self, symbol: str) -> Dict:
        """Fetch current stock price"""
        if self.use_premium and HAS_REQUESTS:
            return self._fetch_premium_price(symbol)
        elif HAS_YFINANCE:
            return self._fetch_yfinance_price(symbol)
        else:
            return {"error": "No data source available. Install yfinance or set FINANCIAL_DATASETS_API_KEY"}
    
    def _fetch_premium_price(self, symbol: str) -> Dict:
        """Fetch from Financial Datasets API"""
        url = f"{self.base_url}/prices/{symbol}"
        headers = {'X-API-KEY': self.api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"API Error: {str(e)}"}
    
    def _fetch_yfinance_price(self, symbol: str) -> Dict:
        """Fetch from Yahoo Finance (free)"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                return {"error": f"No data found for {symbol}"}
            
            latest = hist.iloc[-1]
            
            return {
                "symbol": symbol,
                "price": round(latest['Close'], 2),
                "change": round(latest['Close'] - latest['Open'], 2),
                "change_percent": round(((latest['Close'] - latest['Open']) / latest['Open']) * 100, 2),
                "volume": int(latest['Volume']),
                "high": round(latest['High'], 2),
                "low": round(latest['Low'], 2),
                "open": round(latest['Open'], 2),
                "source": "Yahoo Finance",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"Yahoo Finance Error: {str(e)}"}
    
    def fetch_quote(self, symbol: str) -> Dict:
        """Fetch full quote with additional data"""
        if HAS_YFINANCE:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                return {
                    "symbol": symbol,
                    "name": info.get('longName', 'N/A'),
                    "price": info.get('currentPrice', info.get('regularMarketPrice', 'N/A')),
                    "change": info.get('regularMarketChange', 'N/A'),
                    "change_percent": info.get('regularMarketChangePercent', 'N/A'),
                    "market_cap": info.get('marketCap', 'N/A'),
                    "pe_ratio": info.get('trailingPE', 'N/A'),
                    "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
                    "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
                    "volume": info.get('volume', 'N/A'),
                    "avg_volume": info.get('averageVolume', 'N/A'),
                    "source": "Yahoo Finance",
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            return self.fetch_price(symbol)
    
    def fetch_history(self, symbol: str, days: int = 30) -> Dict:
        """Fetch historical prices"""
        if not HAS_YFINANCE:
            return {"error": "yfinance not installed. Run: pip install yfinance"}
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=f"{days}d")
            
            if hist.empty:
                return {"error": f"No historical data for {symbol}"}
            
            data = []
            for date, row in hist.iterrows():
                data.append({
                    "date": date.strftime('%Y-%m-%d'),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2),
                    "volume": int(row['Volume'])
                })
            
            return {
                "symbol": symbol,
                "period": f"{days} days",
                "data_points": len(data),
                "start_price": data[0]['close'] if data else None,
                "end_price": data[-1]['close'] if data else None,
                "performance": round(((data[-1]['close'] - data[0]['close']) / data[0]['close']) * 100, 2) if data else None,
                "history": data,
                "source": "Yahoo Finance"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def fetch_crypto(self, symbol: str) -> Dict:
        """Fetch cryptocurrency data"""
        # Yahoo Finance format for crypto: BTC-USD, ETH-USD
        if not symbol.endswith('-USD') and not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"
        
        return self.fetch_price(symbol)
    
    def fetch_news(self, symbol: str, days: int = 7) -> Dict:
        """Fetch company news"""
        if not HAS_YFINANCE:
            return {"error": "yfinance not installed"}
        
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if not news:
                return {"symbol": symbol, "news": [], "message": "No recent news found"}
            
            # Filter by date if possible
            filtered_news = []
            for item in news[:10]:  # Top 10 stories
                filtered_news.append({
                    "title": item.get('title', 'N/A'),
                    "publisher": item.get('publisher', 'N/A'),
                    "published": item.get('published', 'N/A'),
                    "link": item.get('link', 'N/A')
                })
            
            return {
                "symbol": symbol,
                "count": len(filtered_news),
                "news": filtered_news
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_report(self, symbol: str) -> str:
        """Generate comprehensive text report"""
        quote = self.fetch_quote(symbol)
        
        if "error" in quote:
            return f"❌ Error fetching data for {symbol}: {quote['error']}"
        
        report = f"""
📊 **{quote.get('name', symbol)} ({symbol})**

💰 **Price Data**
• Current Price: ${quote.get('price', 'N/A')}
• Change: {quote.get('change', 'N/A')} ({quote.get('change_percent', 'N/A')}%)
• Day Range: ${quote.get('low', 'N/A')} - ${quote.get('high', 'N/A')}

📈 **Key Metrics**
• Market Cap: ${self._format_number(quote.get('market_cap'))}
• P/E Ratio: {quote.get('pe_ratio', 'N/A')}
• 52-Week Range: ${quote.get('52_week_low', 'N/A')} - ${quote.get('52_week_high', 'N/A')}
• Volume: {self._format_number(quote.get('volume'))}

⏰ Data as of: {quote.get('timestamp', 'N/A')}
🌐 Source: {quote.get('source', 'N/A')}
"""
        return report.strip()
    
    def _format_number(self, num):
        """Format large numbers"""
        if num is None or num == 'N/A':
            return 'N/A'
        try:
            num = float(num)
            if num >= 1e12:
                return f"{num/1e12:.2f}T"
            elif num >= 1e9:
                return f"{num/1e9:.2f}B"
            elif num >= 1e6:
                return f"{num/1e6:.2f}M"
            else:
                return f"{num:,.0f}"
        except:
            return str(num)

def main():
    parser = argparse.ArgumentParser(description='Fetch financial data')
    parser.add_argument('symbol', help='Stock/crypto symbol (e.g., AAPL, BTC)')
    parser.add_argument('type', help='Data type: price, quote, history, news, crypto, report')
    parser.add_argument('--days', type=int, default=30, help='Days for historical data')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    fetcher = FinancialDataFetcher()
    
    # Route to appropriate method
    if args.type == 'price':
        data = fetcher.fetch_price(args.symbol)
    elif args.type == 'quote':
        data = fetcher.fetch_quote(args.symbol)
    elif args.type == 'history':
        data = fetcher.fetch_history(args.symbol, args.days)
    elif args.type == 'news':
        data = fetcher.fetch_news(args.symbol, args.days)
    elif args.type == 'crypto':
        data = fetcher.fetch_crypto(args.symbol)
    elif args.type == 'report':
        print(fetcher.generate_report(args.symbol))
        return
    else:
        print(f"❌ Unknown data type: {args.type}")
        print("Available: price, quote, history, news, crypto, report")
        sys.exit(1)
    
    # Output
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        if "error" in data:
            print(f"❌ {data['error']}")
        else:
            print(json.dumps(data, indent=2))

if __name__ == '__main__':
    main()
