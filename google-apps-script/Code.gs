// Google Apps Script for OpenClaw → Google Sheets Integration
// Deploy this in Google Apps Script (script.google.com)

const SHEET_ID = 'YOUR_SHEET_ID_HERE'; // Replace with your Google Sheet ID
const API_SECRET = 'YOUR_SECRET_KEY_HERE'; // Replace with a secret key for security

function doPost(e) {
  try {
    // Parse the incoming data
    const data = JSON.parse(e.postData.contents);
    
    // Verify secret key (basic security)
    if (data.secret !== API_SECRET) {
      return ContentService.createTextOutput(JSON.stringify({
        'status': 'error',
        'message': 'Invalid secret key'
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // Get the spreadsheet
    const ss = SpreadsheetApp.openById(SHEET_ID);
    
    // Handle different operations
    switch(data.operation) {
      case 'createSheet':
        return createNewSheet(ss, data);
      case 'appendData':
        return appendDataToSheet(ss, data);
      case 'clearAndWrite':
        return clearAndWriteData(ss, data);
      case 'updateCell':
        return updateCell(ss, data);
      default:
        return ContentService.createTextOutput(JSON.stringify({
          'status': 'error',
          'message': 'Unknown operation: ' + data.operation
        })).setMimeType(ContentService.MimeType.JSON);
    }
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'error',
      'message': error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function createNewSheet(ss, data) {
  const sheetName = data.sheetName || 'New Sheet';
  const headers = data.headers || [];
  
  // Create new sheet or get existing
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  } else {
    sheet.clear();
  }
  
  // Write headers
  if (headers.length > 0) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length)
      .setFontWeight('bold')
      .setBackground('#1F4E78')
      .setFontColor('#FFFFFF');
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    'status': 'success',
    'message': 'Sheet created: ' + sheetName,
    'sheetName': sheetName
  })).setMimeType(ContentService.MimeType.JSON);
}

function appendDataToSheet(ss, data) {
  const sheetName = data.sheetName || 'Sheet1';
  const rows = data.rows || [];
  
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'error',
      'message': 'Sheet not found: ' + sheetName
    })).setMimeType(ContentService.MimeType.JSON);
  }
  
  // Find next empty row
  const lastRow = sheet.getLastRow();
  const startRow = lastRow + 1;
  
  // Append data
  if (rows.length > 0) {
    sheet.getRange(startRow, 1, rows.length, rows[0].length).setValues(rows);
    
    // Format currency columns if specified
    if (data.currencyColumns) {
      data.currencyColumns.forEach(colIndex => {
        sheet.getRange(startRow, colIndex + 1, rows.length, 1)
          .setNumberFormat('$#,##0');
      });
    }
    
    // Color negative values red, positive green if specified
    if (data.colorCodeProfit && rows.length > 0) {
      const profitCol = data.profitColumn || rows[0].length - 1;
      rows.forEach((row, idx) => {
        const value = row[profitCol];
        if (typeof value === 'number') {
          const cell = sheet.getRange(startRow + idx, profitCol + 1);
          if (value < 0) {
            cell.setFontColor('#FF0000').setFontWeight('bold');
          } else if (value > 0) {
            cell.setFontColor('#008000').setFontWeight('bold');
          }
        }
      });
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    'status': 'success',
    'message': 'Data appended: ' + rows.length + ' rows',
    'rowsAdded': rows.length
  })).setMimeType(ContentService.MimeType.JSON);
}

function clearAndWriteData(ss, data) {
  const sheetName = data.sheetName || 'Sheet1';
  const headers = data.headers || [];
  const rows = data.rows || [];
  
  // Get or create sheet
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  
  // Clear existing content
  sheet.clear();
  
  // Write headers
  if (headers.length > 0) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length)
      .setFontWeight('bold')
      .setBackground('#1F4E78')
      .setFontColor('#FFFFFF');
  }
  
  // Write data
  if (rows.length > 0) {
    sheet.getRange(2, 1, rows.length, rows[0].length).setValues(rows);
    
    // Format currency columns
    if (data.currencyColumns) {
      data.currencyColumns.forEach(colIndex => {
        sheet.getRange(2, colIndex + 1, rows.length, 1)
          .setNumberFormat('$#,##0');
      });
    }
    
    // Color code profits
    if (data.colorCodeProfit) {
      const profitCol = data.profitColumn || rows[0].length - 1;
      rows.forEach((row, idx) => {
        const value = row[profitCol];
        if (typeof value === 'number') {
          const cell = sheet.getRange(2 + idx, profitCol + 1);
          if (value < 0) {
            cell.setFontColor('#FF0000').setFontWeight('bold');
          } else if (value > 0) {
            cell.setFontColor('#008000').setFontWeight('bold');
          }
        }
      });
    }
    
    // Auto-resize columns
    sheet.autoResizeColumns(1, headers.length || rows[0].length);
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    'status': 'success',
    'message': 'Sheet cleared and data written: ' + rows.length + ' rows',
    'rowsWritten': rows.length
  })).setMimeType(ContentService.MimeType.JSON);
}

function updateCell(ss, data) {
  const sheetName = data.sheetName || 'Sheet1';
  const row = data.row;
  const col = data.col;
  const value = data.value;
  
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'error',
      'message': 'Sheet not found: ' + sheetName
    })).setMimeType(ContentService.MimeType.JSON);
  }
  
  sheet.getRange(row, col).setValue(value);
  
  return ContentService.createTextOutput(JSON.stringify({
    'status': 'success',
    'message': 'Cell updated: ' + row + ',' + col
  })).setMimeType(ContentService.MimeType.JSON);
}

// Test function (run this to test the script)
function testScript() {
  const testData = {
    'secret': API_SECRET,
    'operation': 'clearAndWrite',
    'sheetName': 'Test Sheet',
    'headers': ['Category', 'Annual Cost', 'Monthly Cost'],
    'rows': [
      ['Franchise Fee', 297000, 24750],
      ['Salaries', 144000, 12000]
    ],
    'currencyColumns': [1, 2]
  };
  
  const mockEvent = {
    'postData': {
      'contents': JSON.stringify(testData)
    }
  };
  
  const result = doPost(mockEvent);
  Logger.log(result);
}
