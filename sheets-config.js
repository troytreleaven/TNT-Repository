// Configuration - Fill in your Google Cloud details
const SHEETS_CONFIG = {
    // Your Google Sheet ID (from the URL)
    // https://docs.google.com/spreadsheets/d/[THIS_PART]/edit
    SHEET_ID: '1Ih4QU2hPCJyZ43fwkJKsVKU95xtc-fD9',
    
    // Your API Key from Google Cloud Console
    // APIs & Services → Credentials → Create API Key
    API_KEY: 'AIzaSyA6Zw9IvxOgMIn1l5pZacg4-_lM7vUkfLM',
    
    // Sheet tab name
    SHEET_NAME: 'Pipeline',
    
    // OAuth Client ID (for full write access - see sheets-oauth-setup.md)
    CLIENT_ID: 'YOUR_OAUTH_CLIENT_ID_HERE'
};

// Don't edit below this line
if (typeof module !== 'undefined') {
    module.exports = SHEETS_CONFIG;
}