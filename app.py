import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.title('📈Stock Dashboard')
st.markdown("<p style='font-size:18px; color:gray;'>Analyze stock market trends with real-time data visualization. All data is collected from Yahoo Finance.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color:gray;'>https://www.linkedin.com/in/marie-elizabeth-robert-3181471a2/</p>", unsafe_allow_html=True)


# Adding description to the sidebar above the ticker input
st.sidebar.markdown("<p style='font-size:16px; color:gray;'>Enter the company symbol, start date, and end date to show data.</p>", unsafe_allow_html=True)

# Configurating the sidebar
ticker = st.sidebar.text_input('Ticker', value="")
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Create side-by-side tabs using st.columns()
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Stock Data & Graph"):
        active_tab = "Stock Data & Graph"
    else:
        active_tab = None

with col2:
    if st.button("Big Company Tickers"):
        active_tab = "Big Company Tickers"
    else:
        active_tab = None

if active_tab == "Stock Data & Graph":

# Tab selection for the main content area (button tabs)
#tab = st.radio('Select a tab', ['Stock Data & Graph', 'Dictionary of Tickers'])

#Old tab
#if tab == 'Stock Data & Graph':
    if ticker:
        data = yf.download(ticker,start=start_date, end=end_date)
        
        if ticker:
            tickers = [t.strip() for t in ticker.replace(',', ' ').split()]
            
            if isinstance(data.columns, pd.MultiIndex):
                fig = go.Figure()
                
                for tick in tickers:
                    try:
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data[('Close', tick)],
                            mode='lines',
                            name=f"{tick} Close"))
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

# Old tab type
#elif tab == 'Dictionnary of company tickers':
elif active_tab == "Big Company Tickers":    
        # List of big company names and their ticker symbols
    big_companies = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Amazon': 'AMZN',
        'Google': 'GOOGL',
        'Tesla': 'TSLA',
        'Meta': 'META',
        'Nvidia': 'NVDA',
        'Berkshire Hathaway': 'BRK.A',
        'Johnson & Johnson': 'JNJ',
        'Walmart': 'WMT'
    }

    # Show a dictionary with company names and ticker symbols
    st.subheader('Big Companies tickers')
    st.write("Here are some big companies and their ticker symbols:")

    # Display the list as a dictionary
    st.write(big_companies)

    # Add a clickable link to bring people to a dictionary of tickers (external link)
    st.markdown("[Click here for a full dictionary of tickers](https://www.nasdaq.com/symbol/)")


