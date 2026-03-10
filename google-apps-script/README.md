# Google Apps Script Webhook for Sheets

Complete solution for pushing data from OpenClaw to Google Sheets via webhook.

## 🚀 Quick Start

### Step 1: Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Copy the Sheet ID from the URL:
   - URL: `https://docs.google.com/spreadsheets/d/1ABC123.../edit`
   - Sheet ID: `1ABC123...`

### Step 2: Create Apps Script

1. Go to [script.google.com](https://script.google.com)
2. Click "New Project"
3. Delete the default `myFunction()`
4. Copy and paste the code from `Code.gs`
5. **Configure the script:**
   - Replace `YOUR_SHEET_ID_HERE` with your Sheet ID
   - Replace `YOUR_SECRET_KEY_HERE` with a secure random string

### Step 3: Deploy as Web App

1. Click **Deploy** → **New deployment**
2. Click **Select type** → **Web app**
3. Configure:
   - **Description:** OpenClaw Sheets Integration
   - **Execute as:** Me (your email)
   - **Who has access:** Anyone
4. Click **Deploy**
5. Copy the **Web app URL** (looks like: `https://script.google.com/macros/s/ABC123/exec`)

### Step 4: Save Credentials

Add to your OpenClaw environment:

```bash
export GOOGLE_SHEETS_WEBHOOK_URL="https://script.google.com/macros/s/YOUR_ID/exec"
export GOOGLE_SHEETS_SECRET="your-secret-key-here"
```

Or save to `~/.bashrc` for persistence.

### Step 5: Test

```bash
cd /data/.openclaw/workspace/google-apps-script
python3 sheets_webhook_client.py
```

---

## 📁 Files

| File | Purpose |
|------|---------|
| `Code.gs` | Google Apps Script (run in Google's environment) |
| `sheets_webhook_client.py` | Python client (run from OpenClaw) |

---

## 🔒 Security

- **Secret key:** Required for all requests (basic authentication)
- **HTTPS:** All communication encrypted
- **No API keys stored:** Uses webhook URL + secret

---

## 📊 Supported Operations

### 1. Create Sheet
```python
client.create_sheet(
    sheet_name='My Data',
    headers=['Column A', 'Column B']
)
```

### 2. Clear and Write Data
```python
client.clear_and_write(
    sheet_name='My Data',
    headers=['Name', 'Amount'],
    rows=[['Troy', 50000], ['Kevin', 40000]],
    currency_columns=[1],  # Format as $
    color_code_profit=True,
    profit_column=1
)
```

### 3. Append Data
```python
client.append_data(
    sheet_name='My Data',
    rows=[['New Entry', 10000]],
    currency_columns=[1]
)
```

### 4. Update Single Cell
```python
client.update_cell(
    sheet_name='My Data',
    row=2,
    col=1,
    value='Updated Name'
)
```

---

## 🎨 Formatting Features

- **Headers:** Blue background, white text, bold
- **Currency:** Automatic $ formatting with commas
- **Profit coloring:** Red for negative, green for positive
- **Auto-resize:** Columns adjust to content

---

## 🔧 Troubleshooting

### "Invalid secret key"
- Check that secret in Python matches the script

### "Sheet not found"
- Ensure sheet name matches exactly (case-sensitive)

### "Script not found" or 404
- Re-deploy the web app (URLs change on new deployments)
- Make sure deployment is set to "Anyone" access

### Data not appearing
- Check script logs: View → Executions in Apps Script
- Verify Sheet ID is correct

---

## 📝 API Reference

### Request Format
```json
{
  "secret": "your-secret",
  "operation": "clearAndWrite",
  "sheetName": "Sheet1",
  "headers": ["Col1", "Col2"],
  "rows": [["A", 100], ["B", 200]],
  "currencyColumns": [1],
  "colorCodeProfit": true,
  "profitColumn": 1
}
```

### Response Format
```json
{
  "status": "success",
  "message": "Data written: 2 rows",
  "rowsWritten": 2
}
```

---

## 🔄 Re-deployment

If you edit the script, you MUST redeploy:

1. Save changes (Ctrl+S)
2. Click **Deploy** → **Manage deployments**
3. Click **Edit** (pencil icon)
4. Click **New version**
5. Click **Deploy**

The URL stays the same, but the code updates.

---

## 🎯 Use Cases

### Daily Reports
```python
# Automated daily report
client.append_data(
    sheet_name='Daily Sales',
    rows=[[today, revenue, expenses, profit]],
    currency_columns=[1, 2, 3]
)
```

### Cost Analysis
```python
# Full cost breakdown
client.clear_and_write(
    sheet_name='Cost Analysis',
    headers=['Category', 'Amount'],
    rows=cost_data,
    currency_columns=[1]
)
```

### Pipeline Tracking
```python
# Update specific deal
client.update_cell(
    sheet_name='Pipeline',
    row=deal_row,
    col=5,
    value='Closed Won'
)
```

---

## 💡 Tips

1. **Test first:** Use `testScript()` function in Apps Script
2. **Batch uploads:** Send multiple rows at once for efficiency
3. **Currency columns:** Always specify which columns contain money
4. **Color coding:** Enable for profit/loss columns for visual impact

---

## 📧 Support

If issues persist:
1. Check Apps Script execution logs
2. Verify webhook URL is accessible (try in browser)
3. Test with simple data first
4. Check Python script error messages

---

*Built for Troy Treleaven - Dale Carnegie Training*
