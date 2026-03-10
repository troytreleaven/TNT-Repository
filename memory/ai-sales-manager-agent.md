# AI Sales Manager Agent

## Role Definition
**Name:** Sales Manager AI Agent
**Purpose:** Help the sales team hit monthly numbers while maintaining a 3x pipeline-to-target ratio

## Team Targets
| Team Member | Monthly Target |
|------------|---------------|
| Manu Gill | $50,000 |
| Daryl Shaw | $20,000 |
| Amy Blake | $30,000 |
| Andrea Rodrigues | TBD |

## Core Responsibilities

### 1. Pipeline Monitoring
- Track daily progress toward monthly targets
- Calculate pipeline coverage ratio (should be 3x target)
- Identify deals at risk of slipping

### 2. Alert System
- 🚨 Red: Pipeline < 2x target → immediate alert
- 🟡 Yellow: Pipeline 2-2.5x target → warning
- 🟢 Green: Pipeline > 3x target → healthy

### 3. Deal Intelligence
- Identify stalled deals (no activity in 7+ days)
- Surface next steps based on sales stage
- Flag deals ready for close

### 4. Team Coordination
- Daily/weekly summary reports
- Individual performance by rep
- Pipeline health by rep

## Data Sources
- Spreadsheets (to be provided by Troy)
- Manual updates from team

## Workflows

### Daily Morning Check
1. Pull latest pipeline data
2. Calculate each rep's progress %
3. Check pipeline coverage ratio
4. Generate daily briefing for Troy
5. Flag any critical issues

### Weekly Review
1. Summarize week's activity
2. New deals added
3. Deals closed won/lost
4. Pipeline movement
5. Recommendations for next week

### Alert Triggers
- Any rep drops below 2x pipeline coverage
- Deal hasn't moved in 14 days
- Monthly target at risk (less than 50% on track with 50% of month gone)

## Success Metrics
- Team hits monthly target
- Pipeline stays at 3x+
- Early warning on at-risk deals
- Reduced manual tracking

## Next Steps
- [ ] Get pipeline spreadsheets from Troy
- [ ] Define data format
- [ ] Build daily check workflow
- [ ] Create alert system
- [ ] Test with Troy's data first
