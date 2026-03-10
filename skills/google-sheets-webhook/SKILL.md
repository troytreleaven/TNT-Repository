---
name: google-sheets-webhook
description: Send data from OpenClaw to Google Sheets via Google Apps Script webhook. Use when you need to programmatically create, update, or append data to Google Sheets without complex OAuth setup.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      env: ["GOOGLE_SHEETS_WEBHOOK_URL", "GOOGLE_SHEETS_SECRET"]
    files:
      - google-apps-script/Code.gs
      - google-apps-script/sheets_webhook_client.py
      - google-apps-script/README.md
---

# Google Sheets Webhook Integration

Push data from OpenClaw to Google Sheets via webhook - no complex OAuth required!

## Overview

This solution uses a **Google Apps Script web app** as a bridge:

```
OpenClaw → HTTP POST → Google Apps Script → Google Sheets
```

**Advantages:**
- No OAuth tokens to manage
- No API rate limits (Google handles it)
- Works from any environment
- Simple secret-key authentication

## Setup (One-Time)

### 1. Create Google Sheet
- Go to [sheets.google.com](https://sheets.google.com)
- Create new spreadsheet
- Copy the Sheet ID from URL

### 2. Deploy Apps Script
- Go to [script.google.com](https://script.google.com)
- New Project → Paste `Code.gs`
- Set `SHEET_ID` and `API_SECRET`
- Deploy → Web App → Execute as: Me, Access: Anyone
- Copy the webhook URL

### 3. Configure OpenClaw
```bash
export GOOGLE_SHEETS_WEBHOOK_URL="https://script.google.com/macros/s/.../exec"
export GOOGLE_SHEETS_SECRET="your-secret-key"
```

## Usage

### Python Client

```python
from sheets_webhook_client import GoogleSheetsWebhook

client = GoogleSheetsWebhook(
    webhook_url=os.getenv('GOOGLE_SHEETS_WEBHOOK_URL'),
    secret=os.getenv('GOOGLE_SHEETS_SECRET')
)

# Create sheet with headers
client.create_sheet('Cost Analysis', ['Category', 'Amount'])

# Write data with formatting
client.clear_and_write(
    sheet_name='Cost Analysis',
    headers=['Category', 'Annual', 'Monthly'],
    rows=[
        ['Rent', 84000, 7000],
        ['Salaries', 144000, 12000]
    ],
    currency_columns=[1, 2],  # Format as $
    color_code_profit=True    # Red negative, green positive
)

# Append more data
client.append_data('Cost Analysis', [['Marketing', 48000, 4000]])

# Update single cell
client.update_cell('Cost Analysis', row=2, col=2, value=90000)
```

### Command Line

```bash
# Upload cost analysis
python3 google-apps-script/sheets_webhook_client.py
```

## Operations

| Operation | Purpose |
|-----------|---------|
| `createSheet` | Create new sheet with headers |
| `clearAndWrite` | Clear sheet, write headers + data |
| `appendData` | Add rows to existing sheet |
| `updateCell` | Update single cell value |

## Formatting Options

- **currencyColumns:** Array of column indices to format as $
- **colorCodeProfit:** Color negative values red, positive green
- **profitColumn:** Which column contains profit values (for coloring)

## Security

- Secret key required in all requests
- HTTPS encrypted communication
- No credentials stored in code

## Files

- `Code.gs` - Apps Script (deploy to Google)
- `sheets_webhook_client.py` - Python client
- `README.md` - Full documentation

## Troubleshooting

**"Invalid secret key"**
→ Check secret matches between script and client

**"Sheet not found"**
→ Sheet name must match exactly (case-sensitive)

**404 or "Script not found"**
→ Re-deploy web app (URLs change)

**Data not appearing**
→ Check Apps Script execution logs

## Example: Dale Carnegie Cost Analysis

See `sheets_webhook_client.py` for complete working example that uploads:
- Fixed Costs sheet with $1.12M annual breakdown
- Profit Scenarios sheet with break-even analysis
- Proper currency formatting and color coding

---

*Simple webhook-based solution for Google Sheets integration*
