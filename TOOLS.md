# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Telegram Groups
| Group Name | Chat ID |
|------------|---------|
| Troy's VAs (Joanna & Jen) | -978038902 |
| DT Crew | -4895683713 |
| TE Crew | -4942721032 |
| Marketing Reinvention | -4783349964 |
| Maritimes GTM | -4177101595 |

---

## Convex - Mission Control Task Board

**Deployment URL:** https://patient-fox-716.convex.cloud
**Project:** mc2
**Owner:** Troy Treleaven

### Schema
- Table: `tasks`
- Indexes: `by_status`, `by_assignee`, `by_assignee_status`

### Functions
- `tasks:getAll` - Get all tasks
- `tasks:getByStatus(status)` - Get tasks by status
- `tasks:getByAssignee(assignee)` - Get tasks by assignee
- `tasks:create(task)` - Create new task
- `tasks:update(id, updates)` - Update task
- `tasks:remove(id)` - Delete task

### Connection
Use Convex client to read/write tasks in real-time.


---

Add whatever helps you do your job. This is your cheat sheet.
