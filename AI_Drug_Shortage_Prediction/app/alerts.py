import streamlit as st
import sqlite3
from email_sender import send_email

def show_alerts():

    st.title("🔔 Alerts")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    # ---------------- LOW STOCK ----------------

    st.subheader("🟠 Low Stock Medicines")

    low = cursor.execute("""
    SELECT medicine_name, current_stock, reorder_level
    FROM medicines
    WHERE current_stock <= reorder_level
    AND current_stock > 0
    """).fetchall()

    if low:

        for idx, (medicine, stock, reorder) in enumerate(low):

            st.warning(
                f"""
**💊 Medicine:** {medicine}

📦 Current Stock: {stock}

🔁 Reorder Level: {reorder}
"""
            )

            if st.button(f"📧 Send Email - {medicine}", key=f"send_email_{idx}"):

                send_email(
                    medicine,
                    stock,
                    reorder
                )

                st.success("✅ Email Sent Successfully!")

            st.divider()

    else:
        st.success("✅ No Low Stock Medicines")

    # ---------------- OUT OF STOCK ----------------

    st.subheader("🔴 Out of Stock Medicines")

    out_stock = cursor.execute("""
    SELECT medicine_name
    FROM medicines
    WHERE current_stock = 0
    """).fetchall()

    if out_stock:

        for med in out_stock:
            st.error(f"❌ {med[0]} is Out of Stock")

    else:
        st.success("✅ No Out of Stock Medicines")

    # ---------------- EXPIRY ----------------

    st.subheader("⚠️ Medicines Expiring Within 30 Days")

    expiry = cursor.execute("""
    SELECT medicine_name, expiry_date
    FROM medicines
    WHERE expiry_date <= date('now','+30 day')
    """).fetchall()

    if expiry:

        for med, exp in expiry:
            st.warning(f"💊 {med} | Expiry Date: {exp}")

    else:
        st.success("✅ No Medicines Expiring Soon")

    conn.close()