from openpyxl import Workbook
from tinydb import TinyDB



db = TinyDB('fishing_reports.json')
all_data = db.all()

headers = [key for key in all_data[0].keys()]

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Write the headers to the first row
ws.append(headers)

# Write data rows
for entry in all_data:
    # Convert each entry to a list of values, handling None values
    row = [entry.get(header) for header in headers]
    ws.append(row)

# Save the workbook to a file
wb.save("fishing_reports.xlsx")
print("Excel file created successfully: fishing_reports.xlsx")