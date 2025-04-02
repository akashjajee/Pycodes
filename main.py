import gspread
from oauth2client.service_account import ServiceAccountCredentials
from Autoemail import *

# Google Sheets API authorization
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('Auth_key.json', scope)
client = gspread.authorize(creds)

# Fetch data from the spreadsheet
spreadsheet = client.open('Customer Issues')
worksheet = spreadsheet.get_worksheet(0)
data = worksheet.get_all_records()

# Use a standard dictionary
customer_counts = {}

for entry in data:
    customer = entry['Email ID']

    # Initialize dictionary for the customer if not already present
    if customer not in customer_counts:
        customer_counts[customer] = {'Total': 0, 'Pending': 0, 'Resolved': 0}

    # Update counts
    customer_counts[customer]['Total'] += 1
    if entry['Resolved'] == '':
        customer_counts[customer]['Pending'] += 1
    else:
        customer_counts[customer]['Resolved'] += 1

# Send emails and print the customer issue summary
for customer, counts in customer_counts.items():
    SendMail(customer, counts['Total'], counts['Pending'], counts['Resolved'])

    print(f"Customer: {customer}")
    print(f"  Total Issues: {counts['Total']}")
    print(f"  Pending Issues: {counts['Pending']}")
    print(f"  Resolved Issues: {counts['Resolved']}")
