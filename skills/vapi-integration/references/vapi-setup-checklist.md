# VAPI.ai Setup Checklist

Use this checklist when onboarding a new VAPI.ai account (Alex Chen or future teammates).

## Account & Authentication
1. Navigate to https://vapi.ai and click **Sign Up**.
2. Register using the assigned Gmail (e.g., alex.chen.gta.dc@gmail.com).
3. Verify the inbox for the confirmation email and complete the activation.
4. In the VAPI dashboard, go to **Settings → API Keys**.
5. Click **Generate New Key**. Copy the key (format: `vapi-xxxxx`).
6. Store the key in `/data/.openclaw/workspace/skills/groq-voice/.env`:
   ```bash
   echo "VAPI_API_KEY=vapi-your-key-here" >> /data/.openclaw/workspace/skills/groq-voice/.env
   ```
7. Record the key location inside secrets tracker if required.

## Integration with Alex Chen Workflows
1. Confirm Alex can access `/data/.openclaw/workspace/skills/groq-voice/` for environment updates.
2. Reload any services that depend on the `.env` file (e.g., restart groq-voice scripts if running persistently).
3. Update configuration for any voice bots or agents to include:
   - `provider: vapi`
   - API key path or value
   - Webhook/call routing settings
4. Test by running a quick voice interaction (sample CLI provided in SKILL instructions).

## Testing & Validation
1. Run `python3 skills/groq-voice/voice_chat.py --mode demo` to ensure ElevenLabs/Groq pipeline still works.
2. Create a sample VAPI agent in the dashboard (e.g., "Alex Voice Concierge") and copy its Agent ID.
3. Send a test call or simulate conversation via VAPI console.
4. Confirm transcripts/responses arrive in OpenClaw logs.
5. When successful, notify Troy with:
   - Account owner (email)
   - API key location
   - Test date & result

## Troubleshooting
- **401 Unauthorized**: Regenerate the key and update `.env`.
- **Webhook failures**: Ensure OpenClaw gateway (port 18789) is reachable from VAPI callbacks.
- **Audio quality issues**: Adjust voice settings in VAPI agent config or verify ElevenLabs credentials.
