const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    const page = await context.newPage();
    
    try {
        console.log("Navigating to Gmail...");
        await page.goto('https://gmail.com');
        await page.waitForLoadState('networkidle');
        
        console.log("Entering email...");
        await page.fill('input[type="email"]', "alex.chen.dc.gta@gmail.com");
        await page.click('#identifierNext');
        await page.waitForTimeout(2000);
        
        console.log("Entering password...");
        await page.fill('input[type="password"]', "yfwsmwhaleuujesq");
        await page.click('#passwordNext');
        await page.waitForTimeout(5000);
        
        console.log("Waiting for Gmail to load...");
        await page.waitForSelector('div[role="button"][gh="cm"]', { timeout: 15000 });
        
        console.log("Clicking Compose...");
        await page.click('div[role="button"][gh="cm"]');
        await page.waitForTimeout(2000);
        
        console.log("Filling email details...");
        await page.fill('input[role="combobox"][aria-label="To recipients"]', "ttr11@gmail.com");
        await page.fill('input[aria-label="Subject"]', "Test from Alex Chen via Browser");
        await page.fill('div[aria-label="Message Body"]', "Hi Troy, This email was sent using browser automation! Alex Chen is now able to send emails through the Gmail web interface. Let me know if you received this. Best regards, Alex Chen");
        
        await page.waitForTimeout(1000);
        
        console.log("Sending...");
        await page.click('div[role="button"][aria-label*="Send"]');
        await page.waitForTimeout(3000);
        
        console.log(JSON.stringify({
            "status": "success",
            "from": "alex.chen.dc.gta@gmail.com",
            "to": "ttr11@gmail.com",
            "subject": "Test from Alex Chen via Browser",
            "sent_at": "2026-03-01T15:22:42.666167"
        }));
        
    } catch (error) {
        console.log(JSON.stringify({
            "status": "error",
            "error": error.message
        }));
    } finally {
        await browser.close();
    }
})();
