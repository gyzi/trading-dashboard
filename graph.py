import requests
import os
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
  "timeFrom": "2019-08-24T14:15:22Z",
  "timeTo": datetime.now().isoformat() + "Z"
}
headers = {
  "Content-Type": "application/json",
  "Authorization": os.environ.get('TRADING212_API_KEY')
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

with open('stocks.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if data:
        writer.writerow(data[0].keys())
    for row in data:
        writer.writerow(row.values())
