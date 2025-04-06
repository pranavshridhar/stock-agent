# import requests
# import os
# from dotenv import load_dotenv

# import streamlit as st

# st.title("🚀 Bankruptcy Risk AI")
# st.write("Welcome to your ML-powered risk prediction app!")
# load_dotenv()
# api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# def get_stock_data(symbol):
#     url = f"https://www.alphavantage.co/query"
#     params = {
#         "function": "TIME_SERIES_INTRADAY",
#         "symbol": symbol,
#         "interval": "1min",
#         "apikey": api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()

#     try:
#         last_refreshed = list(data["Time Series (1min)"].keys())[0]
#         latest_data = data["Time Series (1min)"][last_refreshed]
#         return {
#             "symbol": symbol,
#             "price": float(latest_data["4. close"]),
#             "volume": int(latest_data["5. volume"])
#         }
#     except Exception as e:
#         print("Error:", e)
#         return None

# print(get_stock_data("AAPL"))
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Load model and artifacts
model = joblib.load("bankruptcy_model.pkl")
scaler = joblib.load("scaler.pkl")
expected_features = joblib.load("features_list.pkl")  # List of 95 features

st.set_page_config(page_title="Bankruptcy Predictor", layout="centered")
st.title("💼 Bankruptcy Risk Predictor")

st.markdown("Enter a few known financial metrics. The rest will be filled with defaults.")

# Collect user inputs for a few known features
user_inputs = {}
for feature in expected_features[:5]:  # Let’s show first 5 for simplicity
    user_inputs[feature] = st.number_input(f"{feature}", value=0.0)

# Build full input feature vector (fill missing with 0.0)
input_vector = np.array([user_inputs.get(f, 0.0) for f in expected_features]).reshape(1, -1)
input_scaled = scaler.transform(input_vector)

# Predict
prediction = model.predict(input_scaled)[0]
prediction_prob = model.predict_proba(input_scaled)[0][1]

st.subheader("🔍 Bankruptcy Risk Prediction:")
if prediction == 1:
    st.error("⚠️ High Risk")
else:
    st.success("✅ Low Risk")
st.metric("📊 Risk Score", f"{prediction_prob:.2f}")

# Optional: Visualize training data distribution
if st.checkbox("📈 Show Sample Data & Distribution"):
    df = pd.read_csv("data.csv")
    st.dataframe(df.head())

    st.subheader("📉 Feature Distribution: ROA(C)")
    fig, ax = plt.subplots()
    sns.histplot(df["ROA(C) before interest and depreciation before interest"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

st.markdown("---")
st.caption("Built with ❤️ by you + AI")