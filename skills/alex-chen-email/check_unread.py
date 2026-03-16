#!/usr/bin/env python3
"""
Alex Chen Email Checker (No-Dotenv Version)
Checks alex.chen.gta.dc@gmail.com for unread emails.
"""

import os
import sys
import imaplib
import email
from pathlib import Path

# Manual .env parsing to avoid 'dotenv' dependency
def load_env_manual(path):
    if not os.path.exists(path):
        return
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

# Load environment variables
env_path = Path("/data/.openclaw/workspace/skills/groq-voice/.env")
load_env_manual(env_path)

# Gmail Configuration
GMAIL_USER = os.getenv('ALEX_GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('ALEX_GMAIL_APP_PASSWORD', '').replace(' ', '')
IMAP_SERVER = 'imap.gmail.com'

def read_unread():
    try:
        if not GMAIL_USER or not GMAIL_APP_PASSWORD:
            print("❌ Error: Gmail credentials not found in .env")
            return []

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        
        status, messages = mail.search(None, 'UNSEEN')
        
        if status != 'OK' or not messages[0]:
            return []
        
        email_ids = messages[0].split()
        emails = []
        
        for email_id in reversed(email_ids):
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = msg['subject'] or '(No subject)'
            from_addr = msg['from'] or '(Unknown)'
            date = msg['date'] or '(No date)'
            
            # Get email body preview
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode()
                except:
                    pass
            
            emails.append({
                'subject': subject,
                'from': from_addr,
                'date': date,
                'preview': body[:200].replace('\n', ' ').strip() + '...'
            })
        
        mail.close()
        mail.logout()
        return emails
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

if __name__ == '__main__':
    unread = read_unread()
    if not unread:
        print("NO_NEW_EMAILS")
    else:
        for i, e in enumerate(unread, 1):
            print(f"--- EMAIL {i} ---")
            print(f"FROM: {e['from']}")
            print(f"SUBJECT: {e['subject']}")
            print(f"DATE: {e['date']}")
            print(f"PREVIEW: {e['preview']}")
            print("-----------------")
