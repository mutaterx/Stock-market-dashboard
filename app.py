import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Using the function st.title for the title of the dashboard
st.title('📈Stock Dashboard')

# Using the function st.markdown to write the description of the dashboard
st.markdown("<p style='font-size:18px; color:gray;'>Analyze stock market trends with real-time data visualization.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color:gray;'>https://www.linkedin.com/in/marie-elizabeth-robert-3181471a2/</p>", unsafe_allow_html=True)

# Using st.markdown with .sidebar, in order to add a description in the sidebar 
st.sidebar.markdown("<p style='font-size:16px; color:gray;'>Enter the company symbol, start date, and end date to show data.</p>", unsafe_allow_html=True)

# Now, in order to allows users to display data based on the companies they choose, I added a input section in the sidebar
# Users must choose a ticker, a ticker refers to the code used to represent a publicly traded company on a stock exchange
# For exemple Microsoft's ticker is MSFT
# Using the st.sidebar.text_input function to display an input box for the tickers
# The variable is 'Ticker' and the default value is empty (value=""), so in order to display data, users must enter a ticker 
# Because the default value is empty, no data will be displayed until a ticker is chosen
ticker = st.sidebar.text_input('Ticker', value="")

# Using the dare_input function so users can choose the periode of data to be displayed
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# In order to seperate the dashboard into two parts, I added a tab selection : one for the main content area and another for a dictionary of tickers
# Using the selectbox() function in order to create a dropdown menu, users will then choose the content they wish to display
# They will choose one of the strings : 'Stock Data & Graph', 'Big Company Tickers', the choosen string is then stored into the tab variable
tab = st.selectbox('Select a tab', ['Stock Data & Graph', 'Big Company Tickers'])

# If the tab variable has the value 'Stock Data & Graph' then view the code up until elif tab = 'Big Company Tickers'
if tab == 'Stock Data & Graph':
    # Before downloading the data from yahoo fiancne and displaying it, I will check that the ticker variable is not empty (this allows me to avoid downloading errors)
    # To check if the ticker variable has a value, I'll use "if ticker: data = yh ...." this translates to : if the ticker variable has a value/is not empty, then download data 
    if ticker:
        data = yf.download(ticker, start=start_date, end=end_date)

        # For easier readability, I chose to separate the tickers by space or comma
        tickers = [t.strip() for t in ticker.replace(',', ' ').split()]

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
