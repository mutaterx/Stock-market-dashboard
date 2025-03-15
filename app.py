import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker', value="MSFT")
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')
data = yf.download(ticker,start=start_date, end=end_date)
if ticker:
    # For multiple tickers, separate by space or comma
    tickers = [t.strip() for t in ticker.replace(',', ' ').split()]
    
    # Download the data - this creates a MultiIndex DataFrame
    data = yf.download(tickers, start=start_date, end=end_date)
    
    # Check if we have a MultiIndex (multiple tickers) or single ticker
    if isinstance(data.columns, pd.MultiIndex):
        # Create a figure with traces for each ticker's closing price
        fig = go.Figure()
        
        for tick in tickers:
            try:
                # Access data with MultiIndex
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[('Close', tick)],
                    mode='lines',
                    name=f"{tick} Close"
                ))
            except KeyError:
                st.warning(f"Data for {tick} not available")
        
        fig.update_layout(
            title="Closing Prices",
            xaxis_title="Date",
            yaxis_title="Price",
            legend_title="Tickers"
        )
    else:
        # Single ticker - create a candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=ticker
        )])
        
        fig.update_layout(
            title=f"{ticker} Price",
            xaxis_title="Date",
            yaxis_title="Price"
        )
    
    # Display the plotly figure
    st.plotly_chart(fig)
    
    # Display the raw data
    st.write(data)
else:
    st.write("Please enter a ticker symbol in the sidebar")


st.tabs(["Description"])


