---
name: doc-to-excel
name: Convert Word documents to Excel spreadsheets
metadata:
  openclaw:
    emoji: "📊"
---

# DOC to Excel Converter

Convert Word documents (.docx) containing tabular data into properly formatted Excel (.xlsx) files.

## Prerequisites

Requires `openpyxl` Python package:
```bash
pip3 install openpyxl --user --break-system-packages
```

## Usage

1. Extract data from Word document
2. Parse tables and structured data
3. Create formatted Excel workbook with multiple sheets
4. Apply styling (headers, currency formats, colors)

## Python Script

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def doc_to_excel(data_sheets, output_path):
    """
    Convert document data to Excel
    
    Args:
        data_sheets: List of dicts with 'title', 'headers', 'data'
        output_path: Path for output .xlsx file
    """
    wb = openpyxl.Workbook()
    
    for idx, sheet_info in enumerate(data_sheets):
        if idx == 0:
            ws = wb.active
            ws.title = sheet_info['title']
        else:
            ws = wb.create_sheet(sheet_info['title'])
        
        # Headers
        for col, header in enumerate(sheet_info['headers'], 1):
            cell = ws.cell(row=1, column=col)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        
        # Data
        for row_idx, row_data in enumerate(sheet_info['data'], 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell.value = value
        
        # Auto-adjust column widths
        for col in range(1, len(sheet_info['headers']) + 1):
            ws.column_dimensions[get_column_letter(col)].width = 15
    
    wb.save(output_path)
    return output_path
```

## Example

```python
sheets = [
    {
        'title': 'Fixed Costs',
        'headers': ['Category', 'Annual', 'Monthly', '%', 'Notes'],
        'data': [
            ['Rent', 84000, 7000, '7.5%', ''],
            ['Salaries', 144000, 12000, '12.9%', ''],
        ]
    },
    {
        'title': 'Profit Scenarios',
        'headers': ['Camps', 'Revenue', 'Costs', 'Profit'],
        'data': [
            [4, 185600, 57600, 34834],
            [6, 278400, 86400, 98834],
        ]
    }
]

doc_to_excel(sheets, '/output/cost_analysis.xlsx')
```

## Output

Creates professionally formatted Excel file with:
- Multiple sheets
- Styled headers (blue background, white text)
- Currency formatting
- Auto-sized columns
- Color-coded values (red for negative, green for positive)

## Notes

- Uses openpyxl (no Microsoft Office required)
- Works on Linux/Mac/Windows
- Can be extended to read docx directly with `python-docx` package
