# Jarvis Emergency Recovery Guide
## Step-by-Step Instructions for Troy

---

## 📋 OVERVIEW

This guide shows you exactly how to restart Jarvis if he ever goes down, directly from your computer's terminal.

---

## 🖥️ STEP 1: OPEN YOUR TERMINAL

### On Mac (MacBook/iMac):
1. Press `Command + Space` (opens Spotlight search)
2. Type: `terminal`
3. Press `Enter`
4. A black window with white text opens — this is your terminal

### On Windows (PC):
1. Press `Windows key + R`
2. Type: `cmd`
3. Press `Enter`
4. A black window opens — this is Command Prompt

---

## 🔑 STEP 2: CONNECT TO YOUR SERVER

You need to SSH (secure shell) into the computer where Jarvis runs.

### Type this command in your terminal:

```bash
ssh node@YOUR_SERVER_IP
```

**Replace `YOUR_SERVER_IP` with your actual server IP address.**

*Example:*
```bash
ssh node@192.168.1.100
```

### When prompted for password:
- Type your password (characters won't show — this is normal!)
- Press `Enter`

### You should see something like:
```
node@server:~$
```

✅ **You're now connected to your server!**

---

## 🔍 STEP 3: CHECK IF JARVIS IS ALIVE

### Run this command:
```bash
openclaw status
```

### What to look for:

✅ **GOOD (Jarvis is working):**
```
│ Gateway         │ local · ws://127.0.0.1:18789 · reachable 67ms · auth token ·
│ Telegram    │ ON      │ OK     │ token config · accounts 1/1
```

❌ **BAD (Jarvis is down):**
```
│ Gateway         │ local · NOT reachable
│ Telegram    │ ON      │ ERROR  │ 
```

---

## 🔄 STEP 4: RESTART JARVIS

### If Jarvis is down, run this command:
```bash
openclaw gateway restart
```

### Wait 10 seconds, then check again:
```bash
openclaw status
```

### Try messaging Jarvis on Telegram. He should respond!

---

## 🌐 STEP 5: FIX BROWSER ISSUES

### If Jarvis replies but can't do web tasks:

**Run this command:**
```bash
/data/.openclaw/start-browser.sh
```

**You should see:**
```
Chromium started on port 18800 (PID: XXXX)
```

---

## 🚨 STEP 6: NUCLEAR OPTION (Complete Restart)

### If nothing else works:

**Run this command:**
```bash
/data/.openclaw/start-all.sh
```

This restarts everything: browser, gateway, and all services.

**Wait 30 seconds, then test.**

---

## 💾 STEP 7: DISCONNECT FROM SERVER

### When done, type:
```bash
exit
```

Or simply close the terminal window.

---

## 📱 QUICK REFERENCE CARD

### Commands You Need to Know:

| Command | What It Does |
|---------|--------------|
| `openclaw status` | Check if Jarvis is running |
| `openclaw gateway restart` | Restart Jarvis (most common fix) |
| `/data/.openclaw/start-browser.sh` | Fix browser/web tasks |
| `/data/.openclaw/start-all.sh` | Restart everything |
| `exit` | Disconnect from server |

---

## 🎯 SYMPTOM TROUBLESHOOTING

| What's Happening | Run This Command |
|------------------|------------------|
| Jarvis not replying to messages | `openclaw gateway restart` |
| "Can't reach browser" error | `/data/.openclaw/start-browser.sh` |
| Jarvis is slow/laggy | Wait for 4 AM auto-restart, or run `openclaw gateway restart` |
| Web tasks fail but text works | `/data/.openclaw/start-browser.sh` |
| Complete system crash | `/data/.openclaw/start-all.sh` |

---

## 📞 STILL NOT WORKING?

If none of these work, you may need to restart the entire Docker container:

```bash
docker restart openclaw
```

Wait 1 minute, then try messaging Jarvis.

---

## ✅ VERIFICATION CHECKLIST

After running any fix:

- [ ] Run `openclaw status` and see "reachable"
- [ ] Send Jarvis a test message on Telegram
- [ ] Wait for his reply (should be within 10 seconds)
- [ ] If he replies, you're good to go!

---

**Created:** March 3, 2026  
**For:** Troy Treleaven  
**Purpose:** Emergency Jarvis Recovery Procedures
