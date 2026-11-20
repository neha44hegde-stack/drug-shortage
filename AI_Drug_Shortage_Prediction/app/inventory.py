import streamlit as st
import sqlite3

def show_inventory():

    st.title("📦 Inventory Management")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    data = cursor.execute("""
    SELECT
        medicine_name,
        current_stock,
        reorder_level,
        shelf_location
    FROM medicines
    """).fetchall()

    if data:
        st.dataframe(data, width="stretch")
    else:
        st.info("No medicines available.")

    conn.close()