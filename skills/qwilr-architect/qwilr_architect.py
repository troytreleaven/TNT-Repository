#!/usr/bin/env python3
"""
Jarvis Qwilr Architect - Sales Presentation Builder
Transforms raw sales notes into high-conversion Qwilr Pages
"""
import os
import sys
import json
import requests
from datetime import datetime
import uuid

# Configuration
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://api.qwilr.com/v1/pages"

def load_env():
    """Load API key from .env file"""
    env = {}
    env_path = os.path.join(SKILL_DIR, '.env')
    workspace_env = '/data/.openclaw/workspace/.env.qwilr'
    
    for filepath in [env_path, workspace_env]:
        if os.path.exists(filepath):
            with open(filepath) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        env[key] = val.strip().strip('"').strip("'")
    return env

def get_api_key(env):
    """Get Qwilr API key"""
    key = env.get('QWILR_API_KEY') or env.get('API_KEY')
    if not key:
        print("Error: QWILR_API_KEY not found")
        sys.exit(1)
    return key

def analyze_sales_notes(notes_text):
    """Analyze raw sales notes and extract key components."""
    lines = notes_text.strip().split('\n')
    client_name = "Valued Client"
    
    for line in lines:
        if line.lower().startswith('client:'):
            client_name = line.split(':', 1)[1].strip()
            break
    
    content = '\n'.join(lines[1:]) if len(lines) > 1 else notes_text
    return {'client_name': client_name, 'content': content[:500]}

def create_qwilr_page(client_name, sales_notes, brand_color=None):
    """
    Create a Qwilr page using the correct API format.
    """
    env = load_env()
    api_key = get_api_key(env)
    header_color = brand_color or "#C41E3A"
    
    analysis = analyze_sales_notes(sales_notes)
    
    # Generate block IDs
    block_ids = [str(uuid.uuid4()) for _ in range(4)]
    
    # Correct Qwilr API format - using their block structure
    # Note: This may need adjustment based on actual Qwilr API docs
    payload = {
        "name": f"Strategic Proposal for {analysis['client_name']}",
        "templateId": "default",  # or specific template ID
        "blocks": [
            {
                "id": block_ids[0],
                "type": "hero",
                "content": {
                    "title": f"Partnering with {analysis['client_name']}",
                    "subtitle": "A Tailored Strategic Approach"
                }
            },
            {
                "id": block_ids[1],
                "type": "text",
                "content": {
                    "body": f"<h2>Our Proposed Solution</h2><p>{analysis['content']}</p>"
                }
            },
            {
                "id": block_ids[2],
                "type": "quote",
                "content": {
                    "text": "Efficiency is doing things right; effectiveness is doing the right things.",
                    "attribution": "Peter Drucker"
                }
            },
            {
                "id": block_ids[3],
                "type": "cta",
                "content": {
                    "buttonText": "Let's Get Started",
                    "title": "Ready to transform your team?"
                }
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try the API - if it fails, provide helpful error
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers, timeout=30)
        
        if response.status_code in [200, 201]:
            result = response.json()
            return {
                "success": True,
                "url": result.get('url', result.get('preview_url', 'Created')),
                "page_id": result.get('id'),
                "client": analysis['client_name']
            }
        else:
            # Return info for manual creation
            return {
                "success": False,
                "error": f"API Error ({response.status_code})",
                "details": response.text[:500],
                "client": analysis['client_name'],
                "notes": sales_notes,
                "payload": json.dumps(payload, indent=2)
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "client": analysis['client_name'],
            "notes": sales_notes
        }

def cmd_create(args):
    """CLI for creating pages"""
    if len(args) < 2:
        print("Usage: qwilr_architect.py create <client> <notes> [color]")
        return
    
    client = args[0]
    notes = args[1]
    color = args[2] if len(args) > 2 else None
    
    result = create_qwilr_page(client, notes, color)
    
    if result['success']:
        print(f"✅ Page created: {result['url']}")
    else:
        print(f"❌ Error: {result.get('error')}")
        print(f"\nClient: {result.get('client')}")
        print(f"Notes: {result.get('notes')[:200]}...")
        if 'payload' in result:
            print(f"\nPayload (for manual creation):")
            print(result['payload'][:500])

def main():
    if len(sys.argv) < 2:
        print("🤖 Jarvis Qwilr Architect")
        print("Usage: python3 qwilr_architect.py create <client> <notes> [color]")
        return
    
    if sys.argv[1] == "create":
        cmd_create(sys.argv[2:])
    else:
        print(f"Unknown command: {sys.argv[1]}")

if __name__ == "__main__":
    main()