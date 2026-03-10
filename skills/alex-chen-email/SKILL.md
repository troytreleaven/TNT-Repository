# Alex Chen Email Skill

Send and receive emails as Alex Chen — Dale Carnegie GTA Operations Coordinator.

## Features

- ✅ Send emails via Gmail SMTP
- ✅ Read inbox via IMAP
- ✅ Send professional Dale Carnegie inquiry responses
- ✅ Test connection to verify setup

## Setup Status

| Component | Status |
|-----------|--------|
| Gmail account | ✅ Created (alex.chen.gta.dc@gmail.com) |
| 2FA enabled | ✅ Yes |
| App password | ✅ Configured |
| SMTP access | ✅ Ready |
| IMAP access | ✅ Ready |

## Usage

### Test Connection
```bash
cd /data/.openclaw/workspace/skills/alex-chen-email
python3 email_client.py test
```

### Read Inbox
```bash
# Read last 10 emails
python3 email_client.py read

# Read last 5 emails
python3 email_client.py read 5

# Read only unread
python3 email_client.py read-unread
```

### Send Email
```bash
python3 email_client.py send prospect@company.com "Subject Line"
# Then type body and press Ctrl+D
```

### Send Auto-Reply (Dale Carnegie Template)
```bash
python3 email_client.py auto-reply prospect@company.com "Prospect Name"
```

## Next Enhancements

- [ ] Auto-respond to common inquiries
- [ ] Calendar integration (schedule meetings)
- [ ] Email templates library
- [ ] Sentiment analysis for incoming emails
- [ ] CRM integration (log emails to Salesforce)

## Credentials

Stored securely in: `/data/.openclaw/workspace/skills/groq-voice/.env`

**Never commit credentials to git!**
