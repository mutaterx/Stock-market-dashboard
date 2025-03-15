# Import necessary libraries
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd  # Ensure pandas is imported

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

# Get the ticker symbol and period code
ticker = stocks[selected_stock]
period = period_options[selected_period]

# Fetch stock data from Yahoo Finance
data = yf.download(ticker, period=period, interval="1d")

# Check if data is available
if not data.empty:
    # Plot stock price graph
    fig = px.line(data, x=data.index, y="Close", title=f"{selected_stock} Stock Price Over {selected_period}")
    st.plotly_chart(fig)
else:
    st.warning("No data available for the selected options. Try a different selection.")

