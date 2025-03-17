import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# Title and description of the app
st.title('📈Stock Dashboard')
st.markdown("<p style='font-size:18px; color:gray;'>Analyze stock market trends with real-time data visualization.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color:gray;'>https://www.linkedin.com/in/marie-elizabeth-robert-3181471a2/</p>", unsafe_allow_html=True)

# Add description in the sidebar above the ticker input
st.sidebar.markdown("<p style='font-size:16px; color:gray;'>Enter the company symbol, start date, and end date to show data.</p>", unsafe_allow_html=True)

# Sidebar inputs
ticker = st.sidebar.text_input('Ticker', value="")
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Tab selection for the main content area
tab = st.selectbox('Select a tab', ['Stock Data & Graph', 'Big Company Tickers'])

if tab == 'Stock Data & Graph':
    # Ensure ticker is not empty before downloading data
    if ticker:
        data = yf.download(ticker, start=start_date, end=end_date)

        # For multiple tickers, separate by space or comma
        tickers = [t.strip() for t in ticker.replace(',', ' ').split()]

        if len(tickers) > 0:  # Check if there are valid tickers
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

            # Display the dataframe
            st.subheader('Stock Data')
            st.dataframe(data)

        else:
            st.warning("Please enter a valid ticker symbol.")
    else:
        st.warning("Please enter a ticker symbol.")

elif tab == 'Big Company Tickers':
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
    st.subheader('Big Companies and Tickers')
    st.write("Here are some big companies and their ticker symbols:")

    # Display the list as a dictionary
    st.write(big_companies)

    # Add a clickable link to bring people to a dictionary of tickers (external link)
    st.markdown("[Click here for a full dictionary of tickers](https://www.nasdaq.com/symbol/)")
