# Outlook Skill

Microsoft 365 integration for Outlook email and calendar via Microsoft Graph API.

## Features

- 📧 Read, list, and search emails
- 📅 Create and list calendar events
- 👤 Get user profile

## Setup

Credentials must be saved in `.env`:
```
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
DEFAULT_USER=your-email@domain.com
```

## Usage

```bash
# List recent emails
python3 outlook.py emails

# Read specific email
python3 outlook.py read-email <message-id>

# List calendar events
python3 outlook.py events

# Create calendar event
python3 outlook.py create-event "Meeting Title" "2026-03-10T14:00:00" "2026-03-10T15:00:00"

# Get user info
python3 outlook.py whoami
```

## Requirements

- Python 3.8+
- requests
- msal (Microsoft Authentication Library)
