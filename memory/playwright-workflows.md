# Jarvis Workflows - Playwright & Automation

## Playwright Browser Automation

### Capability
Navigate websites, click buttons, fill forms, extract data, take screenshots.

### Installed
- Playwright MCP skill from ClawHub (Feb 22, 2026)

---

## Playwright Workflows

### 1. Salesforce Navigation
**Use:** Navigate Salesforce CRM, update records, run reports
**Trigger:** "Navigate Salesforce and [action]"
**Notes:** 
- API is better for most things
- Use Playwright for UI wizards screenshots
- Reliable but fragile if UI changes

### 2. Competitor Monitoring
**Use:** Check competitor websites, pull pricing, course schedules
**Trigger:** "Run competitor monitoring" or scheduled weekly
**Output:** Competitor report for Eleanor (CSO)

### 3. Lead Research & Enrichment
**Use:** Visit company websites, scrape leadership team, about page, news
**Input:** Company list from LinkedIn/PhantomBuster
**Output:** Enriched CRM data for sales reps

### 4. Event Registration Automation
**Use:** Auto-fill registration forms, confirm attendance, send follow-ups
**Trigger:** "Set up registration for [event]"
**Used for:** Stretch Camps, boot camps, DCC programs

---

## When to Use Playwright vs API

| Task | Use |
|------|-----|
| CRM data updates | API (Salesforce) |
| Report generation | API |
| UI wizards | Playwright |
| Screenshots | Playwright |
| Website scraping | Playwright |
| Form submissions | Playwright |
| Complex clicking flows | Playwright |

---

## Commands

- "Navigate to [URL] and [action]"
- "Extract data from [website]"
- "Fill form at [URL]"
- "Take screenshot of [page]"

---

*Updated: Feb 22, 2026*
