#!/usr/bin/env python3
"""
Troy Treleaven Outlook Email Monitoring (Dale Carnegie)
IMAP/SMTP access for ttreleaven@dalecarnegie.ca
"""

import os
import sys
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path('/data/.openclaw/workspace/.env.outlook')
load_dotenv(env_path)

# Outlook Configuration
OUTLOOK_USER = os.getenv('OUTLOOK_USER')
OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD')
OUTLOOK_NAME = os.getenv('OUTLOOK_NAME', 'Troy Treleaven')

# Microsoft 365 IMAP/SMTP Settings
IMAP_SERVER = 'outlook.office365.com'
IMAP_PORT = 993
SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587

# Dale Carnegie Signature
DALE_CARNEGIE_SIGNATURE = """
---
Troy Treleaven
Managing Partner
Dale Carnegie Training of Toronto, Hamilton, KW, Niagara, and Maritimes

📱 Mobile: 905.928.1034
🌐 Website: Dale Carnegie Ontario and Maritimes
📅 Book time: calendly.com/troytreleaven
💻 Zoom: zoom.us/j/3095287379
🔗 LinkedIn: linkedin.com/in/troytreleaven
🐦 Twitter: @DaleCarnegieSCO

📥 DOWNLOAD Dale Carnegie Ebooks
📊 Our programs, events and solutions
"""


def check_unread_emails(limit=10):
    """Check for unread emails in Outlook inbox"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(OUTLOOK_USER, OUTLOOK_PASSWORD)
        mail.select('inbox')
        
        # Search for UNSEEN (unread) emails
        status, messages = mail.search(None, 'UNSEEN')
        
        if status != 'OK':
            return []
        
        email_ids = messages[0].split()
        
        if len(email_ids) == 0:
            return []
        
        emails = []
        for email_id in email_ids[-limit:]:  # Get last N emails
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract details
            subject = msg['subject'] or '(No subject)'
            from_addr = msg['from']
            date = msg['date']
            
            # Extract sender name
            sender_name = ""
            if '<' in from_addr:
                sender_name = from_addr.split('<')[0].strip().strip('"')
            else:
                sender_name = from_addr
            
            # Get body
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
                'id': email_id.decode(),
                'subject': subject,
                'from': from_addr,
                'sender_name': sender_name,
                'date': date,
                'body': body[:500] + '...' if len(body) > 500 else body
            })
        
        mail.close()
        mail.logout()
        
        return emails
        
    except Exception as e:
        print(f"❌ Error checking Outlook: {str(e)}")
        return []


def test_connection():
    """Test Outlook connection"""
    print("🔍 Testing Dale Carnegie Outlook connection...")
    print(f"   Account: {OUTLOOK_USER}")
    
    try:
        # Test IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(OUTLOOK_USER, OUTLOOK_PASSWORD)
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        count = len(messages[0].split())
        print(f"✅ IMAP (reading) - Connected! {count} emails in inbox")
        mail.logout()
        
        # Test SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(OUTLOOK_USER, OUTLOOK_PASSWORD)
            print("✅ SMTP (sending) - Connected!")
        
        print("\n🎉 Dale Carnegie Outlook is ready!")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        return False


def send_email(to_email, subject, body):
    """Send an email from Dale Carnegie Outlook"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{OUTLOOK_NAME} <{OUTLOOK_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate(localtime=True)
        
        # Add body with signature
        full_body = body + DALE_CARNEGIE_SIGNATURE
        msg.attach(MIMEText(full_body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(OUTLOOK_USER, OUTLOOK_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent from {OUTLOOK_USER} to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def main():
    if len(sys.argv) < 2:
        print("""
Dale Carnegie Outlook Email Monitor - Usage:

  test                    Test Outlook connection
  check                   Check for unread emails
  send <to> <subject>     Send email (will prompt for body)

Examples:
  python3 outlook_client.py test
  python3 outlook_client.py check
  python3 outlook_client.py send client@company.com "Follow-up"
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'test':
        test_connection()
    
    elif command == 'check':
        emails = check_unread_emails()
        if len(emails) == 0:
            print("📭 No new unread emails in Dale Carnegie Outlook.")
        else:
            print(f"\n📧 {len(emails)} new Dale Carnegie email(s):\n")
            for i, e in enumerate(emails, 1):
                print(f"{'='*60}")
                print(f"DALE CARNEGIE EMAIL #{i}")
                print(f"{'='*60}")
                print(f"From: {e['from']}")
                print(f"Subject: {e['subject']}")
                print(f"Date: {e['date']}")
                print(f"\nPreview:\n{e['body'][:300]}...")
                print()
    
    elif command == 'send':
        if len(sys.argv) < 4:
            print("❌ Usage: send <to_email> <subject>")
            return
        to = sys.argv[2]
        subject = sys.argv[3]
        print("Enter email body (Ctrl+D when done):")
        body = sys.stdin.read()
        send_email(to, subject, body)
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()
