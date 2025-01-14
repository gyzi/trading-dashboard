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
st.sidebar.header('User Options')
 
markets = screener_df ['Market'].unique()
 
selected_markets = st.sidebar.multiselect( 'Select markets to include:', markets,default=markets)

filtered_df = screener_df [screener_df ['Market'].isin(selected_markets)]
 
ranking_options = ['Market Cap (USD)', 'P/E Ratio', 'Dividend Yield']
selected_metric = st.sidebar.selectbox('Select a metric to rank by:', ranking_options)
 
sort_order = st.sidebar.radio('Sort order:', ['Descending', 'Ascending']) 
ascending = sort_order == 'Ascending'
 
top_n = st.sidebar.slider('Number of top stocks to display:', min_value=5,max_value=50,value=10,step=1)

st.subheader(f"Top {top_n} stocks in selected markets by {selected_metric}")

ranked_stocks = rank_stocks(filtered_df,selected_metric,ascending,top_n)

st.dataframe(ranked_stocks)