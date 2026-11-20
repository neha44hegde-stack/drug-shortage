import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import joblib
import os

# Load dataset
df = pd.read_csv("dataset/drug_data.csv")

# Encode categorical columns
le_drug = LabelEncoder()
le_age = LabelEncoder()
le_severity = LabelEncoder()

df["Drug_Name"] = le_drug.fit_transform(df["Drug_Name"])
df["Age_Group"] = le_age.fit_transform(df["Age_Group"])
df["Severity_Level"] = le_severity.fit_transform(df["Severity_Level"])
df["Shortage_Status"] = df["Shortage_Status"].astype(int)

# Features and target
X = df[
    [
        "Drug_Name",
        "Demand_Quantity",
        "Available_Stock",
        "Temperature",
        "Humidity",
        "Rainfall",
        "Age_Group",
        "Severity_Level",
    ]
]

y = df["Shortage_Status"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    use_label_encoder=False,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# Save model
os.makedirs("../model", exist_ok=True)
joblib.dump(model, "../model/drug_shortage_model.pkl")

print("✅ AI Model Trained Successfully!")