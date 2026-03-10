# Troy Treleaven Email Monitoring Skill

Monitor Troy's primary Gmail inbox with draft responses ready for approval.

## Features

- ✅ **Monitor Primary Inbox** - Check for unread emails every 60 minutes
- ✅ **Draft Responses** - Pre-written responses awaiting Troy's approval
- ✅ **Respond as Troy** - Send emails with full Dale Carnegie signature
- ✅ **Respond as Virtual Assistant** - Professional VA responses with confidentiality notice
- ✅ **Smart Detection** - Auto-detects inquiry, scheduling, follow-up, or thank-you emails

## Setup Status

| Component | Status |
|-----------|--------|
| Gmail account | ✅ ttreleaven@gmail.com |
| 2FA enabled | ✅ Yes |
| App password | ✅ Configured |
| SMTP access | ✅ Ready |
| IMAP access | ✅ Ready |

## Usage

### Test Connection
```bash
cd /data/.openclaw/workspace/skills/troy-email
python3 troy_email.py test
```

### Check for New Emails (with Draft Responses)
```bash
python3 troy_email.py check
```

This will:
1. Check for unread emails
2. Display original message
3. Show **Draft Response as Troy** (for your editing/approval)
4. Show **Draft Response as Virtual Assistant** (Jarvis responding on your behalf)

### Send Email
```bash
python3 troy_email.py send recipient@example.com "Subject Line"
# Then type body and press Ctrl+D
```

## Response Options

### Option 1: Respond as Troy
- Full Dale Carnegie signature
- Professional tone
- [TROY TO ADD] placeholders for customization

### Option 2: Respond as Virtual Assistant (Jarvis)
- Acknowledges receipt
- States you're with customers
- **Confidentiality notice** included
- Professional VA signature

## Email Types Auto-Detected

- **Inquiries** - Training/program questions
- **Scheduling** - Meeting/calendar requests
- **Follow-ups** - Checking in/status updates
- **Thank you** - Gratitude messages
- **General** - Other correspondence

## Monitoring Schedule

**Check Frequency:** Every 60 minutes via cron job
**Alert Method:** Telegram notification with draft responses
**Auto-send:** Disabled (requires Troy's approval)

## Credentials

Stored securely in: `/data/.openclaw/workspace/.env.troy`

**Never commit credentials to git!**

## Next Enhancements

- [ ] One-click approve/send from Telegram
- [ ] Custom response templates
- [ ] CRM integration (auto-log to Salesforce)
- [ ] Sentiment analysis for prioritization
- [ ] Auto-archive after response
