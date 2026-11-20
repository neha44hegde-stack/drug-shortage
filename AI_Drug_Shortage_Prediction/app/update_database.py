import sqlite3

conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE medicines
    ADD COLUMN image TEXT
    """)
    print("✅ Image column added successfully!")
except Exception as e:
    print("ℹ️", e)

conn.commit()
conn.close()