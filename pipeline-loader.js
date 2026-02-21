/**
 * pipeline-loader.js
 * Fetches Troy's 2026 Pipeline from Google Sheets (published CSV)
 * and exposes window.PipelineData for any dashboard page to consume.
 *
 * ─── SETUP (one-time, 2 minutes) ────────────────────────────────────────────
 * 1. Open your Google Sheet:
 *    https://docs.google.com/spreadsheets/d/1Ih4QU2hPCJyZ43fwkJKsVKU95xtc-fD9/edit
 * 2. File → Share → Publish to web
 * 3. Under "Link", choose the tab: "Troys 2026 Pipeline"
 * 4. Change format dropdown to "Comma-separated values (.csv)"
 * 5. Click "Publish" → copy the URL
 * 6. Paste it as SHEET_CSV_URL below
 * ────────────────────────────────────────────────────────────────────────────
 */

const SHEET_CSV_URL = 'YOUR_PUBLISHED_CSV_URL_HERE';
// Example: 'https://docs.google.com/spreadsheets/d/1Ih4QU2.../pub?gid=0&single=true&output=csv'

// ─── CSV Parser ───────────────────────────────────────────────────────────────
function parseCSV(text) {
  const lines = text.split(/\r?\n/);
  return lines.map(line => {
    const cols = [];
    let cur = '', inQuote = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (inQuote && line[i + 1] === '"') { cur += '"'; i++; }
        else inQuote = !inQuote;
      } else if (ch === ',' && !inQuote) {
        cols.push(cur.trim()); cur = '';
      } else cur += ch;
    }
    cols.push(cur.trim());
    return cols;
  });
}

function $$(str) {
  if (!str) return 0;
  const n = parseFloat(str.replace(/[$ ,CAD\s]/g, '').replace('CA', ''));
  return isNaN(n) ? 0 : Math.abs(n);
}

function pct(str) {
  if (!str) return null;
  const n = parseFloat(str.replace('%', ''));
  return isNaN(n) ? null : n;
}

// ─── Sheet Parser ─────────────────────────────────────────────────────────────
function parseSheet(rows) {
  // Col map (0-indexed): 1=Name, 2=Notes, 3=Payment, 5=LeadSource, 6=Product,
  // 7=ProjectedSale, 8=Probability, 9=NetForecast, 10=NextStep,
  // 11=Sep,12=Oct,13=Nov,14=Dec,15=Jan,16=Feb,17=Mar,18=Apr,19=May,20=Jun,21=Jul,22=Aug
  const MONTHS = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'];
  const MCOLS  = [11,12,13,14,15,16,17,18,19,20,21,22];

  const warmPipeline = [], hotOpps = [], collected = [];
  let section = 'warm';

  for (const row of rows) {
    const name = row[1] || '';
    const lower = name.toLowerCase();

    // Section switches
    if (lower === 'hot opportunity') { section = 'hot'; continue; }
    if (lower === 'collected')       { section = 'collected'; continue; }

    // Skip headers / totals / empty
    if (!name) continue;
    if (['subtotals','total net forecast','budget goal','surplus/shortfall',
         'total unclosed pipeline','warm opportunity','opportunity\nname',
         'opportunity name'].some(s => lower.includes(s))) continue;

    const projSale   = $$(row[7]);
    const probability = pct(row[8]);
    const netForecast = $$(row[9]);

    if (projSale === 0 && netForecast === 0) continue;

    const monthly = {};
    MCOLS.forEach((col, i) => {
      const v = $$(row[col]);
      if (v > 0) monthly[MONTHS[i]] = v;
    });

    const entry = {
      date: row[0] || '',
      name,
      notes:       row[2] || '',
      leadSource:  row[5] || '',
      product:     row[6] || '',
      projectedSale: projSale,
      probability,
      netForecast,
      nextStep:    row[10] || '',
      monthly,
    };

    if (section === 'hot')       hotOpps.push(entry);
    else if (section === 'collected') collected.push(entry);
    else warmPipeline.push(entry);
  }

  // ── Totals ──
  const totalPipeline  = [...warmPipeline, ...hotOpps].reduce((s, d) => s + d.projectedSale, 0);
  const weightedForecast = [...warmPipeline, ...hotOpps].reduce((s, d) => {
    return s + (d.probability != null ? d.projectedSale * d.probability / 100 : 0);
  }, 0);
  const collectedYTD = collected.reduce((s, d) => s + d.projectedSale, 0);

  // ── Monthly forecast rollup ──
  const monthlyForecast = {};
  const MONTHS_ALL = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'];
  MONTHS_ALL.forEach(m => { monthlyForecast[m] = 0; });
  [...warmPipeline, ...hotOpps, ...collected].forEach(d => {
    Object.entries(d.monthly).forEach(([m, v]) => {
      monthlyForecast[m] = (monthlyForecast[m] || 0) + v;
    });
  });

  // ── This month (Feb) highlight ──
  const thisMonth = monthlyForecast['Feb'] || 0;

  return {
    warmPipeline,
    hotOpps,
    collected,
    totals: {
      totalPipeline,
      weightedForecast,
      collectedYTD,
      thisMonth,
      budgetGoal: 600000,
      hotCount: hotOpps.filter(d => (d.probability || 0) >= 75).length,
    },
    monthlyForecast,
    lastUpdated: new Date().toLocaleTimeString(),
  };
}

// ─── Fetch & Expose ──────────────────────────────────────────────────────────
window.PipelineData = null;
window.PipelineLoadCallbacks = [];

window.onPipelineLoaded = function(cb) {
  if (window.PipelineData) { cb(window.PipelineData); return; }
  window.PipelineLoadCallbacks.push(cb);
};

async function loadPipeline() {
  try {
    // If no URL set yet, use embedded fallback data
    if (!SHEET_CSV_URL || SHEET_CSV_URL.includes('YOUR_PUBLISHED')) {
      console.warn('pipeline-loader: No sheet URL set. Using embedded snapshot data.');
      window.PipelineData = getSnapshotData();
      window.PipelineLoadCallbacks.forEach(cb => cb(window.PipelineData));
      return;
    }

    const resp = await fetch(SHEET_CSV_URL);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const text = await resp.text();
    const rows = parseCSV(text);
    window.PipelineData = parseSheet(rows);
    window.PipelineData.source = 'live';
    console.log('✅ Pipeline loaded from Google Sheets:', window.PipelineData.totals);
  } catch (err) {
    console.error('pipeline-loader: fetch failed, using snapshot.', err);
    window.PipelineData = getSnapshotData();
    window.PipelineData.source = 'snapshot';
  }
  window.PipelineLoadCallbacks.forEach(cb => cb(window.PipelineData));
}

// ─── Snapshot (real data from your CSV, Feb 2026) ────────────────────────────
function getSnapshotData() {
  const warmPipeline = [
    { name: 'RHI Magnesita',                    probability: 25,  projectedSale: 40000, netForecast: 10000, nextStep: 'Mid-March check in', notes: 'Project likely in the states', monthly: { Apr: 11250 } },
    { name: 'Automotive Group',                 probability: 0,   projectedSale: 20000, netForecast: 0,     nextStep: 'Present end of Jan', notes: 'Tirecraft + Alan Beech Group', monthly: {} },
    { name: 'CMTO',                             probability: 25,  projectedSale: 40000, netForecast: 10000, nextStep: 'Confirm first week of Jan', notes: 'Coaching project', monthly: { Apr: 20000 } },
    { name: 'BCM Insurance',                    probability: 50,  projectedSale: 40000, netForecast: 20000, nextStep: 'Waiting for Job Grant', notes: 'Committed, pending grant', monthly: { Apr: 40000 } },
    { name: 'Michipoten First Nation',          probability: 50,  projectedSale: 35000, netForecast: 17500, nextStep: 'Follow-up mid Feb', notes: 'Build into 26/27 budget', monthly: { Apr: 20000 } },
    { name: 'Toronto Jewish Network (women)',   probability: 50,  projectedSale: 27000, netForecast: 13500, nextStep: 'Finish men → suggest Feb/Mar', notes: 'After men\'s class', monthly: { Mar: 27000 } },
    { name: 'SBI (Indian Bank)',                probability: 25,  projectedSale: 22500, netForecast: 5625,  nextStep: 'Confirm first week of Jan', notes: 'Up to $50K', monthly: { Mar: 11250 } },
    { name: 'MTE Coaching/Microlearnings',      probability: 25,  projectedSale: 20000, netForecast: 5000,  nextStep: 'Discuss first week of Jan', notes: 'Microlearning discussion', monthly: { Apr: 20000 } },
    { name: 'Berq RNG',                         probability: 75,  projectedSale: 17400, netForecast: 13050, nextStep: 'Check in with Bas', notes: 'LWI 6 employees or private', monthly: { May: 3800 } },
    { name: 'Earth Fresh Foods',                probability: 25,  projectedSale: 14500, netForecast: 3625,  nextStep: 'Check in beg. January', notes: 'Team for Burlington Boot Camp', monthly: { Mar: 14500 } },
    { name: 'JFE Shoji',                        probability: 0,   projectedSale: 14500, netForecast: 0,     nextStep: 'Discuss first week of Jan', notes: 'Team for Burlington Boot Camp', monthly: { Mar: 14500 } },
    { name: 'Meridian Credit Union',            probability: null,projectedSale: 17500, netForecast: 0,     nextStep: 'Check in June', notes: 'Quincy - group of 7 for Niagara Sep', monthly: {} },
    { name: 'Performance Acura',                probability: 0,   projectedSale: 3000,  netForecast: 0,     nextStep: '', notes: 'Conflict workshop', monthly: {} },
    { name: 'Global Help Foundation (GHF)',     probability: 0,   projectedSale: 10000, netForecast: 0,     nextStep: '', notes: '2 Day Workshop in May - Toronto', monthly: {} },
    { name: 'Algoma Central Refresher (Tina)',  probability: 25,  projectedSale: 20000, netForecast: 5000,  nextStep: 'Tina inquiring about Refresher', notes: '', monthly: { Feb: 5000 } },
    { name: 'BMO Capital Markets',              probability: 0,   projectedSale: 40000, netForecast: 0,     nextStep: 'Sent email to connect', notes: 'Jen Harrop referral', monthly: {} },
    { name: 'Thorpe Handcrafted Carpentry',     probability: 25,  projectedSale: 17400, netForecast: 4350,  nextStep: 'Discuss proposal with her husband', notes: 'LWI 6 employees', monthly: {} },
    { name: 'Ron - Jenna\'s Dad',              probability: 25,  projectedSale: 2500,  netForecast: 625,   nextStep: 'Send dates', notes: 'Boot Camp or Dale', monthly: { Mar: 2500 } },
    { name: 'Meridian CU (Erin Pickering)',     probability: 75,  projectedSale: 4990,  netForecast: 3743,  nextStep: 'Waiting for budget confirmation', notes: '2 for DCC Niagara Sep', monthly: {} },
    { name: 'WalterFedy',                       probability: 25,  projectedSale: 17500, netForecast: 4375,  nextStep: 'Sent info, getting clear on budget', notes: 'Community group 6-10', monthly: { Mar: 5000 } },
    { name: 'TireCraft Regional Support',       probability: 0,   projectedSale: 15000, netForecast: 0,     nextStep: 'Check back with Usman', notes: '', monthly: {} },
    { name: 'RWDI - Kerry Smith',               probability: 0,   projectedSale: 10000, netForecast: 0,     nextStep: '', notes: '', monthly: { May: 2500 } },
    { name: 'Axium Group - David Honicky',      probability: 25,  projectedSale: 6500,  netForecast: 1625,  nextStep: 'Meeting booked Wed 18th', notes: 'Fern Resort / Camp Axsium', monthly: { Aug: 6500 } },
    { name: 'Grand River Foods',                probability: 25,  projectedSale: 2900,  netForecast: 725,   nextStep: 'Check in', notes: 'Sandeep - leadership training', monthly: { Dec: 800 } },
    { name: 'Napa Conference',                  probability: 0,   projectedSale: 5000,  netForecast: 0,     nextStep: 'Invite in October', notes: 'October conference', monthly: { Jul: 5000 } },
    { name: 'Scott Eccles',                     probability: null,projectedSale: 2500,  netForecast: 0,     nextStep: 'Talking Monday', notes: '', monthly: { Mar: 2500 } },
    { name: 'La Boîte à Soleil',               probability: null,projectedSale: 2900,  netForecast: 0,     nextStep: 'Meeting booked 2/6', notes: 'LWI details', monthly: {} },
    { name: 'Kevin Lebruyn',                    probability: 0,   projectedSale: 2900,  netForecast: 0,     nextStep: '', notes: '1 LWI possible', monthly: {} },
  ];

  const hotOpps = [
    { name: 'Mazak Corporation',           probability: 75,  projectedSale: 5800,  netForecast: 4350,  nextStep: '', notes: '2 for KW LWI', monthly: { Feb: 5800 } },
    { name: 'Berq RNG Coaching + Boot Camp', probability: 75, projectedSale: 6559, netForecast: 4919,  nextStep: 'Book meeting w/ Andy, Bob, Tyson', notes: 'Michael Dowdy coaching', monthly: { Feb: 6559 } },
    { name: 'Angstrom Engineering',        probability: null,projectedSale: 0,     netForecast: 0,     nextStep: 'Next Kitchener DCC', notes: '2 for DCC - bus issue', monthly: {} },
    { name: 'Jeff & Rob Huten LWI Upgrade',probability: 100, projectedSale: 1600,  netForecast: 1600,  nextStep: 'Kevin to do upgrade', notes: 'Registered', monthly: { Feb: 1600 } },
    { name: 'Makaxo Traffic Management',   probability: 100, projectedSale: 2900,  netForecast: 2900,  nextStep: 'Waiting for payment', notes: 'Burlington LWI', monthly: { Mar: 2900 } },
  ];

  const collected = [
    { name: 'Cambridge Elevating',         probability: 100, projectedSale: 11475, netForecast: 11475, notes: 'KW class', monthly: { Jan: 11475 } },
    { name: 'Andy Xiao MTE',               probability: 100, projectedSale: 2900,  netForecast: 2900,  notes: 'Mississauga Boot Camp', monthly: { Jan: 2900 } },
    { name: 'Kevin Heeringa All-Pro',      probability: 100, projectedSale: 2500,  netForecast: 2500,  notes: 'KKW Class', monthly: { Jan: 2500 } },
    { name: 'Toronto Jewish Network',      probability: 100, projectedSale: 16000, netForecast: 16000, notes: 'Remainder + payment', monthly: { Jan: 16000 } },
    { name: 'Jackie - Eclipse Automation', probability: 100, projectedSale: 2500,  netForecast: 2500,  notes: 'HIP', monthly: { Jan: 2500 } },
    { name: 'PureLogic/PureLogic IT',      probability: 100, projectedSale: 7500,  netForecast: 7500,  notes: 'WWRS', monthly: { Jan: 7500 } },
    { name: 'Pure Logic (2 more)',         probability: 100, projectedSale: 5000,  netForecast: 5000,  notes: '2 more for Sales Course', monthly: { Jan: 5000 } },
    { name: 'Natalie Black',               probability: 100, projectedSale: 2295,  netForecast: 2295,  notes: 'KW class', monthly: {} },
    { name: 'Algoma Central LTM',          probability: 100, projectedSale: 31000, netForecast: 31000, notes: 'Runs end of February', monthly: { Feb: 31000 } },
    { name: 'Hutton and Company',          probability: 75,  projectedSale: 39000, netForecast: 29250, notes: 'Project confirmed', monthly: { Feb: 32000, Jun: 4500 } },
    { name: 'Owen Lee',                    probability: 100, projectedSale: 2500,  netForecast: 2500,  notes: 'Hamilton Dale', monthly: { Feb: 2500 } },
    { name: 'North American Stamping',     probability: null,projectedSale: 2900,  netForecast: 0,     notes: 'LB-KW', monthly: { Feb: 2900 } },
  ];

  const totalPipeline    = [...warmPipeline, ...hotOpps].reduce((s, d) => s + d.projectedSale, 0);
  const weightedForecast = [...warmPipeline, ...hotOpps].reduce((s, d) => s + (d.probability != null ? d.projectedSale * d.probability / 100 : 0), 0);
  const collectedYTD     = collected.reduce((s, d) => s + d.projectedSale, 0);
  const MONTHS_ALL = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'];
  const monthlyForecast = {};
  MONTHS_ALL.forEach(m => { monthlyForecast[m] = 0; });
  [...warmPipeline, ...hotOpps, ...collected].forEach(d => {
    Object.entries(d.monthly).forEach(([m, v]) => { monthlyForecast[m] = (monthlyForecast[m] || 0) + v; });
  });

  return {
    warmPipeline, hotOpps, collected,
    totals: {
      totalPipeline,
      weightedForecast,
      collectedYTD,
      thisMonth: monthlyForecast['Feb'] || 0,
      budgetGoal: 600000,
      hotCount: hotOpps.filter(d => (d.probability || 0) >= 75).length,
    },
    monthlyForecast,
    source: 'snapshot',
    lastUpdated: 'Feb 21, 2026 (snapshot)',
  };
}

// Auto-load on script include
loadPipeline();
