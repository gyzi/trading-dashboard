import requests
import os
import json
import csv
from datetime import datetime

url = "https://demo.trading212.com/api/v0/history/exports"

payload = {
  "dataIncluded": {
    "includeDividends": True,
    "includeInterest": True,
    "includeOrders": True,
    "includeTransactions": True
  },
  "timeFrom": "2024-01-24T14:15:22Z",
  "timeTo": datetime.now().isoformat() + "Z"
}

headers = {
  "Content-Type": "application/json",
  "Authorization": os.environ.get('TRADING212_API_KEY')
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))

    # Save to CSV
    with open('stocks.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers
        if data:
            writer.writerow(data[0].keys())
        
        # Write data rows
        for row in data:
            writer.writerow(row.values())
    
    print("Data saved to stocks.csv")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
