import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Trading212 Portfolio Dashboard", page_icon="📈", layout="wide")

def fetch_trading_data(api_key, base_url):
    url = f"{base_url}/api/v0/equity/portfolio"
    headers = {"Authorization": api_key}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def process_data(data):
    if not data:
        st.error("No data to process.")
        return pd.DataFrame()
    df = pd.DataFrame(data)
    df['initialFillDate'] = pd.to_datetime(df['initialFillDate'], utc=True)
    df['totalValue'] = df['quantity'] * df['currentPrice']
    df['totalCost'] = df['quantity'] * df['averagePrice']
    df['profitLoss'] = df['ppl']
    df['cleanTicker'] = df['ticker'].str.replace('_US_EQ', '').str.replace('_EQ', '')
    return df

def fetch_realtime_data(ticker):
    api_key = st.session_state.api_ninja_key  # Get API key from session state
    url = f'https://api.api-ninjas.com/v1/stockprice?ticker={ticker}'
    try:
        response = requests.get(url, headers={'X-Api-Key': api_key})
        if response.status_code == 200:
            data = response.json()
            return {
                'ticker': data.get('ticker', ticker),
                'currentPrice': data.get('price'),
                'name': data.get('name', ticker)
            }
    except:
        pass
    return {'ticker': ticker, 'currentPrice': None, 'name': ticker}

def show_home_page():
    st.title("📊 Trading212 Portfolio Dashboard")
    
    # Centering content using columns
    col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column proportions as needed
    
    with col2:
        st.write("🚀 Welcome to your personal Trading212 portfolio analyzer!")
        st.write("📈 This project provides a comprehensive view of your Trading212 portfolio using their API.")
        st.write("🔗 GitHub Repository: [GitHub Repository](https://github.com/gyzi/trading-dashboard)")
        st.write("🔑 To get started, enter your Trading212 API key in the sidebar and select your environment (Demo or Live).")
        st.write("🔑 Your Trading212 API key can be generate from App Settings > API then generate with permessions Meta data and Portfolio ON")
        st.write("🔑 As of 2nd optional Join API NANJA to get api for realtime stock pricing https://api-ninjas.com/api")
        st.write("💖 If you find this project helpful, consider supporting the developer:")
        
        # Embed YouTube video
        st.video("https://www.youtube.com/watch?v=s2IHQ0XWzBo")

def show_dashboard(df):
    st.title("📊 Trading212 Portfolio Dashboard")
    
    # Add some space below the title
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_value = df['totalValue'].sum()
        st.metric("Portfolio Value", f"${total_value:,.2f}")
        
    with col2:
        total_pl = df['profitLoss'].sum()
        st.metric("Total P/L", f"${total_pl:,.2f}", delta=f"{(total_pl/total_value)*100:.1f}%")
        
    with col3:
        positions_count = len(df)
        st.metric("Open Positions", positions_count)
        
    with col4:
        profitable_positions = len(df[df['profitLoss'] > 0])
        st.metric("Profitable Positions", f"{profitable_positions}/{positions_count}")

    # Use columns for Portfolio Overview and Top Performers
    col_overview, col_analysis = st.columns(2)

    with col_overview:
        fig_treemap = px.treemap(
            df,
            values='totalValue',
            path=['ticker'],
            title="Portfolio Allocation",
            color='profitLoss',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        st.plotly_chart(fig_treemap)

    with col_analysis:
        st.subheader("Top Performers")
        fig_bar = px.bar(
            df.nlargest(10, 'profitLoss'),
            x='ticker',
            y='profitLoss',
            title="Top 10 Positions by P/L",
            color='profitLoss',
            color_continuous_scale=['red', 'green']
        )
        st.plotly_chart(fig_bar)

    # Add space before Position Details table
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Position Details Table
    st.subheader("Position Details")
    
    display_columns = ['ticker', 'name', 'quantity', 'averagePrice', 'currentPrice', 'profitLoss', 'totalValue', 'initialFillDate']
    
    display_df = df[display_columns]
    
    display_df = display_df.style.format({
        'averagePrice': '${:.2f}',
        'currentPrice': '${:.2f}',
        'profitLoss': '${:.2f}',
        'totalValue': '${:.2f}',
        'initialFillDate': lambda x: x.strftime('%Y-%m-%d')
    })
    
    # Displaying the dataframe
    st.dataframe(display_df)

# Sidebar
st.sidebar.header("Trading212 API Key")
api_key = st.sidebar.text_input("Enter your Trading212 API Key:", type="password")
api_ninja_key = st.sidebar.text_input("Enter your API Ninja Key (optional):", type="password")
environment = st.sidebar.radio("Select Trading212 Environment", ("Demo", "Live"))
base_url = "https://demo.trading212.com" if environment == "Demo" else "https://live.trading212.com"

# Button to submit and show dashboard
if st.sidebar.button("Submit"):
    if api_key:
        # Store API Ninja key in session state if provided
        if api_ninja_key:
            st.session_state.api_ninja_key = api_ninja_key
        
        trading_data = fetch_trading_data(api_key, base_url)
        
        if trading_data:
            df = process_data(trading_data)
            
            if not df.empty:
                realtime_data = []
                
                for ticker in df['cleanTicker'].unique():
                    data = fetch_realtime_data(ticker)
                    if data:
                        realtime_data.append(data)

                if realtime_data:
                    realtime_df = pd.DataFrame(realtime_data)
                    df = df.merge(realtime_df, left_on='cleanTicker', right_on='ticker', how='left', suffixes=('', '_realtime'))
                    df['currentPrice'] = df['currentPrice_realtime'].fillna(df['currentPrice'])
                    
                    # Use stock name from API Ninja if found
                    df['name'] = df.get('name_realtime', ticker)

                show_dashboard(df)
                
            else:
                st.error("No data available. Please check your Trading212 account.")
                
# Show home page if no API key entered
if not api_key:
    show_home_page()
