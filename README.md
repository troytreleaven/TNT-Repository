# 🎯 Dale Carnegie Dashboard

Your personalized sales and operations dashboard with movable kanban boards, weekly targets tracking, and daily check-ins.

## 📁 Dashboard Files

| File | Purpose |
|------|---------|
| `index.html` | Main dashboard with weekly targets overview |
| `kanban.html` | Movable kanban board for tasks and pipeline |
| `appointments.html` | Appointment scheduling and tracking |
| `pipeline.html` | Detailed pipeline by stage |
| `seats.html` | Niagara program enrollment tracker |

## 🚀 How to Use

1. **Open the dashboard:**
   ```bash
   # From terminal
   open /data/.openclaw/workspace/dashboard/index.html
   
   # Or double-click the file in your file manager
   ```

2. **Kanban Board:**
   - Drag and drop cards between columns
   - Click "+ Add Task" or "+ Add Deal" to create new items
   - Hover over cards to see delete button
   - Switch between Tasks and Pipeline tabs

3. **Track Progress:**
   - Check the main dashboard for weekly targets
   - Click any target card to see detailed view
   - Monitor Niagara seat count and pipeline value

## 🔔 Automated Check-ins

I've set up two daily reminders:

### 1. Daily Target Check-in (9:00 AM, Mon-Fri)
- Reminds you of weekly targets
- Asks: "What's your plan today?" and "What's one action you can take right now?"

### 2. Mid-Week Progress Review (2:00 PM, Wednesdays)
- Reviews progress on weekly targets
- Prompts reflection on what's working/needs attention

## 📊 This Week's Targets

- **Appointments:** 10
- **Seat target:** 6-8 (Niagara focus)
- **Pipeline added:** ~$30K
- **Focus:** Niagara closes + Boot Camp positioning
- **Milestone:** Niagara ≥18 seats; pipeline ≥$125K (2.5× moment)

## 🎨 Customization

Want to modify the dashboard? Just edit the HTML files:
- Change colors in the `<style>` section
- Add new columns to kanban
- Update targets in the summary cards
- Add new pages by copying a template

## 📝 Notes

- All data is currently static (for demo purposes)
- In the future, we can connect to Salesforce or Google Sheets for live data
- Kanban cards persist only during session (refreshing resets to defaults)

---

Built for Troy Treleaven - Dale Carnegie Training
