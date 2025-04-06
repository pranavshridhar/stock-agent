# fetch_stock_data.py

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import random
import time
import uuid




API_KEY = "ALPHAVANTAGE_API_KEY"  # Replace with your actual key

# Load list of S&P 500 companies (manually defined or from a CSV)
@st.cache_data
def load_sp500_symbols():
    url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
    df = pd.read_csv(url)
    return df

# Fetch real-time intraday data from Alpha Vantage
def fetch_intraday(symbol, interval="1min"):
    url = (
        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY"
        f"&symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=compact"
    )
    response = requests.get(url)
    data = response.json()
    key = f"Time Series ({interval})"
    if key not in data:
        st.error("Error fetching data. API limit or bad symbol?")
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(data[key], orient="index")
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

# Streamlit App
def main():
    st.title("📈 Real-Time Stock Plot (Alpha Vantage)")

    sp500 = load_sp500_symbols()
    symbols = sp500["Symbol"].tolist()

    selected_symbol = st.selectbox("Choose a stock symbol:", symbols)

    if st.button("Fetch & Plot Live Data"):
        st.write(f"Showing real-time intraday data for: **{selected_symbol}**")

        placeholder = st.empty()

        for _ in range(10):  # You can change number of refreshes
            df = fetch_intraday(selected_symbol)

            if df.empty:
                st.stop()

            fig = px.line(df, x=df.index, y="close", title=f"{selected_symbol} Price Over Time")
            fig.update_layout(xaxis_title="Timestamp", yaxis_title="Price (USD)")

            placeholder.plotly_chart(fig, use_container_width=True, key=str(uuid.uuid4()))

            time.sleep(5)  # wait 5 seconds between updates

if __name__ == "__main__":
    main()
