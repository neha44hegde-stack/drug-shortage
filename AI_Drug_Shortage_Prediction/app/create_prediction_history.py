import sqlite3

conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    prediction_result TEXT,
    prediction_date TEXT,
    prediction_time TEXT
)
""")

conn.commit()
conn.close()

print("✅ Prediction History Table Created Successfully!")