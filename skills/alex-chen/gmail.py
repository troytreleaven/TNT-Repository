#!/usr/bin/env python3
"""
Alex Chen Gmail Skill
Email automation and Google services integration for Alex Chen identity
"""

import os
import sys
import base64
import json
from datetime import datetime
from typing import Optional, List, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Try to import required libraries
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("❌ requests library not installed. Run: pip install requests")

# Load credentials from environment or .env file
def load_credentials():
    """Load Gmail credentials from environment or .env file"""
    # Try environment variables first
    user = os.getenv('ALEX_GMAIL_USER')
    password = os.getenv('ALEX_GMAIL_APP_PASSWORD')
    
    # Try .env file
    if not user or not password:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if key == 'ALEX_GMAIL_USER' and not user:
                            user = value
                        elif key == 'ALEX_GMAIL_APP_PASSWORD' and not password:
                            password = value
    
    return user, password

class AlexChenGmail:
    """Gmail automation for Alex Chen"""
    
    def __init__(self):
        self.user, self.password = load_credentials()
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.imap_server = "imap.gmail.com"
        
        if not self.user or not self.password:
            raise ValueError("❌ Gmail credentials not found. Set ALEX_GMAIL_USER and ALEX_GMAIL_APP_PASSWORD")
    
    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> Dict:
        """Send an email as Alex Chen"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"Alex Chen <{self.user}>"
            msg['To'] = to
            msg['Subject'] = subject
            
            # Attach body
            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type))
            
            # Connect and send
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            
            return {
                "status": "success",
                "from": self.user,
                "to": to,
                "subject": subject,
                "sent_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def check_inbox(self, limit: int = 10) -> List[Dict]:
        """Check recent emails in inbox"""
        try:
            import imaplib
            import email
            
            # Connect to IMAP
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.user, self.password)
            mail.select('inbox')
            
            # Search for all emails
            _, search_data = mail.search(None, 'ALL')
            email_ids = search_data[0].split()
            
            # Get recent emails
            emails = []
            for e_id in reversed(email_ids[-limit:]):
                _, msg_data = mail.fetch(e_id, '(RFC822)')
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                emails.append({
                    "id": e_id.decode(),
                    "from": email_message['From'],
                    "subject": email_message['Subject'],
                    "date": email_message['Date']
                })
            
            mail.close()
            mail.logout()
            
            return emails
            
        except Exception as e:
            return [{"error": str(e)}]
    
    def send_template_email(self, to: str, template_name: str, **kwargs) -> Dict:
        """Send using a template"""
        templates = {
            "meeting_invite": {
                "subject": "Meeting Invitation: {topic}",
                "body": """Hi {name},

I'd like to schedule a meeting to discuss {topic}.

Proposed time: {datetime}
Duration: {duration}
Location: {location}

Please let me know if this works for you.

Best regards,
Alex Chen
Operations Coordinator
Dale Carnegie Training — Greater Toronto Area"""
            },
            "follow_up": {
                "subject": "Following up: {topic}",
                "body": """Hi {name},

I wanted to follow up on our conversation about {topic}.

{message}

Please let me know if you have any questions.

Best regards,
Alex Chen"""
            },
            "introduction": {
                "subject": "Introduction: {topic}",
                "body": """Hi {name},

My name is Alex Chen, and I'm the Operations Coordinator for Dale Carnegie Training in the Greater Toronto Area.

{message}

I'd welcome the opportunity to connect and discuss how we might be able to support your team's development.

Best regards,
Alex Chen
alex.chen.dc.gta@gmail.com"""
            }
        }
        
        if template_name not in templates:
            return {"error": f"Template '{template_name}' not found"}
        
        template = templates[template_name]
        subject = template['subject'].format(**kwargs)
        body = template['body'].format(**kwargs)
        
        return self.send_email(to, subject, body)

def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Alex Chen Gmail Assistant')
    parser.add_argument('action', choices=['send', 'inbox', 'test'], help='Action to perform')
    parser.add_argument('--to', help='Recipient email')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body')
    parser.add_argument('--template', help='Template name')
    
    args = parser.parse_args()
    
    try:
        alex = AlexChenGmail()
        
        if args.action == 'test':
            print(f"✅ Alex Chen Gmail configured!")
            print(f"📧 Email: {alex.user}")
            print("✅ Ready to send emails")
            
        elif args.action == 'send':
            if not args.to or not args.subject:
                print("❌ Usage: --to recipient@email.com --subject 'Subject' --body 'Message'")
                sys.exit(1)
            
            result = alex.send_email(args.to, args.subject, args.body or "")
            print(json.dumps(result, indent=2))
            
        elif args.action == 'inbox':
            emails = alex.check_inbox(limit=5)
            print(f"📧 Recent emails for {alex.user}:")
            for e in emails:
                if 'error' in e:
                    print(f"❌ Error: {e['error']}")
                else:
                    print(f"  From: {e['from']}")
                    print(f"  Subject: {e['subject']}")
                    print(f"  Date: {e['date']}\n")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
