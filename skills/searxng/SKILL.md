# SearxNG Skill

Privacy-respecting, self-hosted metasearch engine for OpenClaw.

## What is SearxNG?

SearxNG is a free internet metasearch engine which aggregates results from more than 70 search services. Users are neither tracked nor profiled.

**Key Benefits over Brave:**
- ✅ **Self-hosted** - Your searches stay on your server
- ✅ **No API limits** - Unlimited searches
- ✅ **Multiple engines** - Aggregates Google, Brave, DuckDuckGo, Bing, etc.
- ✅ **No tracking** - Privacy by design
- ✅ **Free** - No API costs

## Status

| Component | Status |
|-----------|--------|
| **Server** | ✅ Running on http://127.0.0.1:8888 |
| **JSON API** | ✅ Enabled |
| **Engines** | ✅ 70+ search engines aggregated |
| **Python Skill** | ✅ Ready |
| **Default Search** | ✅ Replaces Brave for all queries |

## Quick Start

### Search from command line:

```bash
python3 /data/.openclaw/workspace/skills/searxng/searxng_search.py "your query" general 10
```

### Search programmatically:

```python
from searxng_search import search, format_results

# General search
results = search("Dale Carnegie leadership", num_results=10)
print(format_results(results))

# Image search
images = search_images("teamwork photos", num_results=5)

# News search
news = search_news("leadership trends 2026", num_results=10)
```

## Available Categories

- `general` - Web search (default)
- `images` - Image search
- `news` - News articles
- `videos` - Video search
- `it` - IT/technical content
- `science` - Scientific content

## Search Engines Included

- Google
- Brave
- DuckDuckGo
- Bing
- Wikipedia
- GitHub
- Stack Overflow
- And 70+ more...

## Web Interface

Access SearxNG directly at: http://127.0.0.1:8888

## 🔥 DEFAULT SEARCH ENGINE

**SearxNG is now the default search for all OpenClaw queries!**

### Using the Default Adapter

```python
# NEW WAY (SearxNG - default)
from skills.searxng.default_search import web_search

results = web_search("Dale Carnegie leadership training", count=10)

# Returns results in Brave-compatible format:
# [
#   {
#     "title": "...",
#     "url": "...",
#     "description": "...",
#     "site_name": "..."
#   }
# ]
```

### For OpenClaw Skills

Any skill using the `web_search` tool will now automatically use SearxNG instead of Brave:

```python
# This now uses SearxNG instead of Brave:
results = web_search(query="prospect research", count=10)
```

### Benefits
- ✅ **Drop-in replacement** - Same API as Brave
- ✅ **No code changes** - Existing skills work unchanged
- ✅ **Unlimited** - No API quotas
- ✅ **Faster** - Local server, no network latency
- ✅ **Private** - Searches stay local

### Fallback to Brave

If SearxNG is unavailable, you can still use Brave:

```python
# Import directly from searxng module
from skills.searxng.searxng_search import search

# Or use the original web_search tool (requires Brave API key)
# from web_search import web_search as brave_search
```

## Advantages for Dale Carnegie Business

1. **Unlimited searches** - No API quotas
2. **Prospect research** - Search company info, executives
3. **Content research** - Leadership articles, training materials
4. **Competitive intel** - Find competitor information
5. **News monitoring** - Track industry trends

## Troubleshooting

If the server isn't responding:

```bash
# Check if running
curl http://127.0.0.1:8888

# Restart server
cd /data/.openclaw/searxng
pkill -f "python3 searx/webapp.py"
export PYTHONPATH=/data/.openclaw/searxng:$PYTHONPATH
export SEARXNG_SETTINGS_PATH=/data/.openclaw/searxng/settings.yml
nohup python3 searx/webapp.py > /tmp/searxng.log 2>&1 &
```

## Configuration

Settings file: `/data/.openclaw/searxng/settings.yml`

Key settings:
- `instance_name` - Display name
- `formats` - Output formats (html, json)
- `engines` - Enabled search engines
- `server.port` - Port number (8888)

## Security Notes

- Server binds to localhost only (127.0.0.1)
- Not accessible from external networks
- No API key required
- No tracking or logging
