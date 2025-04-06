import pandas as pd
import numpy as np
import joblib

# -------------------------------
# Load saved model & scaler
# -------------------------------
model = joblib.load("bankruptcy_model.pkl")
scaler = joblib.load("scaler.pkl")
expected_features = joblib.load("features_list.pkl")

# -------------------------------
# Load the dataset again
# -------------------------------
df = pd.read_csv("data.csv")
X = df.drop("Bankrupt?", axis=1)

# -------------------------------
# Pick a sample row from the dataset
# -------------------------------
sample_index = 100  # Change this index to simulate different companies
company_raw = X.iloc[sample_index]
company_features = company_raw.values.reshape(1, -1)

# -------------------------------
# Scale & Predict
# -------------------------------
company_scaled = scaler.transform(company_features)
prediction = model.predict(company_scaled)[0]
prediction_prob = model.predict_proba(company_scaled)[0][1]

# -------------------------------
# Output
# -------------------------------
print(f"📦 Company #{sample_index}")
print("🔎 Bankruptcy Risk Prediction:", "⚠️ High Risk" if prediction == 1 else "✅ Low Risk")
print(f"📊 Risk Score: {prediction_prob:.2f}")