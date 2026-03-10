#!/usr/bin/env python3
"""
Google OAuth refresh token generator for OpenClaw
Uses Mission Control's existing credentials
"""
import os
import urllib.parse
import webbrowser

# Use Mission Control's credentials
CLIENT_ID = "794402546207-4t8268cm4nifv1i4308sem1hbp843u8e.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# OAuth scopes needed
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly"
]

# Build authorization URL
auth_url = (
    "https://accounts.google.com/o/oauth2/v2/auth?"
    + urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    })
)

print("=" * 60)
print("Google Calendar OAuth Setup for OpenClaw")
print("=" * 60)
print()
print("Step 1: Open this URL in your browser:")
print()
print(auth_url)
print()
print("Step 2: Sign in with your Google account and authorize access")
print()
print("Step 3: Copy the authorization code provided")
print()
print("Step 4: Run this command with the code:")
print()
print(f"python3 /data/.openclaw/workspace/get_refresh_token.py <auth_code>")
print()

# Try to open browser automatically
try:
    webbrowser.open(auth_url)
    print("✅ Browser opened automatically!")
except:
    print("⚠️  Please manually open the URL above in your browser")
