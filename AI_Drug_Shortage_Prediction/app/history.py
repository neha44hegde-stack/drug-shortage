import streamlit as st
import sqlite3
import pandas as pd

def show_history():

    st.title("📜 Recent Search History")

    conn = sqlite3.connect("pharmacy.db")

    history = pd.read_sql_query(
        "SELECT * FROM prediction_history ORDER BY id DESC",
        conn
    )

    conn.close()

    if not history.empty:
        st.dataframe(history, use_container_width=True)
    else:
        st.info("No prediction history available.")