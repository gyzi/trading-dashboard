import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Trading212 Portfolio Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load and process data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('trading212_positions.csv')
        df['initialFillDate'] = pd.to_datetime(df['initialFillDate'])
        df['totalValue'] = df['quantity'] * df['currentPrice']
        df['totalCost'] = df['quantity'] * df['averagePrice']
        df['profitLoss'] = df['ppl']
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Load data
df = load_data()

if not df.empty:
    st.title("📊 Trading212 Portfolio Dashboard")
    
    # Summary metrics
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

    # Create tabs
    tab1, tab2 = st.tabs(["Portfolio Overview", "Position Details"])

    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Portfolio Allocation Pie Chart
            fig_pie = px.pie(
                df,
                values='totalValue',
                names='ticker',
                title="Portfolio Allocation",
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Top Performers
            fig_bar = px.bar(
                df.nlargest(10, 'profitLoss'),
                x='ticker',
                y='profitLoss',
                title="Top 10 Positions by P/L",
                color='profitLoss',
                color_continuous_scale=['red', 'green']
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        # Detailed Position Table
        st.subheader("Position Details")
        
        # Format columns for display
        display_df = df[['ticker', 'quantity', 'averagePrice', 'currentPrice', 
                        'profitLoss', 'totalValue', 'initialFillDate']]
        
        display_df = display_df.style.format({
            'averagePrice': '${:.2f}',
            'currentPrice': '${:.2f}',
            'profitLoss': '${:.2f}',
            'totalValue': '${:.2f}',
            'initialFillDate': lambda x: x.strftime('%Y-%m-%d')
        })
        
        st.dataframe(display_df, use_container_width=True)

else:
    st.error("No data available. Please check if trading212_positions.csv exists and is properly formatted.")