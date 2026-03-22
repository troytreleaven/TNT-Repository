---
name: vapi-integration
description: Procedures and scripts for onboarding VAPI.ai voice agents (e.g., Alex Chen) — create accounts, secure API keys, update groq-voice env files, and validate the integration with OpenClaw. Use when asked to set up or troubleshoot VAPI.ai for Alex or other team members.
---

# VAPI Integration Skill

Use this skill whenever Troy asks to "set up VAPI" for Alex Chen or any other teammate. It covers account creation, secure credential storage, and validation with the existing groq-voice pipeline.

## Before You Start
- You must have the teammate's Gmail credentials (Alex: `alex.chen.gta.dc@gmail.com`).
- Ensure `/data/.openclaw/workspace/skills/groq-voice/.env` is writable (stores voice credentials).
- Gateway + browser must be healthy (VAPI uses web callbacks).

## Workflow Summary
1. **Create/verify VAPI account**
2. **Generate API key & store securely**
3. **Update groq-voice environment**
4. **Configure a starter agent in VAPI dashboard**
5. **Run validation call/demo**
6. **Report status to Troy**

Detailed checklist: [`references/vapi-setup-checklist.md`](references/vapi-setup-checklist.md)

---
## 1. Create / Verify Account
1. Open https://vapi.ai → **Sign Up** (or **Login** if already created).
2. Register with the teammate's Gmail.
3. Confirm the verification email.

> **Tip:** If multi-factor auth is enabled on the Gmail, be ready to confirm the login from Troy's device.

## 2. Generate API Key & Store It
1. VAPI Dashboard → **Settings → API Keys → Generate New Key**.
2. Copy the key (format `vapi-xxxxx`).
3. Append it to the groq-voice `.env`:
   ```bash
   echo "VAPI_API_KEY=vapi-your-key-here" >> /data/.openclaw/workspace/skills/groq-voice/.env
   ```
4. Record the key location (and optionally checksum) in Troy's secrets tracker.

## 3. Update groq-voice Config
If groq-voice scripts reference the `.env`, restart any persistent processes so the new variable loads:
```bash
cd skills/groq-voice
python3 voice_chat.py --mode demo
```
This confirms existing ElevenLabs/Groq credentials still work before adding VAPI on top.

## 4. Create a Starter Agent in VAPI
1. In VAPI dashboard → **Agents → New Agent**.
2. Suggested defaults:
   - Name: "Alex Voice Concierge"
   - Provider: choose GPT-4o / Llama (match Troy's preference)
   - Voice: pick a neutral North American voice
   - Webhook URL: `https://<gateway-domain>/vapi/webhook` (adjust once route is defined)
3. Save the Agent ID for logging.

## 5. Validate End-to-End
1. Use VAPI console to simulate a call/chat.
2. Confirm OpenClaw receives the webhook/transcript (check gateway logs).
3. If hooking into Alex's workflows, send a test voicemail or SMS and confirm it appears in the relevant topic/thread.

## 6. Report Back to Troy
Send Troy a summary that includes:
- Account owner email
- Location of API key (.env path)
- Agent ID / name created
- Date & result of validation test
- Any follow-up actions (e.g., need DNS entry for webhook)

## Troubleshooting
| Issue | Fix |
|-------|-----|
| 401 Unauthorized from VAPI | Regenerate API key and re-run step 2 |
| Webhook timeout | Confirm gateway port 18789 accessible; check firewall |
| No audio / choppy calls | Adjust VAPI agent voice settings or verify ElevenLabs creds |
| Alex lacks access | Ensure he can SSH or use OpenClaw interface to update `.env` |

See [`references/vapi-setup-checklist.md`](references/vapi-setup-checklist.md) for the full checklist and troubleshooting notes.

---
## Re-running / Future Users
- Repeat the workflow for each teammate; store each key in the same `.env` or create dedicated files (document in summary to Troy).
- If multiple VAPI agents are needed (e.g., Sales bot, Support bot), reuse this skill and adjust the agent creation step accordingly.

## When to Escalate
- Account creation blocked (captcha failure, IP restrictions)
- Webhook needs DNS changes or SSL certs
- Need to integrate with existing telephony (Twilio, SIP)

Escalate to Troy before spending budget or making infrastructure changes.
