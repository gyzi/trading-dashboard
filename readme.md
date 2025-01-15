# Trading212 Stock Exporter and Dynamic Graph Visualizer

This project exports stock data from Trading212 and creates a dynamic graph visualization using Streamlit.

## Features
- Exports Trading212 open postions data to CSV
- Creates interactive, real-time stock visualizations using Streamlit
- Dynamically updates graph based on user input

## Installation
1. Clone the repository
    Install required packages:
2. Set up your Trading212 API key as an environment variable

```bash
pip install -r requirements.txt
export TRADING212_API_KEY='your_api_key'

# export open position from trading212 to csv
python trading212.py

# Then run streamlit to show interactive visualizations for csv data
streamlit run dashborad.py
```

