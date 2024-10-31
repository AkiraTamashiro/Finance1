import streamlit as st
import datetime
import yfinance as yf
import pandas as pd

# Set up cache directory for appdirs
import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"

# Set up your web app
st.set_page_config(layout="wide", page_title="WebApp_Demo")

# Sidebar input
st.sidebar.title("Input")
symbol = st.sidebar.text_input('Please enter the stock symbol:', 'NVDA').upper()

# Selection for a specific time frame.
col1, col2 = st.sidebar.columns(2, gap="medium")
with col1:
    sdate = st.date_input('Start Date', value=datetime.date(2024, 1, 1))
with col2:
    edate = st.date_input('End Date', value=datetime.date.today())

# Display the selected stock symbol
st.title(f"Stock Data for {symbol}")

# Fetch stock data
stock = yf.Ticker(symbol)

# Display company basics
if stock.info.get('sector') and stock.info.get('beta') is not None:
    st.write(f"**Sector:** {stock.info['sector']}")
    st.write(f"**Company Beta:** {stock.info['beta']}")
    st.write(f"**Market Cap:** {stock.info['marketCap']}")
    st.write(f"**PE Ratio:** {stock.info['trailingPE']}")
    st.write(f"**Dividend Yield:** {stock.info['dividendYield'] * 100 if stock.info['dividendYield'] else 0}%")
else:
    st.error("Failed to fetch stock information. Please check the symbol and try again.")

# Download historical data
data = yf.download(symbol, start=sdate, end=edate)

if not data.empty:
    # Create a line chart for the closing prices
    st.line_chart(data['Close'], use_container_width=True)

    # Calculate and display some additional metrics
    st.subheader("Stock Performance Metrics")
    st.write(f"**Max Price:** {data['Close'].max():.2f}")
    st.write(f"**Min Price:** {data['Close'].min():.2f}")
    st.write(f"**Average Price:** {data['Close'].mean():.2f}")
    
    # Simple investment suggestion logic
    current_price = data['Close'][-1]  # Last closing price
    historical_avg = data['Close'].mean()
    
    if current_price < historical_avg * 0.9:
        st.success("**Suggestion:** The current price is significantly below the average. This may be a good buying opportunity!")
    elif current_price > historical_avg * 1.1:
        st.warning("**Suggestion:** The current price is significantly above the average. Consider selling or holding.")
    else:
        st.info("**Suggestion:** The current price is around the average. It's a good time to evaluate your investment strategy.")

else:
    st.error("Failed to fetch historical data. Please check the stock symbol and date range.")
