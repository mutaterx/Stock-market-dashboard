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

st.plotychart(data)
#(df, x = 'Date', y = 'Close'
st.write(data)
