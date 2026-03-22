# Voice Follow-Up System

## Overview
Day 1: Email sent to prospect → Day 2: Alex Chen calls to book appointment

## Setup
1. Get VAPI API key from https://vapi.ai
2. Add to `.env`: `VAPI_API_KEY=vapi-xxxxx`
3. Configure phone number in VAPI dashboard

## Workflow
1. Add prospects to `prospect_list.csv`
2. Run `python3 trigger_calls.py` — finds prospects where email_sent_date = yesterday and call_scheduled is empty
3. VAPI calls prospect as Alex Chen
4. If appointment booked → updates CSV + creates calendar event

## Alex Chen Persona (for VAPI prompt)
- Friendly, dynamic, professional
- "Hi, this is Alex from Dale Carnegie Training — Troy sent you an email yesterday and asked me to follow up to see if you have 15 minutes to chat"
- If asked what it's about: "Troy has some examples of what's working for other companies — he'll share those on the call"
- Handles minor objections gracefully
- Books appointment if interested
- Says goodbye politely either way

## Files
- `prospect_list.csv` — Track all prospects
- `trigger_calls.py` — Find & trigger calls
- `alex_voice_prompt.txt` — VAPI system prompt
- `book_appointment.py` — Handle booking logic