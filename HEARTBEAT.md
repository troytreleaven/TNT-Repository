# HEARTBEAT.md - System Health Checks

# Health check configuration for OpenClaw monitoring
# This file is checked every hour by the heartbeat system

## CRITICAL: Maximum Uptime Protocol
**Troy's Priority:** Keep Jarvis online at all times. Auto-restart everything.

## Health Check Instructions

Read this file and perform the following checks during each heartbeat:

### 1. **Check Gateway Status** (CRITICAL)
- Run: `openclaw status`
- If gateway is not running or shows errors:
  - Run: `openclaw gateway restart`
  - ALERT: "🚨 Gateway restarted - was down"

### 2. **Check Telegram Connectivity** (CRITICAL)
- Verify Telegram channel is responsive
- If Telegram messages are not going through:
  - ALERT: "📱 Telegram connectivity issue - check immediately"

### 3. **Check Browser Service** (CRITICAL)
- Run: `curl -s http://127.0.0.1:18800/json/version`
- If no response:
  - Run: `/data/.openclaw/start-browser.sh`
  - ALERT: "🌐 Browser restarted - was down"

### 4. **Check Email Monitoring** (HIGH)
- Verify email credentials exist:
  - `/data/.openclaw/workspace/.env.troy` (Troy Gmail)
  - `/data/.openclaw/workspace/skills/groq-voice/.env` (Alex Chen)
- If missing, ALERT: "📧 Email credentials missing"

### 5. **Check Disk Space** (MEDIUM)
- Run: `df -h / | awk 'NR==2 {print $5}' | tr -d '%'`
- If usage > 90%, ALERT: "💾 Disk space critical (>90%)"

### 6. **Check Recent Session Activity**
- Check if there have been any sessions in the last hour
- If no activity but gateway is running, reply: HEARTBEAT_OK

### 7. **Check for Stuck Processes**
- Look for any background processes that may be hanging
- If found, ALERT: "⚠️ Stuck process detected"

## Auto-Restart Scripts (Use These!)

```bash
# Quick browser restart
/data/.openclaw/start-browser.sh

# Full system startup
/data/.openclaw/start-all.sh

# Gateway restart
openclaw gateway restart
```

## Response Guidelines

- If ALL checks pass: Reply "HEARTBEAT_OK"
- If ANY check fails: 
  1. **Attempt auto-restart FIRST**
  2. Then ALERT Troy with details
- If uncertain: Reply "HEARTBEAT_OK" but note concern

## Last Updated
2026-03-03 - Added maximum uptime safeguards, browser health checks, auto-restart protocol
