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
st.markdown("<p style='font-size:15px; color:gray;'><em>Data is provided by Yahoo Finance</em></p>", unsafe_allow_html=True)

# Using st.markdown with .sidebar, in order to add a description in the sidebar 
st.sidebar.markdown("<p style='font-size:16px; color:gray;'>Enter the company symbol, start date, and end date to show data.</p>", unsafe_allow_html=True)

# Now, in order to allow users to display data based on the companies they choose, I added an input section in the sidebar
# Users must choose a ticker (a ticker refers to the code used to represent a publicly traded company on a stock exchange)
# For example Microsoft's ticker is MSFT
# Using the st.sidebar.text_input function to display an input box for the tickers
# The variable is 'ticker' and the default value is empty (value=""), so in order to display data, users must enter a ticker 
ticker = st.sidebar.text_input('Ticker', value="")

# Using the date_input function so users can choose the period of data to be displayed
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Adding a dropdown to switch between tabs for main content or company list
tab = st.selectbox('Select a tab', ['Stock Data & Graph', 'Big Company Tickers'])

# With this code, the fetched downloaded data and company info will be cached.
# Caching the data will speed up the app and reduce the number of requests (in order to avoid Yahoo finance API limit)
@st.cache_data(show_spinner=False)
def get_stock_data(ticker_symbol, start, end):
    return yf.download(ticker_symbol, start=start, end=end)

@st.cache_data(show_spinner=False)
def get_company_info(ticker_symbol):
    return yf.Ticker(ticker_symbol).info

# If the tab variable has the value 'Stock Data & Graph' then view the code up until elif tab = 'Big Company Tickers'
if tab == 'Stock Data & Graph':
    # Before downloading the data from Yahoo Finance and displaying it, the code will check that the ticker variable is not empty (this avoids downloading errors)
    if ticker:
         data = yf.download(ticker, start=start_date, end=end_date)
        # Code to fetch and display company description and info from Yahoo Finance 
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

        # Creating the list 'tickers' that stores all the ticker symbols entered by users
        # In case users enter commas to separate the tickers, the code will transform the commas into spaces with ticker.replace(',', ' ')
        # Then the code will store the values into a list thanks to .split()
        # For example: "AAPL, MSFT, TSLA" → ["AAPL", "MSFT", "TSLA"]
        tickers = [t.strip() for t in ticker.replace(',', ' ').split()]

        # len(tickers) checks the number of items in the list named 'tickers'
        # if and > 0, allows the code to run if there is at least 1 symbol in the list
        if len(tickers) > 0:  # Check if there are valid tickers
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

                # Display the line chart for closing prices
                fig.update_layout(
                    title="Closing Prices",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    legend_title="Tickers"
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                # If it's a single ticker, handle it directly
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Close'],
                    mode='lines',
                    name=f"{tickers[0]} Close"
                ))
                fig.update_layout(
                    title=f"{tickers[0]} - Closing Price",
                    xaxis_title="Date",
                    yaxis_title="Price"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Display the raw data table
            st.subheader('Stock Data')
            st.dataframe(data)
        else:
            st.warning("Please enter a valid ticker symbol.")  # If the ticker is not valid, show warning
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

    # Using st.subheader and st.write to write the subtitle and description of the dictionary tab 
    st.subheader('Big Companies and Tickers')
    st.write("Here are some big companies and their ticker symbols:")

    # Display the list of tickers created in the code above
    st.write(big_companies)

    # Add a clickable link to bring users to a dictionary of tickers (external link)
    st.markdown("[Click here for a full dictionary of tickers](https://www.nasdaq.com/symbol/)")
