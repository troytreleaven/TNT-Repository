#!/usr/bin/env python3
"""Trigger voice follow-up calls to prospects"""
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CSV_FILE = SCRIPT_DIR / "prospect_list.csv"
ENV_FILE = Path("/data/.openclaw/workspace/skills/groq-voice/.env")

def load_env():
    env = {}
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env[key] = val.strip().strip('"').strip("'")
    return env

def load_prospects():
    prospects = []
    if CSV_FILE.exists():
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prospects.append(row)
    return prospects

def get_prospects_to_call():
    """Find prospects who got email yesterday but haven't been called yet"""
    prospects = load_prospects()
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    to_call = []
    
    for p in prospects:
        if p.get('email_sent_date') == yesterday and not p.get('call_scheduled'):
            to_call.append(p)
    
    return to_call

def trigger_vapi_call(prospect):
    """Trigger a VAPI call to the prospect"""
    env = load_env()
    vapi_key = env.get('VAPI_API_KEY')
    
    if not vapi_key:
        print("❌ VAPI_API_KEY not found in .env")
        return False
    
    # This would use VAPI's API to initiate a call
    # For now, just print what we'd do
    print(f"📞 Would call {prospect['name']} at {prospect['phone']}")
    print(f"   Email sent: {prospect.get('email_sent_date')}")
    print(f"   Notes: {prospect.get('notes', '')}")
    
    # TODO: Implement actual VAPI call
    # import requests
    # response = requests.post(
    #     "https://api.vapi.ai/call",
    #     headers={"Authorization": f"Bearer {vapi_key}"},
    #     json={
    #         "phone_number": prospect['phone'],
    #         "agent_id": "ALEX_CHEN_AGENT_ID",
    #         "system_prompt": open(SCRIPT_DIR / "alex_voice_prompt.txt").read()
    #     }
    # )
    return True

def update_prospect_status(prospect, status='scheduled'):
    """Update CSV with call status"""
    prospects = load_prospects()
    for p in prospects:
        if p.get('email') == prospect.get('email'):
            p['call_scheduled'] = datetime.now().strftime('%Y-%m-%d') if status == 'scheduled' else ''
    
    # Write back
    with open(CSV_FILE, 'w', newline='') as f:
        fieldnames = ['name', 'phone', 'email', 'email_sent_date', 'call_scheduled', 'call_completed', 'appointment_booked', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prospects)

def add_prospect(name, phone, email, notes=''):
    """Add a new prospect to the list"""
    prospect = {
        'name': name,
        'phone': phone,
        'email': email,
        'email_sent_date': datetime.now().strftime('%Y-%m-%d'),
        'call_scheduled': '',
        'call_completed': '',
        'appointment_booked': '',
        'notes': notes
    }
    
    prospects = load_prospects()
    prospects.append(prospect)
    
    with open(CSV_FILE, 'w', newline='') as f:
        fieldnames = ['name', 'phone', 'email', 'email_sent_date', 'call_scheduled', 'call_completed', 'appointment_booked', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(prospects)
    
    print(f"✅ Added {name} ({email})")
    print(f"   Email date set to today: {prospect['email_sent_date']}")
    print(f"   Call will trigger tomorrow!")

def main():
    if len(sys.argv) < 2:
        print("Voice Follow-Up System")
        print("Usage:")
        print("  python3 trigger_calls.py add \"Name\" \"+1234567890\" \"email@example.com\" [notes]")
        print("  python3 trigger_calls.py list")
        print("  python3 trigger_calls.py trigger")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) >= 5:
        name = sys.argv[2]
        phone = sys.argv[3]
        email = sys.argv[4]
        notes = sys.argv[5] if len(sys.argv) > 5 else ""
        add_prospect(name, phone, email, notes)
    
    elif cmd == "list":
        prospects = load_prospects()
        print(f"\n📋 Prospects ({len(prospects)} total):")
        for p in prospects:
            status = "✅ booked" if p.get('appointment_booked') else ("📞 called" if p.get('call_completed') else ("⏳ pending" if p.get('call_scheduled') else "📧 email sent"))
            print(f"  • {p['name']} | {p['email']} | {status}")
    
    elif cmd == "trigger":
        to_call = get_prospects_to_call()
        if not to_call:
            print("No prospects to call today!")
            print("(Prospects must have email_sent_date = yesterday)")
            return
        
        print(f"📞 Found {len(to_call)} prospect(s) to call:\n")
        for p in to_call:
            trigger_vapi_call(p)
            update_prospect_status(p, 'scheduled')
            print()

if __name__ == "__main__":
    main()