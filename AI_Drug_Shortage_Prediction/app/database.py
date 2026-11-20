import sqlite3


conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS medicines(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    category TEXT,
    manufacturer TEXT,
    batch_number TEXT,
    expiry_date TEXT,
    price REAL,
    age_group TEXT,
    uses TEXT,
    dosage TEXT,
    prescription_required TEXT,
    side_effects TEXT,
    storage TEXT,
    current_stock INTEGER,
    reorder_level INTEGER,
    shelf_location TEXT,
    image TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER,
    medicine_name TEXT,
    batch_number TEXT,
    quantity INTEGER,
    unit_price REAL,
    total_amount REAL,
    sale_date TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")