import pandas as pd
import random
from datetime import datetime, timedelta

medicine_names = [
    "Paracetamol", "Ibuprofen", "Amoxicillin", "Cetirizine",
    "Metformin", "Aspirin", "Azithromycin", "Omeprazole",
    "Vitamin C", "Insulin", "Dolo 650", "Crocin",
    "Pantoprazole", "Ciprofloxacin", "Diclofenac",
    "Atorvastatin", "Losartan", "Amlodipine",
    "Levocetirizine", "Ranitidine"
]

categories = [
    "Tablet",
    "Capsule",
    "Syrup",
    "Injection",
    "Ointment"
]

manufacturers = [
    "Sun Pharma",
    "Cipla",
    "Dr. Reddy's",
    "Abbott",
    "Lupin",
    "Mankind",
    "Zydus",
    "Alkem"
]

age_groups = [
    "Child",
    "Adult",
    "Both"
]

rows = []

for i in range(1000):

    medicine = random.choice(medicine_names)

    category = random.choice(categories)

    manufacturer = random.choice(manufacturers)

    batch = f"BAT{1000+i}"

    expiry = (
        datetime.today() +
        timedelta(days=random.randint(30, 1500))
    ).strftime("%Y-%m-%d")

    price = round(random.uniform(10, 500), 2)

    age = random.choice(age_groups)

    stock = random.randint(0, 500)

    reorder = random.randint(20, 100)

    shelf = f"{chr(random.randint(65,70))}-{random.randint(1,20)}"

    barcode = str(8901234567000 + i)

    image = ""

    rows.append([
        medicine,
        category,
        manufacturer,
        batch,
        expiry,
        price,
        age,
        stock,
        reorder,
        shelf,
        barcode,
        image
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "medicine_name",
        "category",
        "manufacturer",
        "batch_number",
        "expiry_date",
        "price",
        "age_group",
        "current_stock",
        "reorder_level",
        "shelf_location",
        "barcode",
        "image"
    ]
)

df.to_csv("medicine_dataset.csv", index=False)

print("✅ medicine_dataset.csv generated successfully with 1000 records!")