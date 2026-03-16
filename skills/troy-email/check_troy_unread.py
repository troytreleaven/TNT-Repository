#!/usr/bin/env python3
"""
Troy Gmail unread checker without python-dotenv dependency.
Checks primary unread emails and generates draft replies.
"""

import os
import imaplib
import email
from pathlib import Path


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


def generate_draft_response(sender_name, subject, email_body, respond_as="troy"):
    first_name = sender_name.split()[0] if sender_name else "there"
    subject_lower = (subject or '').lower()
    body_lower = (email_body or '').lower()

    is_inquiry = any(word in subject_lower + body_lower for word in ['training', 'program', 'course', 'leadership', 'quote', 'pricing', 'interest'])
    is_scheduling = any(word in subject_lower + body_lower for word in ['meeting', 'schedule', 'calendar', 'available', 'time'])
    is_follow_up = any(word in subject_lower + body_lower for word in ['follow up', 'follow-up', 'following up', 'checking in'])
    is_thank_you = any(word in subject_lower + body_lower for word in ['thank you', 'thanks', 'appreciate'])

    va_sig = """---
Jarvis | Virtual Assistant to Troy Treleaven
Dale Carnegie Training - Greater Toronto Area & Maritimes

📧 All communications with Troy are private and confidential.
⚡ Troy is currently working with customers and will respond promptly.

📞 905.928.1034
🌐 www.dalecarnegie.com/en/locations/greater-toronto-area-south-central-ontario
🔗 linkedin.com/in/troytreleaven

🎯 Transforming Leaders. Driving Results."""

    troy_sig = """---
Troy Treleaven
Managing Partner
Dale Carnegie Training of Toronto, Hamilton, KW, Niagara, and Maritimes

📱 Mobile: 905.928.1034
🌐 Website: Dale Carnegie Ontario and Maritimes
📅 Book time: https://app.usemotion.com/meet/0mgjn47/meeting
💻 Zoom: zoom.us/j/3095287379
🔗 LinkedIn: linkedin.com/in/troytreleaven
🐦 Twitter: @DaleCarnegieSCO"""

    if respond_as == "va":
        if is_inquiry:
            return f"Hi {first_name},\n\nThank you for reaching out to Troy regarding Dale Carnegie Training programs.\n\nTroy is currently engaged with customers but wanted to ensure you receive a prompt acknowledgment. He will personally review your inquiry and respond within the next few hours.\n\nIn the meantime, if this is time-sensitive, please feel free to call or text Troy directly at 905.928.1034.\n\nBest regards,\n{va_sig}"
        elif is_scheduling:
            return f"Hi {first_name},\n\nThank you for your scheduling request.\n\nTroy has received your message and will review his calendar shortly. For your convenience, you can also book time directly at: calendly.com/troytreleaven\n\nHe'll confirm shortly!\n\nBest regards,\n{va_sig}"
        else:
            return f"Hi {first_name},\n\nThank you for your email.\n\nTroy has received your message and will respond as soon as possible. He is currently working with customers but prioritizes all communications.\n\nIf this is urgent, please call or text: 905.928.1034\n\nBest regards,\n{va_sig}"
    else:
        if is_inquiry:
            return f"Hi {first_name},\n\nThanks for reaching out about Dale Carnegie Training. I'd love to learn more about what you're looking for.\n\n[TROY TO ADD: Specific questions about their needs, team size, timeline]\n\nLet me know when you're free for a quick call to discuss.\n\nBest,\n{troy_sig}"
        elif is_scheduling:
            return f"Hi {first_name},\n\nThanks for your scheduling request.\n\n[TROY TO ADD: Confirm availability or suggest alternatives]\n\nLooking forward to connecting.\n\nBest,\n{troy_sig}"
        elif is_follow_up:
            return f"Hi {first_name},\n\nThanks for following up.\n\n[TROY TO ADD: Update on status/next steps]\n\nTalk soon,\n{troy_sig}"
        elif is_thank_you:
            return f"Hi {first_name},\n\nYou're very welcome!\n\n[TROY TO ADD: Any additional thoughts or next steps]\n\nAppreciate you,\n{troy_sig}"
        else:
            return f"Hi {first_name},\n\nThanks for your email.\n\n[TROY TO ADD: Response content]\n\nBest,\n{troy_sig}"


def extract_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain' and 'attachment' not in str(part.get('Content-Disposition', '')):
                try:
                    payload = part.get_payload(decode=True)
                    body = payload.decode(part.get_content_charset() or 'utf-8', errors='replace')
                    if body.strip():
                        break
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode(msg.get_content_charset() or 'utf-8', errors='replace')
        except Exception:
            pass
    return body


def main():
    load_env_manual('/data/.openclaw/workspace/.env.troy')
    user = os.getenv('TROY_GMAIL_USER')
    pw = os.getenv('TROY_GMAIL_APP_PASSWORD', '').replace(' ', '')
    if not user or not pw:
        print('ERROR: Missing Troy Gmail credentials')
        return

    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(user, pw)
        mail.select('inbox')
        status, messages = mail.search(None, 'X-GM-RAW "category:primary is:unread"')
        if status != 'OK' or not messages[0].strip():
            print('NO_NEW_EMAILS')
            mail.logout()
            return

        email_ids = messages[0].split()[-10:]
        for idx, email_id in enumerate(email_ids, 1):
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            from_addr = msg.get('from', '(Unknown)')
            subject = msg.get('subject', '(No subject)')
            sender_name = from_addr.split('<')[0].strip().strip('"') if '<' in from_addr else from_addr
            body = extract_body(msg)
            preview = ' '.join(body.split())[:300]
            draft_troy = generate_draft_response(sender_name, subject, body, 'troy')
            draft_va = generate_draft_response(sender_name, subject, body, 'va')
            print(f'--- EMAIL {idx} ---')
            print(f'FROM: {from_addr}')
            print(f'SUBJECT: {subject}')
            print(f'PREVIEW: {preview}')
            print('DRAFT_TROY_START')
            print(draft_troy)
            print('DRAFT_TROY_END')
            print('DRAFT_VA_START')
            print(draft_va)
            print('DRAFT_VA_END')
            print('-----------------')
        mail.logout()
    except Exception as e:
        print(f'ERROR: {e}')


if __name__ == '__main__':
    main()
