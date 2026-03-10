# Alex Chen Skill - Gmail & Google Services Integration

## What It Does
Operates as "Alex Chen" — a professional coordinator identity with full Gmail and Google services access.

## Identity
- **Name:** Alex Chen
- **Role:** Operations Coordinator
- **Email:** alex.chen.dc.gta@gmail.com
- **Organization:** Dale Carnegie Training — Greater Toronto Area

## Capabilities

### 1. Email Automation
- Send emails as Alex Chen
- Read inbox (check for replies, verification codes)
- Template-based emails (meeting invites, follow-ups, introductions)

### 2. Google Calendar (Coming Soon)
- Create events
- Send calendar invites
- Check availability

### 3. Google Drive (Coming Soon)
- Create documents
- Share files
- Access shared drives

### 4. Browser Authentication (Coming Soon)
- Log into sites using Google OAuth
- Maintain session cookies
- Navigate authenticated sites

## How to Use

### Test Configuration
```bash
python3 /data/.openclaw/workspace/skills/alex-chen/gmail.py test
```

### Send Email
```bash
python3 /data/.openclaw/workspace/skills/alex-chen/gmail.py send \
  --to recipient@example.com \
  --subject "Meeting Invitation" \
  --body "Hi, let's meet next week."
```

### Check Inbox
```bash
python3 /data/.openclaw/workspace/skills/alex-chen/gmail.py inbox
```

### Use Templates (From Python)
```python
from gmail import AlexChenGmail

alex = AlexChenGmail()

# Send meeting invite
alex.send_template_email(
    to="client@company.com",
    template_name="meeting_invite",
    name="John",
    topic="Leadership Training",
    datetime="Tuesday, March 10 at 2:00 PM",
    duration="30 minutes",
    location="Zoom"
)

# Send introduction
alex.send_template_email(
    to="prospect@company.com",
    template_name="introduction",
    name="Sarah",
    message="I noticed your company is expanding its leadership team..."
)
```

## Security & Boundaries

### What Alex CAN Do:
- ✅ Send professional emails
- ✅ Receive and read emails
- ✅ Access Google Calendar
- ✅ Create Google Docs/Sheets
- ✅ Log into sites for automation

### What Alex WON'T Do:
- ❌ Send emails without Troy's approval
- ❌ Access Troy's personal accounts
- ❌ Sign up for paid services without authorization
- ❌ Share credentials with anyone
- ❌ Impersonate Troy or other real people

## Templates Available

### meeting_invite
Parameters: `name`, `topic`, `datetime`, `duration`, `location`

### follow_up
Parameters: `name`, `topic`, `message`

### introduction
Parameters: `name`, `message`

## Files
- `gmail.py` - Main email automation script
- `SKILL.md` - This documentation
- `.env` - Credentials (secure, not committed to git)

## Status
- ✅ Gmail sending/receiving
- ⏳ Google Calendar integration
- ⏳ Google Drive integration
- ⏳ Browser automation

## Created
March 1, 2026
For: Troy Treleaven / Dale Carnegie GTA
