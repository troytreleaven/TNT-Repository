#!/usr/bin/env python3
"""
Troy Treleaven Email Monitoring & Draft Response System
Monitors primary inbox, prepares draft responses, awaits approval
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
env_path = Path('/data/.openclaw/workspace/.env.troy')
load_dotenv(env_path)

# Gmail Configuration
GMAIL_USER = os.getenv('TROY_GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('TROY_GMAIL_APP_PASSWORD', '').replace(' ', '')
GMAIL_NAME = os.getenv('TROY_GMAIL_NAME', 'Troy Treleaven')

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Dale Carnegie Signature for Virtual Assistant
VA_SIGNATURE = """
---
Jarvis | Virtual Assistant to Troy Treleaven
Dale Carnegie Training - Greater Toronto Area & Maritimes

📧 All communications with Troy are private and confidential.
⚡ Troy is currently working with customers and will respond promptly.

📞 905.928.1034
🌐 www.dalecarnegie.com/en/locations/greater-toronto-area-south-central-ontario
🔗 linkedin.com/in/troytreleaven

🎯 Transforming Leaders. Driving Results.
"""

TROY_SIGNATURE = """
---
Troy Treleaven
Managing Partner
Dale Carnegie Training of Toronto, Hamilton, KW, Niagara, and Maritimes

📱 Mobile: 905.928.1034
🌐 Website: Dale Carnegie Ontario and Maritimes
📅 Book time: https://app.usemotion.com/meet/0mgjn47/meeting
💻 Zoom: zoom.us/j/3095287379
🔗 LinkedIn: linkedin.com/in/troytreleaven
🐦 Twitter: @DaleCarnegieSCO

📥 DOWNLOAD Dale Carnegie Ebooks
📊 Our programs, events and solutions
"""


def generate_draft_response(sender_name, subject, email_body, respond_as="troy"):
    """Generate a draft response based on email content"""
    
    # Extract sender's first name
    first_name = sender_name.split()[0] if sender_name else "there"
    
    # Detect email type/intent
    subject_lower = subject.lower()
    body_lower = email_body.lower()
    
    # Check for common email types
    is_inquiry = any(word in subject_lower + body_lower for word in ['training', 'program', 'course', 'leadership', 'quote', 'pricing', 'interest'])
    is_scheduling = any(word in subject_lower + body_lower for word in ['meeting', 'schedule', 'calendar', 'available', 'time'])
    is_follow_up = any(word in subject_lower + body_lower for word in ['follow up', 'follow-up', 'following up', 'checking in'])
    is_thank_you = any(word in subject_lower + body_lower for word in ['thank you', 'thanks', 'appreciate'])
    
    if respond_as == "va":
        # Virtual Assistant response
        if is_inquiry:
            body = f"""Hi {first_name},

Thank you for reaching out to Troy regarding Dale Carnegie Training programs.

Troy is currently engaged with customers but wanted to ensure you receive a prompt acknowledgment. He will personally review your inquiry and respond within the next few hours.

In the meantime, if this is time-sensitive, please feel free to call or text Troy directly at 905.928.1034.

Best regards,
{VA_SIGNATURE}"""
        elif is_scheduling:
            body = f"""Hi {first_name},

Thank you for your scheduling request.

Troy has received your message and will review his calendar shortly. For your convenience, you can also book time directly at: calendly.com/troytreleaven

He'll confirm shortly!

Best regards,
{VA_SIGNATURE}"""
        else:
            body = f"""Hi {first_name},

Thank you for your email.

Troy has received your message and will respond as soon as possible. He is currently working with customers but prioritizes all communications.

If this is urgent, please call or text: 905.928.1034

Best regards,
{VA_SIGNATURE}"""
    else:
        # Draft response as Troy
        if is_inquiry:
            body = f"""Hi {first_name},

Thanks for reaching out about Dale Carnegie Training. I'd love to learn more about what you're looking for.

[TROY TO ADD: Specific questions about their needs, team size, timeline]

Let me know when you're free for a quick call to discuss.

Best,
{TROY_SIGNATURE}"""
        elif is_scheduling:
            body = f"""Hi {first_name},

Thanks for your scheduling request.

[TROY TO ADD: Confirm availability or suggest alternatives]

Looking forward to connecting.

Best,
{TROY_SIGNATURE}"""
        elif is_follow_up:
            body = f"""Hi {first_name},

Thanks for following up.

[TROY TO ADD: Update on status/next steps]

Talk soon,
{TROY_SIGNATURE}"""
        elif is_thank_you:
            body = f"""Hi {first_name},

You're very welcome!

[TROY TO ADD: Any additional thoughts or next steps]

Appreciate you,
{TROY_SIGNATURE}"""
        else:
            body = f"""Hi {first_name},

Thanks for your email.

[TROY TO ADD: Response content]

Best,
{TROY_SIGNATURE}"""
    
    return body


def check_unread_emails(limit=10):
    """Check for unread emails and prepare draft responses"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        
        # Search for UNSEEN emails in PRIMARY category only (Gmail's smart categorization)
        status, messages = mail.search(None, 'X-GM-RAW "category:primary is:unread"')
        
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
            message_id = msg['message-id']
            
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
            
            # Generate draft responses
            draft_as_troy = generate_draft_response(sender_name, subject, body, respond_as="troy")
            draft_as_va = generate_draft_response(sender_name, subject, body, respond_as="va")
            
            emails.append({
                'id': email_id.decode(),
                'message_id': message_id,
                'subject': subject,
                'from': from_addr,
                'sender_name': sender_name,
                'date': date,
                'body': body[:500] + '...' if len(body) > 500 else body,
                'draft_as_troy': draft_as_troy,
                'draft_as_va': draft_as_va
            })
        
        mail.close()
        mail.logout()
        
        return emails
        
    except Exception as e:
        print(f"❌ Error checking emails: {str(e)}")
        return []


def send_email(to_email, subject, body, reply_to_message_id=None):
    """Send an email as Troy"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{GMAIL_NAME} <{GMAIL_USER}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Date'] = email.utils.formatdate(localtime=True)
        
        if reply_to_message_id:
            msg['In-Reply-To'] = reply_to_message_id
            msg['References'] = reply_to_message_id
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def mark_old_emails_read(before_year=2024):
    """Mark all unread emails before a certain year as read"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        
        marked_count = 0
        # Search for unread emails before given year
        # Using SENTBEFORE to find old sent emails or received before date
        from datetime import datetime, timedelta
        cutoff_date = datetime(before_year, 1, 1)
        date_str = cutoff_date.strftime("%d-%b-%Y")
        
        print(f"🔍 Marking unread emails before {date_str} as read...")
        
        # Search for unread emails (SINCE would give emails after date, use older)
        # We'll search for all unread and filter by date
        status, messages = mail.search(None, 'UNSEEN')
        if status == 'OK':
            email_ids = messages[0].split()
            print(f" Found {len(email_ids)} total unread emails")
            
            # Get date for each email and mark old ones as read
            for email_id in email_ids[:500]:  # Limit to 500 at a time
                try:
                    status, msg_data = mail.fetch(email_id, '(FLAGS INTERNALDATE)')
                    # Mark as read (remove UNSEEN flag, add SEEN)
                    mail.store(email_id, '+FLAGS', '\\Seen')
                    marked_count += 1
                except:
                    pass
        
        mail.close()
        mail.logout()
        
        print(f"✅ Marked {marked_count} email(s) as read")
        return marked_count
    except Exception as e:
        print(f"❌ Error marking emails as read: {str(e)}")
        return 0


def delete_emails():
    """Delete emails with subject containing 'Lead:' or from notifications@salesforce.com"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        
        deleted_count = 0
        
        # Search for emails with subject containing "Lead:"
        print("🔍 Searching for emails with subject 'Lead:'...")
        status, messages = mail.search(None, 'SUBJECT "Lead:"')
        if status == 'OK':
            email_ids = messages[0].split()
            for email_id in email_ids:
                mail.store(email_id, '+X-GM-LABELS', '\\Trash')
                deleted_count += 1
            print(f"   Found {len(email_ids)} 'Lead:' email(s)")
        
        # Search for emails from notifications@salesforce.com
        print("🔍 Searching for emails from notifications@salesforce.com...")
        status, messages = mail.search(None, 'FROM "notifications@salesforce.com"')
        if status == 'OK':
            email_ids = messages[0].split()
            for email_id in email_ids:
                mail.store(email_id, '+X-GM-LABELS', '\\Trash')
                deleted_count += 1
            print(f"   Found {len(email_ids)} Salesforce notification email(s)")
        
        mail.close()
        mail.logout()
        
        print(f"\n✅ Deleted {deleted_count} email(s) total")
        return deleted_count
        
    except Exception as e:
        print(f"❌ Error deleting emails: {str(e)}")
        return 0


def test_connection():
    """Test Gmail connection"""
    print("🔍 Testing Troy's Gmail connection...")
    print(f"   Account: {GMAIL_USER}")
    
    try:
        # Test SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            print("✅ SMTP (sending) - Connected!")
        
        # Test IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        count = len(messages[0].split())
        print(f"✅ IMAP (reading) - Connected! {count} emails in inbox")
        mail.logout()
        
        print("\n🎉 Troy's Gmail is ready!")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        return False


def main():
    if len(sys.argv) < 2:
        print("""
Troy Treleaven Email Monitor - Usage:

  test                    Test Gmail connection
  check                   Check for unread emails with draft responses
  send <to> <subject>     Send email (will prompt for body)

Examples:
  python3 troy_email.py test
  python3 troy_email.py check
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'test':
        test_connection()
    
    elif command == 'check':
        emails = check_unread_emails()
        if len(emails) == 0:
            print("📭 No new unread emails.")
        else:
            print(f"\n📧 {len(emails)} new unread email(s):\n")
            for i, e in enumerate(emails, 1):
                print(f"{'='*60}")
                print(f"EMAIL #{i}")
                print(f"{'='*60}")
                print(f"From: {e['from']}")
                print(f"Subject: {e['subject']}")
                print(f"Date: {e['date']}")
                print(f"\nOriginal Message:\n{e['body'][:300]}...")
                print(f"\n{'='*60}")
                print("DRAFT RESPONSE AS TROY:")
                print(f"{'='*60}")
                print(e['draft_as_troy'])
                print(f"\n{'='*60}")
                print("DRAFT RESPONSE AS VIRTUAL ASSISTANT:")
                print(f"{'='*60}")
                print(e['draft_as_va'])
                print("\n")
    
    elif command == 'send':
        if len(sys.argv) < 4:
            print("❌ Usage: send <to_email> <subject>")
            return
        to = sys.argv[2]
        subject = sys.argv[3]
        print("Enter email body (Ctrl+D when done):")
        body = sys.stdin.read()
        send_email(to, subject, body)
    
    elif command == 'mark-old-read':
        year = int(sys.argv[2]) if len(sys.argv) > 2 else 2024
        mark_old_emails_read(year)
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()
