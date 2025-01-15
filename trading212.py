import requests
import json
import csv
import os

def fetch_trading_data():
    url = "https://live.trading212.com/api/v0/equity/portfolio"
    headers = {"Authorization": os.getenv("TRADING212_AUTH_TOKEN")}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_csv(data, filename='trading212_positions.csv'):
    if not data:
        print("No data to save.")
        return
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers
        writer.writerow(data[0].keys())
        
        # Write data rows
        for row in data:
            writer.writerow(row.values())
    
    print(f"Data saved to {filename}")

def main():
    # Fetch data
    data = fetch_trading_data()
    
    if data:
        # Print JSON output
        print("\nAPI Response:")
        print(json.dumps(data, indent=2))
        
        # Save to CSV
        save_to_csv(data)

if __name__ == "__main__":
    main()