import pandas as pd
import streamlit as st
 
@st.cache_data
 
def load_data():
    df = pd.read_csv('stocks.csv')
    numeric_columns = ['Market Cap (USD)', 'P/E Ratio', 'Dividend Yield']
 
    for col in numeric_columns:
        df [col] = pd.to_numeric(df[col], errors='coerce')
 
    return df
 
screener_df = load_data()

def rank_stocks(df,column,ascending=False,top_n=10):
    df ['Rank'] = df [column].rank(ascending=ascending,method='min')
 
    ranked_df = df.sort_values('Rank').head(top_n)
 
    return ranked_df [['Rank', 'Ticker','Company Name',column, 'Market']]
 
st.title('Global Stock Screener')
st.sidebar.head('User Options')
 
markets = screener_df ['Market'].unique()
 
selected_markets = st.sidebar.multiselect( 'Select markets to include:', markets,default=markets)