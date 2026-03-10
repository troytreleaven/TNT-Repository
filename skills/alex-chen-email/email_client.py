#!/usr/bin/env python3
"""
Alex Chen Email Automation Skill
Send and receive emails as Alex Chen (alex.chen.dc.gta@gmail.com)
Dale Carnegie GTA Operations Coordinator
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
env_path = Path(__file__).parent.parent / "groq-voice" / ".env"
load_dotenv(env_path)
load_dotenv(env_path)

# Gmail Configuration
GMAIL_USER = os.getenv('ALEX_GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('ALEX_GMAIL_APP_PASSWORD', '').replace(' ', '')  # Remove spaces
GMAIL_NAME = os.getenv('ALEX_GMAIL_NAME', 'Alex Chen')

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993


def send_email(to_email, subject, body, html_body=None):
    """Send an email as Alex Chen"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{GMAIL_NAME} <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate(localtime=True)
        
        # Add plain text body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add HTML body if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        # Connect to Gmail SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully!")
        print(f"   From: {GMAIL_NAME} <{GMAIL_USER}>")
        print(f"   To: {to_email}")
        print(f"   Subject: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def read_inbox(limit=10, unread_only=False):
    """Read emails from Alex Chen's inbox"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        
        # Search for emails
        if unread_only:
            status, messages = mail.search(None, 'UNSEEN')
        else:
            status, messages = mail.search(None, 'ALL')
        
        if status != 'OK':
            print("❌ No emails found")
            return []
        
        email_ids = messages[0].split()
        email_ids = email_ids[-limit:]  # Get last N emails
        
        emails = []
        for email_id in reversed(email_ids):
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract email details
            subject = msg['subject'] or '(No subject)'
            from_addr = msg['from'] or '(Unknown)'
            date = msg['date'] or '(No date)'
            
            # Get email body
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
                'date': date,
                'body': body[:500] + '...' if len(body) > 500 else body
            })
        
        mail.close()
        mail.logout()
        
        return emails
        
    except Exception as e:
        print(f"❌ Error reading inbox: {str(e)}")
        return []


def send_dale_carnegie_inquiry_response(to_email, prospect_name, program_interest=None):
    """Send a professional Dale Carnegie inquiry response"""
    
    subject = "Thank you for your interest in Dale Carnegie Training"
    
    body = f"""Dear {prospect_name},

Thank you for your interest in Dale Carnegie Training! My name is Alex Chen, and I'm the Operations Coordinator for our Greater Toronto Area programs.

I'd be happy to help you explore our leadership and professional development offerings:

• **DCC (Dale Carnegie Course)** - 8-week evening program
• **Leadership Boot Camp** - 3-day intensive
• **High Impact Presentations (HIP)** - 2-day program
• **Custom corporate training** for teams

{program_interest if program_interest else ""}

Would you be available for a brief call this week to discuss your specific goals? I can connect you with the right program advisor.

Best regards,
Alex Chen
Operations Coordinator
Dale Carnegie Training - Greater Toronto Area
📧 alex.chen.dc.gta@gmail.com
"""

    return send_email(to_email, subject, body)


def test_connection():
    """Test Gmail connection"""
    print("🔍 Testing Alex Chen Gmail connection...")
    print(f"   Account: {GMAIL_USER}")
    
    try:
        # Test SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            print("✅ SMTP (sending) - Connected successfully!")
        
        # Test IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        count = len(messages[0].split())
        print(f"✅ IMAP (reading) - Connected! {count} emails in inbox")
        mail.logout()
        
        print("\n🎉 Alex Chen email is ready to use!")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        return False


def main():
    if len(sys.argv) < 2:
        print("""
Alex Chen Email Skill - Usage:

  test                    Test Gmail connection
  read [limit]            Read inbox (default: 10)
  read-unread             Read only unread emails
  send <to> <subject>     Send email (will prompt for body)
  auto-reply <to> <name>  Send Dale Carnegie inquiry response

Examples:
  python3 email_client.py test
  python3 email_client.py read 5
  python3 email_client.py send prospect@company.com "Follow-up"
  python3 email_client.py auto-reply john@example.com "John Smith"
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'test':
        test_connection()
    
    elif command == 'read':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        emails = read_inbox(limit=limit)
        print(f"\n📧 Inbox ({len(emails)} emails):\n")
        for i, e in enumerate(emails, 1):
            print(f"{i}. From: {e['from']}")
            print(f"   Subject: {e['subject']}")
            print(f"   Date: {e['date']}")
            print(f"   Preview: {e['body'][:100]}...\n")
    
    elif command == 'read-unread':
        emails = read_inbox(unread_only=True)
        print(f"\n📧 Unread emails ({len(emails)}):\n")
        for i, e in enumerate(emails, 1):
            print(f"{i}. From: {e['from']}")
            print(f"   Subject: {e['subject']}")
            print(f"   Date: {e['date']}\n")
    
    elif command == 'send':
        if len(sys.argv) < 4:
            print("❌ Usage: send <to_email> <subject>")
            return
        to = sys.argv[2]
        subject = sys.argv[3]
        print("Enter email body (Ctrl+D when done):")
        body = sys.stdin.read()
        send_email(to, subject, body)
    
    elif command == 'auto-reply':
        if len(sys.argv) < 4:
            print("❌ Usage: auto-reply <to_email> <prospect_name>")
            return
        to = sys.argv[2]
        name = sys.argv[3]
        send_dale_carnegie_inquiry_response(to, name)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for usage help.")


if __name__ == '__main__':
    main()
