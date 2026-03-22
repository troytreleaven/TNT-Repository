# Jarvis Qwilr Architect Skill

## Purpose
Transform raw sales notes into high-conversion, visually stunning Qwilr Pages using the Qwilr API.

## Design Philosophy
- **Never "Wall of Text"**: Never place two Text Blocks consecutively. Always separate them with a Visual Break (Image, Quote, or Splash).
- **F-Pattern Flow**: Splash → Problem/Solution (Text) → Quote → Call-to-Action
- **Branding**: Use primary brand color for headers and buttons

## Block Selection
| Block Type | Use For | Style |
|------------|---------|-------|
| Splash | Title/Hero | High-res background image, centered |
| Text | Solution details | `<h2>` headers, `<ul>` for scannability |
| Quote | Impact Statement | Pull-quote, visual break |
| Accept | Call-to-Action | Branded button, "Next Steps" |

## Usage

### Command Line
```bash
# Create from command line
python3 qwilr_architect.py create "Client Name" "sales notes text..."

# Interactive mode
python3 qwilr_architect.py interactive

# Test connection
python3 qwilr_architect.py test
```

### Within OpenClaw
1. Load the sales notes or client information
2. Run: `python3 /data/.openclaw/workspace/skills/qwilr-architect/qwilr_architect.py create "<client>" "<notes>"`

## API Key
Stored at: `/data/.openclaw/workspace/.env.qwilr`

## Branding Reference
See: `/data/.openclaw/workspace/memory/dale-carnegie-branding.md`

## Example
Input: Sales notes for a leadership training proposal
Output: Qwilr page with Splash, Text, Quote, Accept blocks in Dale Carnegie branding