import sqlite3
import pandas as pd

df = pd.read_csv("medicine_dataset.csv")

conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

count = 0

for _, row in df.iterrows():

    cursor.execute("""
    INSERT INTO medicines
    (
        medicine_name,
        category,
        manufacturer,
        batch_number,
        expiry_date,
        price,
        age_group,
        uses,
        dosage,
        prescription_required,
        side_effects,
        storage,
        current_stock,
        reorder_level,
        shelf_location,
        image,
        barcode
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["medicine_name"],
        row["category"],
        row["manufacturer"],
        row["batch_number"],
        row["expiry_date"],
        float(row["price"]),
        row["age_group"],

        "General Pain Relief",      # uses
        "1 Tablet",                 # dosage
        "No",                       # prescription_required
        "None",                     # side_effects
        "Store below 25°C",         # storage

        int(row["current_stock"]),
        int(row["reorder_level"]),
        row["shelf_location"],
        row["image"],
        str(row["barcode"])
    ))

    count += 1

conn.commit()
conn.close()

print(f"✅ Successfully imported {count} medicines!")