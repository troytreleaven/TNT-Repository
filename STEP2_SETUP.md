# Step 2: Google Sheets Sync - Setup Guide

## ✅ What's Been Added

Your dashboard now has:
- 📥 **"Load from Sheets"** button - Pulls data FROM Google Sheets
- 📤 **"Save to Sheets"** button - Exports to CSV (full sync requires OAuth setup)
- 📊 Auto-calculating totals and weighted forecasts
- 💾 Local storage persistence

## 🔧 What You Need To Do

### Quick Setup (5 minutes)

1. **Create a Google Sheet**
   - Go to sheets.google.com
   - Create new spreadsheet
   - Name it: "Troy's Pipeline"
   - Add headers in row 1:
     ```
     A1: Company | B1: Contact | C1: Value | D1: Probability | E1: Stage | F1: Notes
     ```

2. **Get Your Sheet ID**
   - Look at the URL: `https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit`
   - Copy that long string of characters

3. **Get API Key**
   - Go to https://console.cloud.google.com/
   - Select your project
   - APIs & Services → Credentials
   - Click "Create Credentials" → "API Key"
   - Copy the key

4. **Update sheets-config.js**
   Open `sheets-config.js` and replace:
   ```javascript
   SHEET_ID: 'YOUR_SHEET_ID_HERE',
   API_KEY: 'YOUR_API_KEY_HERE',
   ```

5. **Enable Google Sheets API**
   - In Google Cloud Console
   - APIs & Services → Library
   - Search "Google Sheets API" → Click "Enable"

6. **Share Your Sheet**
   - In your Google Sheet, click "Share"
   - Change from "Restricted" to "Anyone with the link can view"
   - (Or share with specific people)

### Full Bidirectional Sync (Optional - 15 minutes)

For writing data BACK to Sheets from the dashboard:

See `sheets-oauth-setup.md` for OAuth setup instructions.

## 🧪 Test It

1. Deploy your updated dashboard
2. Click "📥 Load from Sheets"
3. You should see your deals appear!
4. Click "📤 Save to Sheets" to export CSV

## 📝 How It Works

- **Reading**: Pulls data directly from your Google Sheet using the API
- **Writing**: Currently exports CSV (OAuth required for direct write)
- **Storage**: Also saves to browser localStorage for offline viewing

## 🚀 Next: Step 3

Once this is working, we'll add:
- Google Sheets as the **Kanban backend** (cards persist in Sheets)
- Real-time bidirectional sync
- Mobile-friendly updates

**Questions?** Just ask! 🎯
