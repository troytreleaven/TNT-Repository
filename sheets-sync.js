// Google Sheets Sync for Pipeline
// Configuration - Replace with your values
const SHEETS_CONFIG = {
    // Your Google Sheet ID (from the URL)
    // https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
    SHEET_ID: 'YOUR_SHEET_ID_HERE',
    
    // Your API Key from Google Cloud Console
    API_KEY: 'YOUR_API_KEY_HERE',
    
    // Sheet name (tab name at bottom of spreadsheet)
    SHEET_NAME: 'Pipeline'
};

// Pipeline data structure
class PipelineSync {
    constructor() {
        this.baseUrl = 'https://sheets.googleapis.com/v4/spreadsheets';
        this.deals = this.loadDealsFromStorage();
    }
    
    // Load deals from localStorage (your current pipeline)
    loadDealsFromStorage() {
        const saved = localStorage.getItem('pipeline-deals');
        return saved ? JSON.parse(saved) : this.getDefaultDeals();
    }
    
    // Default deals (your current pipeline)
    getDefaultDeals() {
        return [
            { company: 'Mazak', contact: 'Eric', value: 5800, probability: 100, stage: 'Closed Won', notes: 'Hutton - Toronto' },
            { company: 'Berq RNG', contact: 'Nabil', value: 6500, probability: 100, stage: 'Closed Won', notes: 'Lasse Larving referral' },
            { company: 'Algoma', contact: 'Heather', value: 31000, probability: 100, stage: 'Closed Won', notes: 'March 18-20 Boot Camp' },
            { company: 'Cambridge', contact: 'Tim', value: 11500, probability: 100, stage: 'Closed Won', notes: 'Boot Camp' },
            { company: 'TJN', contact: 'Francois', value: 16000, probability: 100, stage: 'Closed Won', notes: '3 seats' },
            { company: 'PureLogic', contact: 'Raj', value: 7500, probability: 100, stage: 'Closed Won', notes: '2 seats' },
            { company: 'Axium Group', contact: 'Rick', value: 6000, probability: 50, stage: 'In Progress', notes: 'Meeting Wed 18th' },
            { company: 'Hutton - DC', contact: 'Andrea', value: 39000, probability: 75, stage: 'In Progress', notes: 'Boot Camp March 3-5' },
            { company: 'Jeff/Rob Huten', contact: 'Various', value: 1600, probability: 75, stage: 'In Progress', notes: '3-week program' }
        ];
    }
    
    // Save deals to localStorage
    saveDeals() {
        localStorage.setItem('pipeline-deals', JSON.stringify(this.deals));
    }
    
    // Read data FROM Google Sheets
    async readFromSheets() {
        try {
            const url = `${this.baseUrl}/${SHEETS_CONFIG.SHEET_ID}/values/${SHEETS_CONFIG.SHEET_NAME}!A2:F100?key=${SHEETS_CONFIG.API_KEY}`;
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.values) {
                // Convert sheet data to deal objects
                this.deals = data.values.map((row, index) => ({
                    id: index + 1,
                    company: row[0] || '',
                    contact: row[1] || '',
                    value: parseFloat(row[2]) || 0,
                    probability: parseInt(row[3]) || 0,
                    stage: row[4] || '0-25%',
                    notes: row[5] || ''
                }));
                
                this.saveDeals();
                return { success: true, message: `Loaded ${this.deals.length} deals from Sheets` };
            }
            
            return { success: true, message: 'No data found in sheet', deals: [] };
        } catch (error) {
            console.error('Read error:', error);
            return { success: false, message: 'Error reading from Sheets: ' + error.message };
        }
    }
    
    // Save data TO Google Sheets (requires OAuth for writing)
    async saveToSheets() {
        // For now, we'll create a CSV download as a workaround
        // Full write requires OAuth setup (see instructions below)
        
        const csv = this.convertToCSV();
        this.downloadCSV(csv, 'pipeline-export.csv');
        
        return { 
            success: true, 
            message: 'Pipeline exported to CSV. For full sync, see OAuth setup instructions.' 
        };
    }
    
    // Convert deals to CSV
    convertToCSV() {
        const headers = ['Company', 'Contact', 'Value', 'Probability', 'Stage', 'Notes'];
        const rows = this.deals.map(d => [
            d.company,
            d.contact,
            d.value,
            d.probability,
            d.stage,
            d.notes
        ]);
        
        return [headers, ...rows]
            .map(row => row.map(cell => `"${cell}"`).join(','))
            .join('\n');
    }
    
    // Download CSV file
    downloadCSV(csv, filename) {
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
    
    // Add new deal
    addDeal(deal) {
        deal.id = this.deals.length + 1;
        this.deals.push(deal);
        this.saveDeals();
    }
    
    // Update deal
    updateDeal(id, updates) {
        const index = this.deals.findIndex(d => d.id === id);
        if (index !== -1) {
            this.deals[index] = { ...this.deals[index], ...updates };
            this.saveDeals();
        }
    }
    
    // Get total pipeline value
    getTotalValue() {
        return this.deals.reduce((sum, d) => sum + d.value, 0);
    }
    
    // Get weighted forecast
    getWeightedForecast() {
        return this.deals.reduce((sum, d) => sum + (d.value * d.probability / 100), 0);
    }
}

// Initialize sync manager
const pipelineSync = new PipelineSync();

// UI Functions
function showSyncStatus(message, isError = false) {
    const statusDiv = document.getElementById('sync-status');
    if (statusDiv) {
        statusDiv.textContent = message;
        statusDiv.className = isError ? 'sync-status error' : 'sync-status success';
        statusDiv.style.display = 'block';
        setTimeout(() => { statusDiv.style.display = 'none'; }, 3000);
    }
}

async function syncFromSheets() {
    showSyncStatus('📥 Loading from Sheets...');
    const result = await pipelineSync.readFromSheets();
    showSyncStatus(result.message, !result.success);
    if (result.success) {
        renderPipeline(); // Refresh the display
    }
}

async function syncToSheets() {
    showSyncStatus('📤 Exporting to CSV...');
    const result = await pipelineSync.saveToSheets();
    showSyncStatus(result.message, !result.success);
}

// For full bidirectional sync, you'll need OAuth
// See: sheets-oauth-setup.md for instructions
