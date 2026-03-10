#!/usr/bin/env python3
"""
Output formatters for financial data
Converts raw data to human-readable formats
"""

import json
from typing import Dict, Any

class FinancialFormatter:
    """Format financial data for different outputs"""
    
    @staticmethod
    def format_price(data: Dict) -> str:
        """Format price data for chat"""
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        symbol = data.get('symbol', 'N/A')
        price = data.get('price', 'N/A')
        change = data.get('change', 0)
        change_pct = data.get('change_percent', 0)
        
        emoji = "🟢" if change >= 0 else "🔴"
        
        return f"""
{emoji} **{symbol}**
Price: ${price}
Change: {change:+.2f} ({change_pct:+.2f}%)
Volume: {data.get('volume', 'N/A'):,}
Source: {data.get('source', 'N/A')}
""".strip()
    
    @staticmethod
    def format_quote(data: Dict) -> str:
        """Format full quote"""
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        return f"""
📊 **{data.get('name', data.get('symbol', 'N/A'))} ({data.get('symbol', '')})**

💰 Price: ${data.get('price', 'N/A')} ({data.get('change_percent', 0):+.2f}%)
📈 Market Cap: {FinancialFormatter._format_market_cap(data.get('market_cap'))}
📊 P/E Ratio: {data.get('pe_ratio', 'N/A')}
📉 52-Week Range: ${data.get('52_week_low', 'N/A')} - ${data.get('52_week_high', 'N/A')}
🔄 Volume: {data.get('volume', 'N/A'):,}
""".strip()
    
    @staticmethod
    def format_history(data: Dict) -> str:
        """Format historical data summary"""
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        symbol = data.get('symbol', 'N/A')
        start = data.get('start_price', 0)
        end = data.get('end_price', 0)
        perf = data.get('performance', 0)
        
        emoji = "🟢" if perf >= 0 else "🔴"
        
        return f"""
📈 **{symbol} - {data.get('period', 'N/A')} History**

Start Price: ${start}
End Price: ${end}
Performance: {emoji} {perf:+.2f}%
Data Points: {data.get('data_points', 0)}

Source: {data.get('source', 'N/A')}
""".strip()
    
    @staticmethod
    def format_news(data: Dict) -> str:
        """Format news data"""
        if "error" in data:
            return f"❌ Error: {data['error']}"
        
        symbol = data.get('symbol', 'N/A')
        news_items = data.get('news', [])
        
        if not news_items:
            return f"📰 No recent news found for {symbol}"
        
        output = f"📰 **Latest News for {symbol}**\n\n"
        
        for i, item in enumerate(news_items[:5], 1):
            output += f"{i}. **{item.get('title', 'N/A')}**\n"
            output += f"   📰 {item.get('publisher', 'N/A')} | {item.get('published', 'N/A')}\n\n"
        
        return output.strip()
    
    @staticmethod
    def _format_market_cap(value):
        """Format market cap"""
        if value is None or value == 'N/A':
            return 'N/A'
        try:
            value = float(value)
            if value >= 1e12:
                return f"${value/1e12:.2f}T"
            elif value >= 1e9:
                return f"${value/1e9:.2f}B"
            elif value >= 1e6:
                return f"${value/1e6:.2f}M"
            else:
                return f"${value:,.0f}"
        except:
            return str(value)

if __name__ == '__main__':
    # Test formatters
    formatter = FinancialFormatter()
    
    test_price = {
        "symbol": "AAPL",
        "price": 175.50,
        "change": 2.50,
        "change_percent": 1.45,
        "volume": 50000000,
        "source": "Test"
    }
    
    print(formatter.format_price(test_price))
