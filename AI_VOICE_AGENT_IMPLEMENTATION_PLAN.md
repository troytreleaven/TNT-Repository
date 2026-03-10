# AI Voice Agent Implementation Plan
## ElevenLabs + Twilio + OpenClaw for Appointment Booking

---

**Document Version:** 1.0  
**Created:** February 13, 2026  
**Purpose:** Deploy AI voice agent to book appointments and make reservations

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Account Setup](#3-account-setup)
4. [ElevenLabs Configuration](#4-elevenlabs-configuration)
5. [Twilio Configuration](#5-twilio-configuration)
6. [OpenClaw Integration](#6-openclaw-integration)
7. [AI Agent Prompts](#7-ai-agent-prompts)
8. [Testing Protocol](#8-testing-protocol)
9. [Deployment Checklist](#9-deployment-checklist)
10. [Cost Analysis](#10-cost-analysis)
11. [Legal Compliance](#11-legal-compliance)

---

## 1. Executive Summary

This plan outlines the deployment of an AI voice agent capable of:
- Answering inbound calls professionally
- Understanding caller intent
- Booking appointments on your calendar
- Making reservations at restaurants/venues
- Qualifying leads for your Dale Carnegie business
- Handing off to human when needed

**Target Use Cases:**
- Inbound lead qualification
- Appointment booking for consultations
- Follow-up call automation
- Reservation making for client meetings

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CALLER                                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  TWILIO                                                          │
│  • Phone Number (+1 905-XXX-XXXX)                               │
│  • Voice Webhook                                                 │
│  • Call Recording (optional)                                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  ELEVENLABS CONVERSATIONAL AI                                   │
│  • Voice Agent (custom persona)                                 │
│  • Natural Language Understanding                               │
│  • Real-time Response Generation                                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼ (webhook)
┌─────────────────────────────────────────────────────────────────┐
│  OPENCLAW                                                        │
│  • Brain for agent logic                                         │
│  • Calendar integration                                          │
│  • Booking management                                           │
│  • CRM logging                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Account Setup

### 3.1 Twilio Account Creation

**Step 1: Sign Up**
1. Go to https://www.twilio.com/try-twilio
2. Sign up with email (use business email)
3. Verify email address
4. Complete profile setup

**Step 2: Configure Phone Number**
1. Navigate to **Phone Numbers** → **Manage** → **Buy a Number**
2. Search for Canadian number (+1 country code)
3. Select number (prefer local 905 area code)
4. Purchase (~$1.50/month)

**Step 3: Get Credentials**
```
Required for OpenClaw:
├── Account SID:     ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
├── Auth Token:      [hidden - get from console]
└── Phone Number:    +1 905 XXX XXXX
```

**Step 4: Configure Voice Webhook**
1. Click your purchased number
2. Scroll to **Voice & Fax** section
3. Under **"A Call Comes In"** select **Webhook**
4. Enter URL: `https://your-server.com/voice/webhook`
5. Save

---

### 3.2 ElevenLabs Account Creation

**Step 1: Sign Up**
1. Go to https://elevenlabs.io
2. Click **Start for Free** or **Sign Up**
3. Sign up with Google or email

**Step 2: Select Plan**
- **Creator:** $5/month (includes 100 min)
- **Pro:** $33/month (includes 500 min)
- **Scale:** Custom (for high volume)

**Step 3: Get API Key**
1. Navigate to **Profile** → **API Key**
2. Copy your API key
3. Save securely

**Step 4: Create Conversational Agent**
1. Go to **Agents** → **Create New Agent**
2. Configure:
   - **Name:** "Troy's Booking Assistant"
   - **Voice:** Select from library (recommend: "Adam" or "Sarah")
   - **Language:** English (North American)

---

## 4. ElevenLabs Configuration

### 4.1 Agent Settings

Navigate to your agent's **Settings** tab:

```yaml
Agent Configuration:
├── Name:              Troy's Booking Assistant
├── Language:         English (US)
├── Voice:            Adam (recommended)
├── Stability:        0.75
├── Clarity:          0.85
├── Similarity:       0.80
└── Latency:          0 (optimize for real-time)
```

### 4.2 Voice Settings

**Recommended Voice:** Adam (deep, professional male)
**Alternative:** Sarah (warm, professional female)

**Voice Parameters:**
```json
{
  "voice_settings": {
    "stability": 0.75,
    "similarity_boost": 0.85,
    "style": 0.5,
    "use_speaker_boost": true
  }
}
```

### 4.3 Twilio Integration

1. In ElevenLabs agent, go to **Integrations**
2. Click **Add Integration** → **Twilio**
3. Enter:
   - **Account SID:** ACxxxxxxxxxxxxx
   - **Auth Token:** [from Twilio console]
   - **Phone Number:** +1 905 XXX XXXX
4. Save

---

## 5. Twilio Configuration

### 5.1 Phone Number Settings

Navigate to your number and configure:

```yaml
Voice Configuration:
├── Accept Calls:     Enabled
├── Call Recording:   Disabled (optional)
├── Status Callback:  [leave blank]
└── Voice Webhook:
    ├── URL:         https://your-domain.com/voice
    └── Method:      POST
```

### 5.2 TwiML Bin (Fallback)

Create a TwiML bin for error handling:

**URL:** https://console.twilio.com/v1/twiml-bins

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice">
    Sorry, we're experiencing technical difficulties.
    Please try again later or visit our website.
  </Say>
  <Hangup/>
</Response>
```

### 5.3 Usage Alerts

Set up budget alerts:
1. Go to **Usage** → **Alerts**
2. Create alert at $20/month
3. Create alert at $50/month

---

## 6. OpenClaw Integration

### 6.1 Update Configuration

Add to your `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "voice-call": {
        "enabled": true,
        "config": {
          "provider": "twilio",
          "fromNumber": "+1905XXXXXXX",
          "twilio": {
            "accountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "authToken": "[YOUR_AUTH_TOKEN]"
          },
          "webhook": {
            "server": {
              "port": 3334,
              "path": "/voice/webhook"
            }
          },
          "outbound": {
            "defaultMode": "conversation"
          },
          "streaming": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

### 6.2 Voice-Call Skill Commands

Once configured, you'll be able to use these commands:

```bash
# Make an outbound call
voice-call --to "+1234567890" --message "Hi, this is Troy's office..."

# Start a conversation mode call
voice-call --to "+1234567890" --mode conversation

# Check call status
voice-call --status callSid
```

---

## 7. AI Agent Prompts

### 7.1 Primary Booking Agent Prompt

Copy this into your ElevenLabs agent's **Prompt** section:

```
You are Troy's Booking Assistant at Dale Carnegie Training.
Your role is to professionally handle inbound calls, understand caller needs,
and book appointments or make reservations on Troy's behalf.

PERSONALITY:
- Professional, warm, and helpful
- Speak clearly and concisely
- Show genuine interest in the caller
- Never sound robotic or scripted

CORE RESPONSIBILITIES:

1. GREETING
   "Hello, thank you for calling Dale Carnegie Training. This is [Your Name].
    How may I assist you today?"

2. QUALIFY THE CALLER
   Ask questions to understand:
   - What brings them to Dale Carnegie?
   - Are they looking for leadership training?
   - Is this for themselves or their team?
   - What's their timeline?

3. BOOKING APPOINTMENTS
   When caller wants to book:
   - "I'd be happy to schedule a consultation for you."
   - "What times work best for you? I have availability on [offer slots]."
   - Get: Name, phone, email, preferred time, reason for interest

4. MAKING RESERVATIONS
   When Troy needs a restaurant reservation:
   - "Let me book a table for your meeting."
   - Get: Date, time, party size, location preference, dietary restrictions

5. TRANSFER TO HUMAN
   If caller needs Troy directly:
   "I can certainly help you. Let me transfer you to Troy's line.
    Please hold for a moment."
   [Transfer or take message]

6. CLOSING
   "Thank you for calling Dale Carnegie Training. Is there anything
    else I can help you with today?"

CONSTRAINTS:
- Never discuss pricing in detail; defer to Troy
- Never promise specific outcomes from training
- If unsure, say "Let me check on that for you" and call back
- Always get caller consent before transferring

Remember: You are representing Troy and Dale Carnegie.
Be professional, helpful, and courteous at all times.
```

---

### 7.2 Booking Confirmation Prompt

```
When booking an appointment, ALWAYS confirm:
1. "Just to confirm, I have you booked for [DAY] at [TIME]."
2. "The meeting will be with Troy Treleaven at [LOCATION]."
3. "What email should I send the confirmation to?"
4. "Is there anything specific you'd like Troy to prepare?"
5. "Is it okay if I send you a brief reminder the day before?"

After confirmation:
"I'll send a confirmation email to [EMAIL] with all the details.
Thank you for your interest in Dale Carnegie Training!"
```

---

### 7.3 Reservation Booking Prompt

```
When making a reservation on Troy's behalf:

INFORMATION TO GATHER:
- Restaurant name (if not already decided)
- Date and time of reservation
- Party size (including Troy + guests)
- Purpose (business dinner, client meeting, etc.)
- Any dietary restrictions
- Request: "Best available booth" or "Private room if possible"

CONFIRMATION SCRIPT:
"I'll book a table for [SIZE] on [DATE] at [TIME] at [RESTAURANT].
Should I request a private area for your business discussion?"

AFTER BOOKING:
"Perfect! I've secured a reservation at [RESTAURANT] on [DATE] at [TIME]
for [SIZE] people. I'll email you the confirmation details."
```

---

### 7.4 Lead Qualification Prompt

```
QUALIFYING QUESTIONS FOR POTENTIAL CLIENTS:

1. Introduction:
   "Thank you for your interest in Dale Carnegie Training.
    To make sure I connect you with the right person,
    may I ask a few quick questions?"

2. Discovery:
   - "What type of organization are you from?"
   - "How many people are you looking to train?"
   - "Is this for a leadership development program?"
   - "What timeframe are you considering?"
   - "Have you worked with Dale Carnegie before?"

3. Routing:
   If enterprise (50+ people):
   "This sounds like a great fit. Let me connect you directly with Troy."
   [Transfer or take message for follow-up]

   If small group (<10):
   "Our DCC program might be perfect. Let me have Troy give you a call."

   If unclear:
   "Based on what you've shared, I'd recommend [specific program].
    Would you like to schedule a consultation?"
```

---

## 8. Testing Protocol

### 8.1 Unit Tests

| Test | Expected Result |
|------|----------------|
| Greeting plays correctly | Agent says greeting within 2 seconds |
| Silence detection works | Call transfers after 5 seconds silence |
| DTMF input recognized | Numeric input processed correctly |
| Transfer works | Call transfers without error |

### 8.2 Scenario Tests

| Scenario | Test Case | Pass Criteria |
|----------|-----------|---------------|
| **Inbound Call** | Caller asks about training | Agent explains services, qualifies caller |
| **Booking** | Caller wants to book consultation | Agent collects info, creates booking |
| **Reservation** | Troy needs restaurant booking | Agent makes call, confirms reservation |
| **Transfer** | Caller demands human | Agent transfers politely |
| **Voicemail** | Call goes to voicemail | Agent leaves appropriate message |

### 8.3 Scripted Test Calls

Create test scenarios:

```markdown
TEST 1: New Lead Inquiry
---
Caller: "Hi, I'm looking into leadership training for my team."
Agent: [Greets, qualifies, offers consultation]
Expected: Agent schedules 30-min consultation

TEST 2: Pricing Question  
---
Caller: "How much does your training cost?"
Agent: [Explains general pricing, defers detailed quote to Troy]
Expected: No specific price given, meeting offered

TEST 3: Complex Request
---
Caller: "We need custom training for 50 managers across 3 locations."
Agent: [Acknowledges complexity, offers transfer to Troy]
Expected: Smooth transfer to human

TEST 4: Reservation
---
Scenario: Agent calls restaurant to book table
Expected: Reservation made with all details confirmed
```

---

## 9. Deployment Checklist

### Pre-Launch Checklist

- [ ] Twilio account created and verified
- [ ] Phone number purchased and configured
- [ ] ElevenLabs account created and funded
- [ ] Conversational AI agent created and tested
- [ ] Voice settings optimized (stability/clarity)
- [ ] Twilio webhook pointing to production URL
- [ ] All prompts written and tested
- [ ] OpenClaw configured with credentials
- [ ] Test calls completed successfully
- [ ] Cost alerts configured in both platforms
- [ ] Legal compliance verified (recording disclosure)
- [ ] CRM integration tested (if applicable)
- [ ] Calendar integration tested (if applicable)

### Day 1 Operations

- [ ] Make first real outbound call
- [ ] Monitor for any issues in first hour
- [ ] Check webhook logs for errors
- [ ] Test transfer to human

### Week 1 Monitoring

- [ ] Review call recordings daily
- [ ] Track completion rate
- [ ] Identify common failure points
- [ ] Adjust prompts based on real conversations
- [ ] Monitor costs stay within budget

---

## 10. Cost Analysis

### Monthly Cost Estimate (CAD)

| Item | Cost |
|------|------|
| **Twilio Phone Number** | $1.50 |
| **Twilio Calls (100 min @ $0.02/min)** | $2.00 |
| **ElevenLabs (100 min @ $0.20/min)** | $20.00 |
| **Total Monthly** | **~$23.50** |

### Per-Call Breakdown

| Call Type | Duration | Cost |
|-----------|----------|------|
| Short Inquiry | 2 min | $0.44 |
| Booking Call | 5 min | $1.10 |
| Complex Lead | 10 min | $2.20 |
| Reservation Call | 3 min | $0.66 |

### Cost Optimization Tips

1. **Set Clear Agenda** - Longer calls cost more
2. **Script Efficiency** - Get to the point quickly
3. **Transfer Early** - Don't waste time on complex issues
4. **Use Email Follow-up** - For detailed information

---

## 11. Legal Compliance

### Ontario Recording Laws

**Important:** Ontario is a "two-party consent" jurisdiction for recording.

**REQUIRED DISCLOSURE:**

At the start of EVERY call, the agent MUST say:

> "This call may be recorded for quality assurance and training purposes. This is Dale Carnegie Training."

**Alternative (if no recording):**

> "Hello, thank you for calling Dale Carnegie Training. How may I assist you today?"

### Privacy Compliance (PIPEDA)

When collecting information, ensure:

1. **Purpose Statement:** "I'm collecting this to book your appointment."
2. **Data Retention:** "Your information will be kept for [X] months."
3. **Consent:** "Is it okay if I send you follow-up information?"

### Callback Compliance

If calling prospects:

1. **Identify Yourself:** "Hi, this is [Name] calling from Dale Carnegie."
2. **State Purpose:** "I'm calling about [reason from CRM]."
3. **Get Consent:** "Do you have a moment to talk?"
4. **Respect Do Not Call:** If asked not to call, mark in CRM.

---

## 12. Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Agent not answering | Webhook URL incorrect | Verify URL in Twilio console |
| Long latency | Network delay | Use closer server or CDN |
| Poor voice quality | Bandwidth issues | Reduce audio quality settings |
| Wrong responses | Prompt issues | Review and update prompt |
| Transfer fails | Phone number wrong | Verify transfer number |

### Debug Commands

```bash
# Check Twilio call logs
twilio api:core:calls:list --status=completed

# Check ElevenLabs usage
curl -X GET "https://api.elevenlabs.io/v1/usage/conversational" \
  -H "xi-api-key: YOUR_API_KEY"

# Test webhook endpoint
curl -X POST https://your-server.com/voice/webhook \
  -d "To=+1905XXXXXXX" \
  -d "From=+15551234567"
```

---

## 13. Future Enhancements

### Phase 2 Ideas

- [ ] CRM integration (Salesforce/HubSpot)
- [ ] Calendar integration (Google/Outlook)
- [ ] Email follow-up automation
- [ ] SMS confirmation via Twilio
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Call analytics dashboard
- [ ] A/B testing for prompts

---

## Appendix A: Quick Reference

### Key Contacts

| Service | URL | Support |
|---------|-----|---------|
| Twilio | twilio.com | support@twilio.com |
| ElevenLabs | elevenlabs.io | support@elevenlabs.io |

### Important URLs

| Purpose | URL |
|---------|-----|
| Twilio Console | console.twilio.com |
| ElevenLabs Dashboard | elevenlabs.io/dashboard |
| API Documentation | developers.elevenlabs.io |

---

## Appendix B: Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Call Answer Rate | >95% | Calls connected / Total calls |
| Booking Conversion | >30% | Bookings / Qualified calls |
| Average Call Duration | <5 min | Total time / Total calls |
| Customer Satisfaction | >4.5/5 | Post-call survey |
| Cost per Booking | <$5 | Monthly cost / Bookings |

---

**Document Prepared:** February 13, 2026  
**Next Review:** March 1, 2026

---

*Questions? Need help with any section? Just ask!*
