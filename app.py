# IMPORTING LIBRARIES

import streamlit as st
import pandas as pd
import yfinance as yf 
import plotly.express as px

# Define stock tickers for Thales, Safran, and Dassault Aviation (Yahoo Finance symbols)
tickers = ["HO.PA", "SAF.PA", "AM.PA"]  # ".PA" means Paris Stock Exchange

# Mapping of company names to Yahoo Finance tickers
stocks = {
    "Thales S.A.": "HO.PA",
    "Safran": "SAF.PA",
    "Dassault Aviation": "AM.PA"
}

# Mapping of period options
period_options = {
    "1 Week": "1wk",
    "1 Month": "1mo",
    "6 Months": "6mo",
    "1 Year": "1y"
}

# Streamlit App Title
st.title("📈 Stock Price Viewer")

# Dropdown list for selecting company
selected_stock = st.selectbox("Select a company:", list(stocks.keys()))

# Dropdown list for selecting time period
selected_period = st.selectbox("Select a time period:", list(period_options.keys()))

# Get the ticker symbol
ticker = stocks[selected_stock]
period = period_options[selected_period]

# Fetch stock data from Yahoo Finance
data = yf.download(ticker, period=period, interval="1d")

# Check if data is available
if not data.empty:
    # Find highest and lowest price
    highest_price = data["High"].max()
    lowest_price = data["Low"].min()

    # Check if prices are valid (not None or NaN)
    if highest_price is not None and lowest_price is not None:
        # Display highest & lowest prices
        st.markdown(f"### 📊 Stock: {selected_stock} ({ticker})")
        st.markdown(f"✅ **Highest Price:** €{highest_price:.2f}")
        st.markdown(f"❌ **Lowest Price:** €{lowest_price:.2f}")
    else:
        st.warning("Could not find valid highest or lowest price data.")

    # Plot stock price graph
    fig = px.line(data, x=data.index, y="Close", title=f"{selected_stock} Stock Price Over {selected_period}")
    st.plotly_chart(fig)

else:
    st.warning("No data available for the selected options. Try a different selection.")
