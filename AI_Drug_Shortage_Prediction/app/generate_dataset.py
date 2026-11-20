import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create dataset folder if it doesn't exist
os.makedirs("app/dataset", exist_ok=True)

drug_names = [
    "Paracetamol", "Ibuprofen", "Amoxicillin", "Cetirizine",
    "Metformin", "Aspirin", "Azithromycin", "Omeprazole",
    "Vitamin C", "Insulin"
]

age_groups = ["Child", "Adult", "Senior"]
severity = ["Low", "Medium", "High"]

data = []

for i in range(1, 1001):
    demand = random.randint(50, 500)
    stock = random.randint(20, 600)

    data.append({
        "Drug_ID": f"D{i:04}",
        "Drug_Name": random.choice(drug_names),
        "Demand_Quantity": demand,
        "Available_Stock": stock,
        "Temperature": random.randint(20, 40),
        "Humidity": random.randint(40, 90),
        "Rainfall": random.randint(0, 50),
        "Expiry_Date": (datetime.today() + timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
        "Age_Group": random.choice(age_groups),
        "Severity_Level": random.choice(severity),
        "Shortage_Status": "Yes" if stock < demand else "No"
    })

df = pd.DataFrame(data)

df.to_csv("app/dataset/drug_data.csv", index=False)

print("✅ Dataset created successfully!")