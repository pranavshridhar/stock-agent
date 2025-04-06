import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

# Load the dataset
df = pd.read_csv("data.csv")
X = df.drop("Bankrupt?", axis=1)
y = df["Bankrupt?"]

# Save column order for inference
joblib.dump(X.columns.tolist(), "features_list.pkl")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, "scaler.pkl")

# Train model
model = RandomForestClassifier(random_state=42, class_weight="balanced")
model.fit(X_train_scaled, y_train)
joblib.dump(model, "bankruptcy_model.pkl")

print("✅ Model, scaler, and feature list saved!")