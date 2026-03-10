#!/usr/bin/env python33
import json, os, re, sys
from urllib.request import urlopen, Request

URL = "https://en.wikipedia.org/wiki/2026_Winter_Olympics_medal_table"
STATE_PATH = os.path.expanduser("/data/.openclaw/workspace/olympics_canada_medals_state.json")
USER_AGENT = "OpenClaw-MedalWatch/1.0"

def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")

def extract_canada_totals(html: str):
    # Look for a table row containing '>Canada<' then capture the next 4 numeric cells (G,S,B,Total)
    # This is intentionally regex-y to avoid external deps.
    # Works for common Wikipedia medal-table markup.
    m = re.search(r"<tr[^>]*>\s*(?:.*?)(?:>Canada<)(?:.*?</tr>)", html, flags=re.I|re.S)
    if not m:
        return None
    row = m.group(0)
    # Extract all cell numbers in the row and take the last 4 as (gold, silver, bronze, total)
    # (earlier numbers may include rank, tiebreakers, etc.)
    all_nums = [int(x) for x in re.findall(r"<t[dh][^>]*>\s*(\d+)\s*</t[dh]>", row)]
    if len(all_nums) < 4:
        # Fallback: any isolated numeric text between tags
        all_nums = [int(x) for x in re.findall(r">\s*(\d+)\s*<", row)]
    if len(all_nums) < 4:
        return None
    gold, silver, bronze, total = all_nums[-4:]
    return {"gold": gold, "silver": silver, "bronze": bronze, "total": total}

def load_state():
    if not os.path.exists(STATE_PATH):
        return None
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None

def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f)

def main():
    try:
        html = fetch(URL)
    except Exception as e:
        print(f"MedalWatch: fetch failed: {e}")
        return 2

    cur = extract_canada_totals(html)
    if not cur:
        print("MedalWatch: couldn't parse Canada's medal totals yet (page may not be updated).")
        return 0

    prev = load_state()
    save_state(cur)

    if not prev:
        print(f"MedalWatch: baseline saved. Canada medals now: {cur['gold']}G {cur['silver']}S {cur['bronze']}B (Total {cur['total']}).")
        return 0

    if cur["total"] > prev.get("total", -1):
        dg = cur['gold'] - prev.get('gold', 0)
        ds = cur['silver'] - prev.get('silver', 0)
        db = cur['bronze'] - prev.get('bronze', 0)
        print(
            "Canada just gained medal(s) at Milano Cortina 2026. "
            f"Now: {cur['gold']}G {cur['silver']}S {cur['bronze']}B (Total {cur['total']}). "
            f"Change: +{dg}G +{ds}S +{db}B.\n"
            f"Source: {URL}"
        )
        return 0

    print("MedalWatch: no new Canada medals since last check.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
