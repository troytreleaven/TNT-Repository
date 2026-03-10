#!/usr/bin/env python3
"""Daily OpenClaw spend/usage report.

This uses only local OpenClaw telemetry (sessions store) + provider usage snapshot
when available.

It is NOT perfect dollar accounting:
- sessions.json provides token totals per session, not per-day usage
- we approximate daily usage via delta from last snapshot

State is stored in: /data/.openclaw/workspace/openclaw_daily_spend_state.json
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

STATE_PATH = "/data/.openclaw/workspace/openclaw_daily_spend_state.json"
TZ = "America/New_York"


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}\n{p.stderr.strip()}")
    return json.loads(p.stdout)


def load_state():
    if not os.path.exists(STATE_PATH):
        return None
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f)


def fmt_int(n):
    return f"{n:,}"


def main():
    now = datetime.now(ZoneInfo(TZ))
    prev = load_state() or {}

    sessions = run_json(["openclaw", "sessions", "--json"])  # has sessions[].totalTokens/inputTokens/outputTokens/model/key
    status = run_json(["openclaw", "status", "--usage", "--json"])  # may include provider usage snapshots

    # Snapshot current totals per session key.
    cur_totals = {}
    cur_models = {}
    for s in sessions.get("sessions", []):
        key = s.get("key")
        total = int(s.get("totalTokens") or 0)
        cur_totals[key] = {
            "model": s.get("model"),
            "totalTokens": total,
            "inputTokens": int(s.get("inputTokens") or 0),
            "outputTokens": int(s.get("outputTokens") or 0),
            "updatedAt": s.get("updatedAt"),
        }
        m = s.get("model") or "unknown"
        cur_models.setdefault(m, 0)
        cur_models[m] += total

    # Deltas since last snapshot (approx daily usage).
    prev_totals = (prev.get("sessions") or {})
    deltas_by_model = {}
    deltas_by_session = {}

    for key, cur in cur_totals.items():
        prev_total = int((prev_totals.get(key) or {}).get("totalTokens") or 0)
        delta = cur["totalTokens"] - prev_total
        if delta < 0:
            # session compact/reset — treat as unknown; ignore negative
            delta = 0
        if delta:
            deltas_by_session[key] = {"model": cur.get("model"), "deltaTokens": delta}
            deltas_by_model.setdefault(cur.get("model") or "unknown", 0)
            deltas_by_model[cur.get("model") or "unknown"] += delta

    # Provider usage snapshot: structure may vary; best-effort extraction.
    provider_usage = status.get("usage") or status.get("providerUsage") or None

    lines = []
    lines.append(f"OpenClaw daily usage report — {now.strftime('%Y-%m-%d %H:%M %Z')}")

    if deltas_by_model:
        lines.append("\nSince last report (approx token deltas):")
        for model, delta in sorted(deltas_by_model.items(), key=lambda x: -x[1]):
            lines.append(f"- {model}: +{fmt_int(delta)} tokens")
    else:
        lines.append("\nSince last report: no token deltas detected (or first run).")

    lines.append("\nCurrent sessions (total tokens in each session):")
    for key, cur in sorted(cur_totals.items(), key=lambda kv: -(kv[1].get("totalTokens") or 0)):
        lines.append(f"- {key} ({cur.get('model')}): {fmt_int(cur.get('totalTokens') or 0)} total")

    if provider_usage:
        # keep it short; dump JSON compact if unknown schema
        try:
            compact = json.dumps(provider_usage, ensure_ascii=False)
            if len(compact) > 1200:
                compact = compact[:1200] + "…"
            lines.append("\nProvider usage snapshot (best-effort):")
            lines.append(compact)
        except Exception:
            pass
    else:
        lines.append("\nProvider usage snapshot: not available (depends on provider creds/endpoints).")

    # Save state for next day
    save_state({
        "ts": int(now.timestamp()),
        "tz": TZ,
        "sessions": cur_totals,
    })

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Daily usage report failed: {e}")
        sys.exit(2)
