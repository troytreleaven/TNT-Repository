#!/usr/bin/env python3
"""
Outlook Skill - Microsoft 365 via Graph API
"""

import os
import sys
import json
import requests
import msal
from datetime import datetime

# Config
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(SKILL_DIR, '.env')

def load_env():
    """Load credentials from .env file"""
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env[key] = val.strip().strip('"').strip("'")
    return env

def get_token(env):
    """Get access token using MSAL"""
    client_id = env.get('CLIENT_ID')
    client_secret = env.get('CLIENT_SECRET')
    tenant_id = env.get('TENANT_ID')
    
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=authority
    )
    
    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        print(f"Error getting token: {result.get('error', 'Unknown')}")
        print(result.get('error_description', ''))
        sys.exit(1)

def make_request(endpoint, token, method="GET", data=None, user=None):
    """Make Graph API request"""
    # Use /me for delegated, /users/{upn} for app-only
    if user and "/me/" in endpoint:
        endpoint = endpoint.replace("me/", f"users/{user}/")
    url = f"https://graph.microsoft.com/v1.0/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        resp = requests.get(url, headers=headers)
    elif method == "POST":
        resp = requests.post(url, headers=headers, json=data)
    elif method == "PATCH":
        resp = requests.patch(url, headers=headers, json=data)
    elif method == "DELETE":
        resp = requests.delete(url, headers=headers)
    
    if resp.status_code in [200, 201]:
        return resp.json() if resp.content else {}
    else:
        print(f"Error: {resp.status_code}")
        print(resp.text)
        return None

def cmd_emails(token, args, user):
    """List recent emails"""
    top = args[0] if args else "10"
    # Use users/{user}/messages for app-only auth
    endpoint = f"users/{user}/messages?$top={top}&$select=from,subject,receivedDateTime,isRead"
    result = make_request(endpoint, token, user=user)
    
    if result and 'value' in result:
        print(f"📧 Recent {len(result['value'])} email(s):\n")
        for i, msg in enumerate(result['value'], 1):
            read_status = "📬" if not msg.get('isRead', False) else "📧"
            subject = msg.get('subject', '(No subject)')
            from_name = msg.get('from', {}).get('emailAddress', {}).get('name', 'Unknown')
            date = msg.get('receivedDateTime', '')[:10]
            print(f"{read_status} #{i}: {from_name}")
            print(f"   Subject: {subject}")
            print(f"   Date: {date}")
            print()
    else:
        print("No emails found or error occurred")

def cmd_read_email(token, args, user):
    """Read specific email by ID"""
    if not args:
        print("Usage: read-email <message-id>")
        return
    
    msg_id = args[0]
    result = make_request(f"me/messages/{msg_id}", token, user=user)
    
    if result:
        print(f"From: {result.get('from', {}).get('emailAddress', {}).get('name', 'Unknown')}")
        print(f"To: {result.get('toRecipients', [{}])[0].get('emailAddress', {}).get('name', 'Unknown')}")
        print(f"Subject: {result.get('subject', '')}")
        print(f"Date: {result.get('receivedDateTime', '')}")
        print(f"\n--- Body Preview ---")
        body = result.get('body', {}).get('content', '')[:1000]
        print(body)
    else:
        print("Email not found or error occurred")

def cmd_events(token, args, user):
    """List calendar events"""
    endpoint = f"users/{user}/events?$top=10&$select=subject,start,end,location,isOnlineMeeting"
    result = make_request(endpoint, token, user=user)
    
    if result and 'value' in result:
        print(f"📅 Upcoming {len(result['value'])} event(s):\n")
        for i, evt in enumerate(result['value'], 1):
            subject = evt.get('subject', '(No title)')
            start = evt.get('start', {}).get('dateTime', '')[:16]
            end = evt.get('end', {}).get('dateTime', '')[:16]
            location = evt.get('location', {}).get('displayName', 'No location')
            online = "🖥️ Teams" if evt.get('isOnlineMeeting') else ""
            
            print(f"#{i}: {subject} {online}")
            print(f"   When: {start} - {end}")
            if location != 'No location':
                print(f"   Where: {location}")
            print()
    else:
        print("No events found or error occurred")

def cmd_create_event(token, args, user):
    """Create calendar event"""
    if len(args) < 3:
        print("Usage: create-event \"Title\" \"2026-03-10T14:00:00\" \"2026-03-10T15:00:00\"")
        print("Optional: create-event \"Title\" \"start\" \"end\" \"description\" \"location\"")
        return
    
    title = args[0]
    start = args[1]
    end = args[2]
    description = args[3] if len(args) > 3 else ""
    location = args[4] if len(args) > 4 else ""
    
    event = {
        "subject": title,
        "start": {"dateTime": start, "timeZone": "America/New_York"},
        "end": {"dateTime": end, "timeZone": "America/New_York"},
        "body": {"contentType": "text", "content": description},
        "location": {"displayName": location},
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }
    
    result = make_request("me/events", token, method="POST", data=event, user=user)
    
    if result and 'id' in result:
        print(f"✅ Event created: {title}")
        print(f"   ID: {result['id']}")
    else:
        print("❌ Failed to create event")

def cmd_whoami(token, args, user):
    """Get user info"""
    # For app-only, get user by principal name
    if user:
        result = make_request(f"users/{user}", token, user=user)
    else:
        result = make_request("me", token, user=user)
    
    if result:
        print(f"👤 Logged in as:")
        print(f"   Name: {result.get('displayName', 'Unknown')}")
        print(f"   Email: {result.get('mail', result.get('userPrincipalName', 'Unknown'))}")
        print(f"   ID: {result.get('id', 'Unknown')}")
    else:
        print("Error getting user info")

def cmd_send_email(token, args, user):
    """Send an email"""
    if len(args) < 2:
        print("Usage: send-email \"to@example.com\" \"Subject\" \"Body text\"")
        return
    
    to_email = args[0]
    subject = args[1]
    body = args[2] if len(args) > 2 else ""
    
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {"address": to_email}
                }
            ]
        },
        "saveToSentItems": "true"
    }
    
    result = make_request("me/sentMessages", token, method="POST", data=email_msg, user=user)
    
    if result and 'id' in result:
        print(f"✅ Email sent to {to_email}")
    else:
        print("❌ Failed to send email")

def main():
    env = load_env()
    
    if not env.get('CLIENT_ID') or not env.get('CLIENT_SECRET'):
        print("Error: Missing credentials in .env file")
        print(f"Expected file at: {ENV_FILE}")
        sys.exit(1)
    
    token = get_token(env)
    user = env.get('DEFAULT_USER', '')
    
    if len(sys.argv) < 2:
        print("Outlook Skill - Microsoft 365")
        print("Usage: python3 outlook.py <command> [args]")
        print()
        print("Commands:")
        print("  emails                    List recent emails")
        print("  read-email <id>           Read specific email")
        print("  events                    List calendar events")
        print("  create-event <title> <start> <end> [desc] [loc]  Create event")
        print("  send-email <to> <subject> <body>  Send email")
        print("  whoami                    Show current user")
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "emails": cmd_emails,
        "read-email": cmd_read_email,
        "events": cmd_events,
        "create-event": cmd_create_event,
        "send-email": cmd_send_email,
        "whoami": cmd_whoami,
    }
    
    if cmd in commands:
        commands[cmd](token, args, user)
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
