# SKILL.md - Doc Beautifier

## What This Skill Does
Takes raw documents (markdown, text, or chat content) and transforms them into professionally formatted Word documents with:
- Proper headings and hierarchy
- Styled tables
- Quote callouts
- Consistent formatting
- Page breaks between sections

## When to Use
- When Troy asks to "beautify" something
- When content is going to be shared externally
- When a document needs professional formatting
- When you receive content in chat that should be a Word doc

## How to Use

### Step 1: Run the Beautifier
```bash
python3 /data/.openclaw/workspace/skills/doc-beautifier/beautify.py <input_file> <output_name>
```

Or run interactively and it will ask for input.

### Step 2: Output Location
- Saves to: `/data/.openclaw/media/outbound/<output_name>.docx`
- Then send via message tool to Troy

## Key Script: beautify.py
Location: `/data/.openclaw/workspace/skills/doc-beautifier/beautify.py`

Current features:
- Dark blue headings (RGB: 0, 51, 102)
- Gold accent option
- Table styling
- Quote blocks
- Page breaks
- Professional margins

## Iteration Log

### v1.0 (2026-02-21) - Initial
- Basic markdown → Word conversion
- Tables for stats
- Quote styling
- Page breaks

### Ideas for v2.0:
- [ ] Add cover page option
- [ ] Support more color themes
- [ ] Auto-detect content type (podcast, proposal, report)
- [ ] Add company branding (Dale Carnegie logo)
- [ ] Export to PDF option

## How to Improve
1. Add new formatting options to beautify.py
2. Update this SKILL.md with new features
3. Test with sample documents
4. Note improvements in Iteration Log

## Remember
When receiving any document content from Troy, ALWAYS ask:
> "Want me to run the doc-beautifier skill on this?"

This applies to:
- Markdown files
- Chat content
- Text files
- Content meant for external sharing
