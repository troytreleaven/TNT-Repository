#!/usr/bin/env python3
"""
Alex Chen - Gmail API Integration
Official Google Gmail API for sending/receiving emails
"""

import os
import sys
import json
import base64
from datetime import datetime
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]

class AlexChenGmailAPI:
    """Gmail API integration for Alex Chen"""
    
    def __init__(self):
        self.skill_dir = os.path.dirname(os.path.abspath(__file__))
        self.credentials_file = os.path.join(self.skill_dir, 'credentials.json')
        self.token_file = os.path.join(self.skill_dir, 'token.json')
        self.service = None
        self.user_email = "alex.chen.dc.gta@gmail.com"
        
        if not os.path.exists(self.credentials_file):
            raise ValueError(f"❌ credentials.json not found at {self.credentials_file}")
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, get them
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token for future runs
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        return True
    
    def get_auth_url(self):
        """Get authorization URL for manual authentication"""
        from google_auth_oauthlib.flow import Flow
        
        flow = Flow.from_client_secrets_file(
            self.credentials_file,
            scopes=SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Out-of-band (manual copy-paste)
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            login_hint=self.user_email
        )
        
        return auth_url, flow
    
    def save_token_from_code(self, flow, code):
        """Save token from authorization code"""
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        with open(self.token_file, 'w') as token:
            token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        return True
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> dict:
        """Send an email using Gmail API"""
        try:
            if not self.service:
                self.authenticate()
            
            # Create message
            message = MIMEText(body, 'html' if html else 'plain')
            message['to'] = to
            message['from'] = self.user_email
            message['subject'] = subject
            
            # Encode for API
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return {
                "status": "success",
                "id": result['id'],
                "from": self.user_email,
                "to": to,
                "subject": subject,
                "sent_at": datetime.now().isoformat()
            }
            
        except HttpError as error:
            return {
                "status": "error",
                "error": f"HTTP {error.resp.status}: {error._get_reason()}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def check_inbox(self, max_results: int = 10) -> dict:
        """Check inbox for recent emails"""
        try:
            if not self.service:
                self.authenticate()
            
            # Get messages
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                labelIds=['INBOX']
            ).execute()
            
            messages = results.get('messages', [])
            
            emails = []
            for msg in messages:
                # Get message details
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                
                # Extract headers
                headers = message['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                
                emails.append({
                    'id': msg['id'],
                    'from': sender,
                    'subject': subject,
                    'snippet': message.get('snippet', '')
                })
            
            return {
                "status": "success",
                "count": len(emails),
                "emails": emails
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

def setup_auth():
    """Setup authentication - generates URL for user to visit"""
    alex = AlexChenGmailAPI()
    auth_url, flow = alex.get_auth_url()
    
    # Save flow for later
    flow_data = {
        'client_config': flow.client_config,
        'scopes': flow.oauth2session.scope,
        'redirect_uri': flow.redirect_uri
    }
    flow_file = os.path.join(alex.skill_dir, 'flow_state.json')
    with open(flow_file, 'w') as f:
        json.dump(flow_data, f)
    
    print("=" * 60)
    print("🔗 AUTHORIZATION REQUIRED")
    print("=" * 60)
    print("\n1. Open this URL in your browser:")
    print(f"\n{auth_url}\n")
    print("2. Log in as: alex.chen.dc.gta@gmail.com")
    print("3. Click 'Allow' to grant permissions")
    print("4. Copy the authorization code")
    print("5. Paste it here\n")
    print("=" * 60)
    
    return auth_url, flow

def complete_auth(code: str):
    """Complete authentication with code"""
    alex = AlexChenGmailAPI()
    
    # Recreate flow
    flow_file = os.path.join(alex.skill_dir, 'flow_state.json')
    if not os.path.exists(flow_file):
        print("❌ No flow state found. Run setup first.")
        return False
    
    with open(flow_file, 'r') as f:
        flow_data = json.load(f)
    
    from google_auth_oauthlib.flow import Flow
    flow = Flow.from_client_config(
        flow_data['client_config'],
        scopes=flow_data['scopes'],
        redirect_uri=flow_data['redirect_uri']
    )
    
    # Complete auth
    alex.save_token_from_code(flow, code)
    print("✅ Authentication successful!")
    print("✅ Token saved. Alex Chen can now send emails via Gmail API.")
    return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Alex Chen Gmail API')
    parser.add_argument('action', choices=['setup', 'auth', 'send', 'inbox', 'test'])
    parser.add_argument('--code', help='Authorization code')
    parser.add_argument('--to', help='Recipient email')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body')
    
    args = parser.parse_args()
    
    if args.action == 'setup':
        setup_auth()
        
    elif args.action == 'auth':
        if not args.code:
            print("❌ Usage: python3 gmail_api.py auth --code YOUR_CODE_HERE")
            sys.exit(1)
        complete_auth(args.code)
        
    elif args.action == 'send':
        if not args.to or not args.subject:
            print("❌ Usage: --to recipient@email.com --subject 'Subject' --body 'Message'")
            sys.exit(1)
        
        alex = AlexChenGmailAPI()
        result = alex.send_email(args.to, args.subject, args.body or "")
        print(json.dumps(result, indent=2))
        
    elif args.action == 'inbox':
        alex = AlexChenGmailAPI()
        result = alex.check_inbox()
        print(json.dumps(result, indent=2))
        
    elif args.action == 'test':
        alex = AlexChenGmailAPI()
        print(f"✅ Gmail API configured!")
        print(f"📧 Email: {alex.user_email}")
        
        if os.path.exists(alex.token_file):
            print("✅ Token exists - ready to send emails!")
        else:
            print("⏳ Token not found - run 'setup' first")

if __name__ == '__main__':
    main()
