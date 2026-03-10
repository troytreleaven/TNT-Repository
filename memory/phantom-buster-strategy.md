# AI Team Strategy Session: PhantomBuster Lead Extraction + Workshop Campaign

**Date:** February 22, 2026  
**Facilitator:** Jarvis (CEO)  
**Attending:** Eleanor (CSO), Marcus (Marketing), Quinn (QC), Sales Manager, Skeptic (New)

---

## Agenda

1. Introduce new team member: The Skeptic
2. PhantomBuster use case analysis
3. Lead targeting strategy for workshop campaigns
4. Cross-reference with Kevin's workshop ideas
5. Team debate and final recommendations

---

## 1. NEW TEAM MEMBER: THE SKEPTIC

### Agent Definition
**Name:** "Atlas" - The Skeptic  
**Purpose:** Challenge assumptions, find flaws in plans, push for rigor

### Core Responsibilities
1. **Question Every Assumption**
   - "What could go wrong?"
   - "Is this actually achievable?"
   - "What data supports this?"

2. **Stress-Test Strategies**
   - Identify blind spots
   - Find weaknesses in logic
   - Push back on groupthink

3. **Ensure Accountability**
   - Demand evidence for claims
   - Track what actually works vs. what we think works

### First Assignment
> "Review this strategy document and find every flaw, assumption, and risk we haven't considered."

---

## 2. PHANTOMBUSTER USE CASE ANALYSIS

### What PhantomBuster Actually Does

| Capability | applicability to Our Business |
|------------|------------------------------|
| **LinkedIn Lead Extraction** | ✅ Primary use - extract prospects from groups, events, company pages |
| **Company Data Enrichment** | ✅ Get company size, industry, headquarters from websites |
| **Email Finder** | ⚠️ Limited - not always accurate for Canada |
| **Multi-Platform** | ✅ Could also extract from events, news, job postings |

### What It Does NOT Do
- ❌ Send automated messages (that's Expandi's job)
- ❌ Integrate directly with Salesforce (requires manual export)
- ❌ Provide verified phone numbers

---

## 3. LEAD TARGETING STRATEGY

### Primary Target: Workshop Attendees

Based on our GTM strategy, we need to extract leads for these workshops:

#### Workshop #1: "Lead Through Stress & Uncertainty"
**Target ICP:**
- Industry: Healthcare, Finance, Technology, Manufacturing
- Company Size: 100-5,000 employees
- Geography: Ontario + Maritimes
- Job Titles: VP HR, Director L&D, COO, CEO (SME)

**PhantomBuster Extraction Strategy:**

| Source | Target Quantity | Priority |
|--------|-----------------|----------|
| LinkedIn Groups (HR Canada, L&D Network) | 500-1,000 | HIGH |
| LinkedIn Company Pages (target industries) | 300-500 | HIGH |
| Industry Events (past attendees) | 200-300 | MEDIUM |
| Job Postings (HR leadership roles) | 100-200 | LOW |

#### Workshop #2: "How to Lead Change" (Kevin's Idea)
**Target ICP:**
- Similar to Stress workshop
- Add: Companies recently announced layoffs, restructuring, mergers

**PhantomBuster Extraction Strategy:**

| Source | Target Quantity | Priority |
|--------|-----------------|----------|
| News mentions (restructuring, layoffs) | 200-400 | HIGH |
| LinkedIn Company Pages (growth companies) | 300-500 | MEDIUM |
| Chamber of Commerce directories | 200-300 | MEDIUM |

#### Workshop #3: "How to Lead Boldly" (Executive Level - Kevin)
**Target ICP:**
- C-Suite only (CEO, COO, CFO, CRO)
- Company Size: 500+ employees
- Industry: All sectors

**PhantomBuster Extraction Strategy:**

| Source | Target Quantity | Priority |
|--------|-----------------|----------|
| LinkedIn Connections (2nd degree) | 200-300 | HIGH |
| Executive networking groups | 100-200 | HIGH |
| Industry association membership lists | 100-150 | MEDIUM |

---

## 4. WORKFLOW: EXTRACTION TO ENROLLMENT

### The Complete Funnel

```
PHANTOMBUSTER EXTRACTION
    ↓
Data Enrichment & Cleaning
    ↓
Salesforce Import (Manual via CSV)
    ↓
SALES TEAM OUTREACH
    ↓
Workshop Registration
    ↓
Workshop Attendance
    ↓
Post-Workshop Survey (Quinn)
    ↓
Sales Consultation
    ↓
Lead with Impact Enrollment
```

### Role Assignments

| Stage | Owner | Notes |
|-------|-------|-------|
| Extraction | Marcus + Vin | Use PhantomBuster |
| Enrichment | Marcus | Clean data, remove dupes |
| Salesforce Import | Sales Manager | Manual upload (weekly) |
| Outreach | Sales Manager / Daryl / Manu | Personalized InMails |
| Workshop Delivery | Quinn / Trainer | Quality assurance |
| Follow-up | Sales Manager | Post-workshop outreach |

---

## 5. THE SKEPTIC'S CHALLENGES

### Atlas's Critical Questions

> **Q1: PhantomBuster data freshness**
> "LinkedIn updates their data constantly. How often do we re-extract? What's the half-life of a lead?"

**Team Response:** Extract monthly, prioritize recent activity signals (new hires, promotions)

> **Q2: Salesforce integration**
> "We're manual CSV uploads. What happens when we scale to 500+ leads/month? Won't the team drown in data entry?"

**Team Response:** This is a real constraint. Need to explore Zapier or API integration. May need to hire admin support.

> **Q3: Email deliverability**
> "PhantomBuster emails aren't verified. What's our sender reputation? Won't we get blocked?"

**Team Response:** Start with LinkedIn InMail only, use company email not generic

> **Q4: Competition**
> "Everyone is doing this. What makes our outreach different?"

**Team Response:** Dale Carnegie brand + workshop value proposition

> **Q5: GDPR/Privacy**
> "These are Canadian companies. Have we checked privacy laws?"

**Team Response:** Need to verify - Canadian PIPLEDA applies

---

## 6. TEAM DEBATE: PHANTOMBUSTER VS. EXPANDI

### Marcus (Marketing): Pro-Expandi
> "Expandi does it all - extract AND message. One tool. Simpler."

### Atlas (Skeptic): Pro-PhantomBuster First
> "Expandi costs more and does less data extraction. Start cheap with PhantomBuster for lead lists, use manual outreach for now."

### Eleanor (CSO): Strategic Choice
> "PhantomBuster first to build the list. Once we prove the funnel works, then invest in Expandi for automation. Smart capital allocation."

### Quinn (QC): Quality Concern
> "Whichever we pick, need to track what actually converts. Don't want the team chasing dead leads."

### Sales Manager: Practical Input
> "Give me 50 quality leads I can personally outreach to over 500 mediocre ones any day."

---

## 7. FINAL RECOMMENDATION

### Phase 1: PhantomBuster (Immediate)
- **Cost:** ~$49/month (annual)
- **Action:** Extract leads for Stress workshop campaign
- **Goal:** Build list of 500 qualified prospects
- **Timeline:** 2 weeks to extraction + cleanup

### Phase 2: Manual Outreach (Month 1-2)
- **Action:** Sales team personally InMails extracted leads
- **Goal:** Workshop registrations
- **Metrics:** Track conversion by source

### Phase 3: Evaluate (Month 2-3)
- **Question:** Is manual outreach working?
- **If YES:** Continue, consider Expandi for scale
- **If NO:** Re-evaluate channel entirely

### Phase 4: Expandi (If Validated)
- **Cost:** ~$99/month
- **Action:** Automate follow-up sequences
- **Goal:** Scale without adding headcount

---

## 8. KEY RISKS (The Skeptic's List)

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Lead data goes stale | HIGH | Re-extract monthly |
| Sales team overwhelmed | MEDIUM | Prioritize quality over quantity |
| Salesforce manual upload friction | MEDIUM | Batch uploads weekly |
| No replies = no pipeline | HIGH | A/B test messaging |
| GDPR compliance | LOW | Consult legal |
| Tool doesn't integrate | MEDIUM | Use CSV as bridge |

---

## 9. NEXT STEPS

### This Week
- [ ] **Marcus:** Sign up for PhantomBuster trial
- [ ] **Marcus:** Define first extraction queries (Stress workshop ICP)
- [ ] **Sales Manager:** Prepare outreach template
- [ ] **Atlas:** Research GDPR implications

### Next 2 Weeks
- [ ] Extract first batch of 500 leads
- [ ] Clean and deduplicate data
- [ ] Upload to Salesforce
- [ ] Begin outreach campaign
- [ ] Track metrics

### Month End Review
- [ ] Review conversion rates
- [ ] Team retrospective
- [ ] Decide on Phase 2 (Expandi?)

---

## 10. ATLAS'S FINAL VERDICT

> "PhantomBuster is the right tool to START because:
> 1. It's cheap ($49/mo vs $99/mo)
> 2. It gives us DATA ownership (not trapped in another platform)
> 3. We can validate the funnel before automating
> 
> But we must:
> - Track EVERYTHING
> - Kill it fast if it doesn't work
> - Not fall in love with the tool
> - Have a real human review every lead before outreach"

---

*Document prepared by Jarvis (CEO)*  
*Team: Eleanor, Marcus, Quinn, Sales Manager, Atlas (Skeptic)*  
*Date: February 22, 2026*
