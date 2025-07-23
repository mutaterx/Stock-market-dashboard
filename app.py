import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Using the function st.title for the title of the dashboard
st.title('Stock Market Dashboard')

# Using the function st.markdown to write the description of the dashboard
# Using em to write in italic
st.markdown("<p style='font-size:15px; color:gray;'><em>Analyze the stock market with real-time data visualization.</em></p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:15px; color:gray;'><em>https://www.linkedin.com/in/marie-elizabeth-robert-3181471a2/</em></p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:15px; color:white;'><em>Data is provided by Yahoo Finance</em></p>", unsafe_allow_html=True)


# Using st.markdown with .sidebar, in order to add a description in the sidebar 
st.sidebar.markdown("<p style='font-size:16px; color:gray;'>Enter the company symbol, start date, and end date to show data.</p>", unsafe_allow_html=True)

# Now, in order to allows users to display data based on the companies they choose, I added an input section in the sidebar
# Users must choose a ticker (a ticker refers to the code used to represent a publicly traded company on a stock exchange)
# For exemple Microsoft's ticker is MSFT
# Using the st.sidebar.text_input function to display an input box for the tickers
# The variable is 'Ticker' and the default value is empty (value=""), so in order to display data, users must enter a ticker 
# Because the default value is empty, no data will be displayed until a ticker is chosen
ticker = st.sidebar.text_input('Ticker', value="")

# Using the date_input function so users can choose the periode of data to be displayed
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# In order to seperate the dashboard into two parts, I added a tab selection : one for the main content area and another for a dictionary of tickers
# Using the selectbox() function in order to create a dropdown menu. 
# Users will then choose the content they wish to display
# They will choose one of the strings : 'Stock Data & Graph' or 'Big Company Tickers', the choosen string is then stored into the tab variable
tab = st.selectbox('Select a tab', ['Stock Data & Graph', 'Big Company Tickers'])

# If the tab variable has the value 'Stock Data & Graph' then view the code up until elif tab = 'Big Company Tickers'
if tab == 'Stock Data & Graph':
    if ticker:
        data = yf.download(ticker, start=start_date, end=end_date)

        # Fetch and display company description
        info = yf.Ticker(ticker).info
        company_name = info.get("longName", "N/A")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        country = info.get("country", "N/A")
        exchange = info.get("exchange", "N/A")

        st.markdown(f"""
            <p style='font-size:16px; color:gray;'>
            <strong>Company Name:</strong> {company_name}<br>
            <strong>Sector:</strong> {sector}<br>
            <strong>Industry:</strong> {industry}<br>
            <strong>Country:</strong> {country}<br>
            <strong>Exchange:</strong> {exchange}
            </p>
        """, unsafe_allow_html=True)

        description = info.get("longBusinessSummary", "Description not available.")
        st.subheader("Company Overview")
        st.write(description)

        # Display charts and data
        ticker_symbol = ticker.strip().upper()
        data = yf.download(ticker_symbol, start=start_date, end=end_date)

        if not data.empty:
            # Closing price line chart
            fig_close = go.Figure()
            fig_close.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Closing Price'
            ))
            fig_close.update_layout(
                title=f"{ticker_symbol} - Closing Price",
                xaxis_title="Date",
                yaxis_title="Price"
            )
            st.plotly_chart(fig_close, use_container_width=True)

            # Candlestick chart
            fig_candle = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            )])
            fig_candle.update_layout(
                title=f"{ticker_symbol} - Candlestick Chart",
                xaxis_title="Date",
                yaxis_title="Price"
            )
            st.plotly_chart(fig_candle, use_container_width=True)

            # Show data table
            st.subheader('Stock Data')
            st.dataframe(data)
        else:
            st.warning("No data found for the given ticker and date range.")
    else:
        st.warning("Please enter a ticker symbol.")


elif tab == 'Big Company Tickers':
    # List of big company names and their ticker symbols so that users have access without having to search up the symbols
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

    # Using st.subheader and st.srite to write the subtitle and description of the dictionary tab 
    st.subheader('Big Companies and Tickers')
    st.write("Here are some big companies and their ticker symbols:")

    # Display the list of tickers created in the code above
    st.write(big_companies)

    # Add a clickable link to bring users to a dictionary of tickers (external link)
    st.markdown("[Click here for a full dictionary of tickers](https://www.nasdaq.com/symbol/)")

