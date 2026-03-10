#!/usr/bin/env python3
"""
Google Sheets Webhook Client for OpenClaw
Sends data to Google Apps Script webhook
"""

import requests
import json
import os
from typing import List, Dict, Optional

class GoogleSheetsWebhook:
    """Client for sending data to Google Sheets via webhook"""
    
    def __init__(self, webhook_url: str, secret: str):
        self.webhook_url = webhook_url
        self.secret = secret
        self.session = requests.Session()
    
    def create_sheet(self, sheet_name: str, headers: List[str]) -> Dict:
        """Create a new sheet with headers"""
        payload = {
            'secret': self.secret,
            'operation': 'createSheet',
            'sheetName': sheet_name,
            'headers': headers
        }
        return self._send_request(payload)
    
    def clear_and_write(self, sheet_name: str, headers: List[str], 
                        rows: List[List], currency_columns: Optional[List[int]] = None,
                        color_code_profit: bool = False, profit_column: int = None) -> Dict:
        """Clear sheet and write new data"""
        payload = {
            'secret': self.secret,
            'operation': 'clearAndWrite',
            'sheetName': sheet_name,
            'headers': headers,
            'rows': rows,
            'currencyColumns': currency_columns or [],
            'colorCodeProfit': color_code_profit,
            'profitColumn': profit_column
        }
        return self._send_request(payload)
    
    def append_data(self, sheet_name: str, rows: List[List],
                    currency_columns: Optional[List[int]] = None,
                    color_code_profit: bool = False, profit_column: int = None) -> Dict:
        """Append data to existing sheet"""
        payload = {
            'secret': self.secret,
            'operation': 'appendData',
            'sheetName': sheet_name,
            'rows': rows,
            'currencyColumns': currency_columns or [],
            'colorCodeProfit': color_code_profit,
            'profitColumn': profit_column
        }
        return self._send_request(payload)
    
    def update_cell(self, sheet_name: str, row: int, col: int, value) -> Dict:
        """Update a single cell"""
        payload = {
            'secret': self.secret,
            'operation': 'updateCell',
            'sheetName': sheet_name,
            'row': row,
            'col': col,
            'value': value
        }
        return self._send_request(payload)
    
    def _send_request(self, payload: Dict) -> Dict:
        """Send POST request to webhook"""
        try:
            response = self.session.post(
                self.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'status': 'error', 'message': str(e)}

# Example usage for Dale Carnegie Cost Analysis
def upload_cost_analysis(webhook_url: str, secret: str):
    """Upload the complete cost analysis to Google Sheets"""
    
    client = GoogleSheetsWebhook(webhook_url, secret)
    
    # Sheet 1: Fixed Costs
    fixed_costs_headers = ['Category', 'Annual Cost', 'Monthly Cost', '% of Total', 'Notes']
    fixed_costs_data = [
        ['Franchise Fee (16.5%)', 297000, 24750, '26.5%', 'Largest fixed cost'],
        ['Troy\'s Salary', 144000, 12000, '12.9%', ''],
        ['Kevin\'s Salary', 144000, 12000, '12.9%', ''],
        ['Credit Cards (Rooms + Subs)', 120000, 10000, '10.7%', ''],
        ['Customer Service Team', 96000, 8000, '8.6%', 'Philippines team'],
        ['Office Rent', 84000, 7000, '7.5%', ''],
        ['BDC Loan', 60000, 5000, '5.4%', ''],
        ['Amy\'s Salary', 60000, 5000, '5.4%', ''],
        ['Marketing (Bryce)', 48000, 4000, '4.3%', ''],
        ['Salesforce Licensing', 18000, 1500, '1.6%', ''],
        ['Accountant', 15000, 1250, '1.3%', ''],
        ['Office Expenses', 12000, 1000, '1.1%', ''],
        ['Trainer Development', 9996, 833, '0.9%', ''],
        ['Conference Travel', 9996, 833, '0.9%', ''],
        ['TOTAL FIXED COSTS', 1117992, 93166, '100%', '']
    ]
    
    result1 = client.clear_and_write(
        'Fixed Costs',
        fixed_costs_headers,
        fixed_costs_data,
        currency_columns=[1, 2]  # Format columns 1 and 2 as currency
    )
    print(f"Fixed Costs sheet: {result1}")
    
    # Sheet 2: Profit Scenarios
    profit_headers = ['# Boot Camps', 'Revenue', 'Variable Costs', 'Contribution', 'Fixed Costs', 'Net Profit']
    profit_data = [
        [1, 46400, 14400, 32000, 93166, -61166],
        [2, 92800, 28800, 64000, 93166, -29166],
        [3, 139200, 43200, 96000, 93166, 2834],
        [4, 185600, 57600, 128000, 93166, 34834],
        [5, 232000, 72000, 160000, 93166, 66834],
        [6, 278400, 86400, 192000, 93166, 98834],
        [7, 324800, 100800, 224000, 93166, 130834],
        [8, 371200, 115200, 256000, 93166, 162834],
        [9, 417600, 129600, 288000, 93166, 194834],
        [10, 464000, 144000, 320000, 93166, 226834],
        [11, 510400, 158400, 352000, 93166, 258834],
        [12, 556800, 172800, 384000, 93166, 290834]
    ]
    
    result2 = client.clear_and_write(
        'Profit Scenarios',
        profit_headers,
        profit_data,
        currency_columns=[1, 2, 3, 4, 5, 6],
        color_code_profit=True,
        profit_column=5  # Net Profit column (0-indexed)
    )
    print(f"Profit Scenarios sheet: {result2}")
    
    return {'fixed_costs': result1, 'profit_scenarios': result2}

if __name__ == '__main__':
    # Get from environment variables or replace with your values
    WEBHOOK_URL = os.getenv('GOOGLE_SHEETS_WEBHOOK_URL', 'YOUR_WEBHOOK_URL_HERE')
    SECRET = os.getenv('GOOGLE_SHEETS_SECRET', 'YOUR_SECRET_HERE')
    
    if WEBHOOK_URL == 'YOUR_WEBHOOK_URL_HERE':
        print("Error: Please set your webhook URL")
        print("Usage: export GOOGLE_SHEETS_WEBHOOK_URL='https://...'")
        exit(1)
    
    results = upload_cost_analysis(WEBHOOK_URL, SECRET)
    print("\nUpload complete!")
    print(json.dumps(results, indent=2))
