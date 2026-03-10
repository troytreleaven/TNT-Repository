#!/usr/bin/env python3
"""
Quick demo of Alex Chen capabilities
"""

import sys
sys.path.insert(0, '/data/.openclaw/workspace/skills/alex-chen')

from gmail import AlexChenGmail

print("🚀 Alex Chen - Digital Assistant Demo\n")
print("=" * 50)

# Initialize
print("\n1️⃣ Initializing Alex Chen...")
try:
    alex = AlexChenGmail()
    print(f"✅ Connected as: {alex.user}")
    print("✅ SMTP server: smtp.gmail.com")
    print("✅ IMAP server: imap.gmail.com")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n2️⃣ Available Templates:")
templates = ["meeting_invite", "follow_up", "introduction"]
for t in templates:
    print(f"   • {t}")

print("\n3️⃣ Ready to Use:")
print("   • Send emails as Alex Chen")
print("   • Check inbox for replies")
print("   • Use email templates")
print("   • Access Google Calendar (coming)")
print("   • Access Google Drive (coming)")

print("\n" + "=" * 50)
print("\n✅ Alex Chen is ready to work!")
print("\nExample commands:")
print('  python3 gmail.py test')
print('  python3 gmail.py inbox')
print('  python3 gmail.py send --to someone@email.com --subject "Hello" --body "Message"')
