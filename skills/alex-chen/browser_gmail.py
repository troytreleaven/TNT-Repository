#!/usr/bin/env python3
"""
Alex Chen - Browser Automation for Gmail
Uses Playwright to automate Gmail web interface
"""

import os
import sys
import json
import re
from datetime import datetime

# Load credentials
def load_credentials():
    """Load Gmail credentials"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    user = None
    password = None
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key == 'ALEX_GMAIL_USER':
                        user = value
                    elif key == 'ALEX_GMAIL_APP_PASSWORD':
                        password = value
    
    return user, password

def escape_js_string(s):
    """Escape string for JavaScript"""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace("'", "\\'")
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '')
    return s

class AlexChenBrowser:
    """Browser automation for Alex Chen's Gmail"""
    
    def __init__(self):
        self.user, self.password = load_credentials()
        if not self.user or not self.password:
            raise ValueError("❌ Credentials not found in .env file")
    
    def send_email_browser(self, to: str, subject: str, body: str) -> dict:
        """Send email using browser automation"""
        
        # Escape strings for JavaScript
        user_esc = escape_js_string(self.user)
        pass_esc = escape_js_string(self.password)
        to_esc = escape_js_string(to)
        subject_esc = escape_js_string(subject)
        body_esc = escape_js_string(body)
        
        playwright_script = f'''const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const context = await browser.newContext({{
        viewport: {{ width: 1280, height: 720 }}
    }});
    const page = await context.newPage();
    
    try {{
        console.log("Navigating to Gmail...");
        await page.goto('https://gmail.com');
        await page.waitForLoadState('networkidle');
        
        console.log("Entering email...");
        await page.fill('input[type="email"]', "{user_esc}");
        await page.click('#identifierNext');
        await page.waitForTimeout(2000);
        
        console.log("Entering password...");
        await page.fill('input[type="password"]', "{pass_esc}");
        await page.click('#passwordNext');
        await page.waitForTimeout(5000);
        
        console.log("Waiting for Gmail to load...");
        await page.waitForSelector('div[role="button"][gh="cm"]', {{ timeout: 15000 }});
        
        console.log("Clicking Compose...");
        await page.click('div[role="button"][gh="cm"]');
        await page.waitForTimeout(2000);
        
        console.log("Filling email details...");
        await page.fill('input[role="combobox"][aria-label="To recipients"]', "{to_esc}");
        await page.fill('input[aria-label="Subject"]', "{subject_esc}");
        await page.fill('div[aria-label="Message Body"]', "{body_esc}");
        
        await page.waitForTimeout(1000);
        
        console.log("Sending...");
        await page.click('div[role="button"][aria-label*="Send"]');
        await page.waitForTimeout(3000);
        
        console.log(JSON.stringify({{
            "status": "success",
            "from": "{user_esc}",
            "to": "{to_esc}",
            "subject": "{subject_esc}",
            "sent_at": "{datetime.now().isoformat()}"
        }}));
        
    }} catch (error) {{
        console.log(JSON.stringify({{
            "status": "error",
            "error": error.message
        }}));
    }} finally {{
        await browser.close();
    }}
}})();
'''
        
        # Write script to skill directory (so it can find node_modules)
        skill_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(skill_dir, 'temp_gmail_send.js')
        with open(script_path, 'w') as f:
            f.write(playwright_script)
        
        # Run with node from skill directory
        import subprocess
        result = subprocess.run(
            ['node', script_path],
            capture_output=True,
            text=True,
            timeout=90,
            cwd=skill_dir
        )
        
        # Parse result (find last JSON line)
        lines = result.stdout.strip().split('\n')
        for line in reversed(lines):
            try:
                return json.loads(line)
            except:
                continue
        
        return {
            "status": "error",
            "error": result.stderr or "Unknown error",
            "stdout": result.stdout
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Alex Chen Browser Automation')
    parser.add_argument('action', choices=['send', 'test'])
    parser.add_argument('--to', help='Recipient email')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--body', help='Email body')
    
    args = parser.parse_args()
    
    try:
        alex = AlexChenBrowser()
        
        if args.action == 'test':
            print(f"✅ Alex Chen Browser Automation configured!")
            print(f"📧 Email: {alex.user}")
            print("✅ Ready to automate Gmail via browser")
            
        elif args.action == 'send':
            if not args.to or not args.subject:
                print("❌ Usage: --to recipient@email.com --subject 'Subject' --body 'Message'")
                sys.exit(1)
            
            print(f"📧 Sending email via browser to {args.to}...")
            result = alex.send_email_browser(args.to, args.subject, args.body or "")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
