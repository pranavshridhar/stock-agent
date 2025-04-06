# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import joblib

# Load model, scaler, and expected feature order
model = joblib.load("bankruptcy_model.pkl")
scaler = joblib.load("scaler.pkl")
expected_features = joblib.load("features_list.pkl")

# Load real dataset for accurate full feature input
df = pd.read_csv("data.csv")
X = df.drop("Bankrupt?", axis=1)
y = df["Bankrupt?"]

# Load S&P 500 tickers
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_table = pd.read_html(url)[0]
all_tickers = sp500_table['Symbol'].tolist()

# ---------------- UI ---------------- #
st.title("📉 AI Bankruptcy Risk Predictor")

mode = st.radio("Choose analysis source:", ["From `data.csv`", "Real-Time (Yahoo Finance)"])

if mode == "From `data.csv`":
    index_selected = st.selectbox("Choose Company Row from CSV", options=list(X.index))

    if st.button("🔍 Analyze CSV Company"):
        try:
            features = X.iloc[index_selected]
            X_input_df = pd.DataFrame([features], columns=expected_features)
            X_scaled = scaler.transform(X_input_df)
            pred = model.predict(X_scaled)[0]
            prob = model.predict_proba(X_scaled)[0][1]

            st.markdown(f"**📦 Company Row:** {index_selected}")
            st.success("✅ Low Risk" if pred == 0 else "⚠️ High Risk")
            st.metric("📊 Bankruptcy Probability", f"{prob:.2%}")
            with st.expander("📌 Show Features"):
                st.write(features)
        except Exception as e:
            st.error(f"Error: {e}")

else:
    selected_ticker = st.selectbox("Choose Ticker", sorted(all_tickers))
    if st.button("🔍 Analyze Ticker"):
        try:
            ticker = selected_ticker.replace(".", "-")
            info = yf.Ticker(ticker).info

            # Build a full-length feature vector based on expected features
            company_stats_dict = {}

            # Fill known mappings
            manual_map = {
                'ROA(C) before interest and depreciation before interest': info.get('returnOnAssets', 0),
                'ROA(A) before interest and % after tax': info.get('returnOnAssets', 0),
                'ROA(B) before interest and depreciation after tax': info.get('returnOnAssets', 0),
                'Operating Gross Margin': info.get('grossMargins', 0),
                'Realized Sales Gross Margin': info.get('grossMargins', 0),
                'Operating Profit Rate': info.get('operatingMargins', 0),
                'Current Ratio': info.get('currentRatio', 0),
                'Debt ratio %': info.get('debtToEquity', 0),
                'Net profit before tax/Paid-in capital': info.get('returnOnEquity', 0),
                'Total Asset Turnover': info.get('revenuePerShare', 0),
            }

            for feat in expected_features:
                company_stats_dict[feat] = manual_map.get(feat, 0.0)

            input_vector = [company_stats_dict[feat] for feat in expected_features]
            X_input_scaled = scaler.transform([input_vector])

            pred = model.predict(X_input_scaled)[0]
            prob = model.predict_proba(X_input_scaled)[0][1]

            st.markdown(f"**📦 Company:** {selected_ticker}")
            st.success("✅ Low Risk" if pred == 0 else "⚠️ High Risk")
            st.metric("📊 Bankruptcy Probability", f"{prob:.2%}")
            with st.expander("📌 Features used:"):
                st.write(pd.DataFrame([company_stats_dict]))
        except Exception as e:
            st.error(f"Error fetching data for {selected_ticker}: {e}")