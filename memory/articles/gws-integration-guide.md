# Google Workspace CLI (gws) Integration for OpenClaw

**Article Saved:** March 6, 2026  
**Source:** Misbah Syed / Clawable.ai

---

## Overview
Google released `gws` - a command-line tool that gives AI agents direct access to Gmail, Google Drive, Calendar, Sheets, Docs, Slides, Chat, Tasks, Meet, Forms, Keep, Classroom, Admin, and every Google Workspace API. Ships with 100+ agent skills and native OpenClaw support.

---

## Key Features

### Architecture
- **Built in Rust** - Fast, reliable
- **Live Discovery Service** - Pulls Google's live API catalog, always current
- **Structured JSON Output** - Machine-readable responses for agents
- **Self-updating** - No manual updates needed

### Skill Categories (100+ Skills)

#### Service Skills (25+)
- `gws-drive` - Files, folders, shared drives
- `gws-gmail` - Send, read, manage email
- `gws-calendar` - Calendar and events
- `gws-sheets` - Spreadsheets
- `gws-docs` - Google Docs
- `gws-slides` - Presentations
- `gws-tasks` - Task lists
- `gws-chat` - Google Chat spaces/messages
- `gws-people` - Contacts and profiles
- `gws-admin` - Users, groups, devices
- `gws-classroom` - Classes, rosters, coursework
- `gws-forms` - Google Forms
- `gws-keep` - Google Keep notes
- `gws-meet` - Conference management
- `gws-vault` - eDiscovery
- `gws-apps-script` - Apps Script projects

#### Persona Skills (10 Pre-Built Agent Roles)
1. **Executive Assistant** - Schedules, inbox, communications
2. **Project Manager** - Projects, tasks, meetings
3. **HR Coordinator** - Onboarding, announcements
4. **Sales Ops** - Sales workflows, deals, calls
5. **IT Admin** - Users, security, Workspace config
6. **Content Creator** - Content creation and distribution
7. **Customer Support** - Tickets, responses, escalation
8. **Event Coordinator** - Events, invitations, logistics
9. **Team Lead** - Standups, task coordination
10. **Researcher** - Research organization, references

#### Helper Skills
- `gws-drive-upload` - Quick file uploads
- `gws-gmail-send` - Quick email sending
- `gws-modelarmor-sanitize-prompt` - Prompt cleaning

#### Recipe Skills (50 Workflows)
- Audit externally shared Drive files
- Send personalized emails from Sheets
- Common productivity automations

---

## Installation

### Quick Start (5 Minutes)
```bash
# 1. Install the CLI
npm install -g @googleworkspace/cli

# 2. Set up auth (walks through everything)
gws auth setup

# 3. Login to Google Workspace account
gws auth login
```

### OpenClaw Integration

#### Option 1: Symlink All Skills (Recommended)
```bash
# Clone the repo
git clone https://github.com/googleworkspace/cli.git
cd cli

# Symlink all skills into OpenClaw skills directory
ln -s $(pwd)/skills/gws-* ~/.openclaw/skills/
```

#### Option 2: Copy Specific Skills
```bash
# Only grab what you need
cp -r skills/gws-drive skills/gws-gmail ~/.openclaw/skills/
```

#### Option 3: Use Skills CLI
```bash
# Install all skills at once
npx skills add https://github.com/googleworkspace/cli

# Or pick individual skills
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-drive
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-gmail
```

---

## Usage Examples

### Gmail
```bash
# Search unread emails from specific sender
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:boss@company.com is:unread"}'

# Send email
gws gmail +send --to alice@company.com --subject 'Q2 Report Ready' \
  --body 'Hey Alice, the Q2 report is ready for review.'

# Triage unread inbox
gws gmail +triage --max 5 --query 'from:boss'
```

### Calendar
```bash
# Today's agenda
gws calendar +agenda

# Create meeting
gws calendar +insert --summary 'Weekly Standup' \
  --start '2026-03-10T09:00:00-07:00' \
  --end '2026-03-10T09:30:00-07:00'
```

### Drive
```bash
# List recent files
gws drive files list --params '{"pageSize": 10}'

# Upload file
gws drive +upload --file ./report.pdf --parent FOLDER_ID

# Create folder
gws drive files create \
  --json '{"name": "Q2 Project", "mimeType": "application/vnd.google-apps.folder"}'
```

### Sheets
```bash
# Read data
gws sheets +read --spreadsheet-id SHEET_ID --range 'Contacts!A2:C'

# Append row
gws sheets +append --spreadsheet-id SHEET_ID --range 'Sheet1' \
  --values '["2026-03-05", "Marketing", "Ad spend", "1500"]'
```

### Docs
```bash
# Create document
gws docs documents create --json '{"title": "Meeting Notes - March 2026"}'

# Write content
gws docs +write --document-id DOC_ID \
  --text '## Project: Q2 Launch\n### Objective Launch by end of Q2.'
```

---

## Security: Model Armor Integration

Built-in safety filtering for agent responses:
```bash
gws gmail users messages get --params '...' \
  --sanitize "projects/P/locations/L/templates/T"
```

- **Warn mode** - Flags suspicious content but returns it
- **Block mode** - Strips out malicious content

Important: 26% of 31,000+ ClawHub skills contain vulnerabilities; 63% of exposed OpenClaw instances are misconfigured.

---

## Benefits for OpenClaw

1. **Native Support** - Built-in OpenClaw compatibility
2. **100+ Skills** - Ready to use immediately
3. **Auto-updating** - Always current with Google APIs
4. **Structured JSON** - Perfect for agent parsing
5. **Persona Bundles** - Complete agent roles out of the box
6. **Helper Commands** - Simplified common operations
7. **Security Built-in** - Model Armor integration

---

## Implementation Notes

### For Dale Carnegie Use Cases
- **Sales Ops persona** - Manage leads, track deals, schedule calls
- **Executive Assistant persona** - Schedule management, inbox triage
- **Content Creator persona** - Training materials, presentations
- **Event Coordinator persona** - Boot camp logistics, invitations

### Integration Priority
1. **gws-gmail** - Email automation for Alex Chen, sales team
2. **gws-calendar** - Schedule management, boot camp planning
3. **gws-drive** - Document storage, training materials
4. **gws-sheets** - Lead tracking, expense reports
5. **gws-docs** - Proposal creation, meeting notes

---

## Next Steps for Implementation

1. [ ] Install gws CLI globally
2. [ ] Authenticate with Google Workspace
3. [ ] Symlink relevant skills to OpenClaw
4. [ ] Test basic operations (email, calendar)
5. [ ] Configure persona skills for Dale Carnegie workflows
6. [ ] Document custom recipes for common tasks

---

**Raw Article Location:** See `/data/.openclaw/workspace/memory/articles/gws-integration-article-raw.md`
