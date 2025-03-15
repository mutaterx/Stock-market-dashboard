# Data process
import numpy as np
import datetime as dt
import pandas as pd

# Yahoo Finance
import yfinance as yf

# Data viz
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')
data = yf.download(ticker,start=start_date, end=end_date)
df = pd.DataFrame(data)

fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=ticker
    )])
    
#fig = px.line(data, x=data.index, y="Close", title="Stock Prices")
st.plotly_chart(fig)
#(df, x = 'Date', y = 'Close'
st.write(data)
