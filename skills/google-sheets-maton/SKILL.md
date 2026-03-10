---
name: google-sheets-maton
name: Create and manage Google Sheets via Maton API integration. Use when you need to push data to Google Sheets programmatically from OpenClaw.
metadata:
  openclaw:
    emoji: "📊"
    requires:
      env: ["MATON_API_KEY"]
---

# Google Sheets via Maton

Create and populate Google Sheets using the Maton API gateway.

## Status: 🔧 INVESTIGATION PHASE

**Working:** Excel file creation (local)
**Not Working:** Direct Maton API calls (auth issues)

## Connection Details

From `memory/secure-credentials.md`:

- **API Key:** `nJuhpgYhY2FOdPTgxn4vXX3IphpytjBPYoYi1EXQCKwZPn_fUpC3CJsyUUERId7Z08WSZlvRVVEf_tfQ17ZROCil58bCCzKryYRJE2xtWA`
- **Google Sheets Connection ID:** `c485f030-9fd7-4ead-a315-15393cccbe26`
- **Email:** ttreleaven@gmail.com

## API Investigation Log

### Attempted Endpoints

```bash
# Base URLs tried:
https://ctrl.maton.ai/api/v1/...
https://api.maton.ai/v1/...
https://maton.ai/api/v1/...
```

### Authentication Attempts

```bash
# Attempt 1: Bearer Token
Authorization: Bearer <token>
Result: "Invalid key=value pair (missing equal-sign)"

# Attempt 2: X-API-Key header
X-API-Key: <token>
Result: "Missing Authentication Token"

# Attempt 3: Connection-specific endpoint
/api/v1/connections/<id>
Result: Same auth error
```

### Error Analysis

The error message suggests Maton uses a different auth scheme:
```
"Invalid key=value pair (missing equal-sign) in Authorization header 
(hashed with SHA-256 and encoded with Base64)"
```

This implies:
1. Not standard Bearer token
2. Possibly requires signature-based auth
3. May need timestamp/nonce
4. Could be HMAC-SHA256 based

## Working Solution (Excel)

While Maton API is investigated, use Python `openpyxl`:

```bash
pip3 install openpyxl --user --break-system-packages
```

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Sheet1"

# Headers
ws['A1'] = "Category"
ws['B1'] = "Amount"
ws['A1'].font = Font(bold=True)

# Data
ws.append(["Rent", 84000])
ws.append(["Salaries", 144000])

# Formatting
for cell in ws['B']:
    if isinstance(cell.value, (int, float)):
        cell.number_format = '$#,##0'

wb.save('/output/file.xlsx')
```

## To Investigate Further

1. **Check Maton Documentation**
   - Find correct API base URL
   - Determine auth scheme (likely HMAC-SHA256)
   - Get proper endpoint paths

2. **Alternative: Google Drive API**
   - Upload Excel to Drive
   - Convert to Sheets
   - May be easier than direct Sheets API

3. **Alternative: Google Apps Script**
   - Create webhook endpoint
   - POST data to script
   - Script writes to Sheets

## Files Created

- `skills/google-sheets-maton/SKILL.md` - This file
- `Dale_Carnegie_Cost_Analysis.xlsx` - Working Excel version

## Next Steps

1. Contact Maton support for API docs
2. Try Google Drive upload API
3. Set up Google Apps Script webhook
4. Update this skill when working solution found

## Notes

- Excel files work immediately with openpyxl
- No auth needed for local Excel creation
- Excel can be manually uploaded to Google Sheets
- For automation, need to solve Maton auth or use alternative approach
