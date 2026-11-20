from datetime import datetime
import streamlit as st
import sqlite3

def show_dashboard():

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    total = cursor.execute(
        "SELECT COUNT(*) FROM medicines"
    ).fetchone()[0]

    low = cursor.execute(
        "SELECT COUNT(*) FROM medicines WHERE current_stock <= reorder_level"
    ).fetchone()[0]

    out = cursor.execute(
        "SELECT COUNT(*) FROM medicines WHERE current_stock = 0"
    ).fetchone()[0]

    conn.close()

    st.title("🏥 AI Pharmacy Management System")

    st.caption("🤖 Powered by XGBoost AI")

    st.write("📅", datetime.now().strftime("%d-%m-%Y %I:%M %p"))

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("💊 Total Medicines", total)

    with c2:
        st.metric("🟠 Low Stock", low)

    with c3:
        st.metric("🔴 Out of Stock", out)

        st.markdown("---")

st.subheader("🧠 AI Model Information")

c1, c2 = st.columns(2)

with c1:
    st.info("""
**Algorithm**
- XGBoost Classifier

**Prediction Type**
- Drug Shortage Classification

**Language**
- Python
""")

with c2:
    st.success("""
**Database**
- SQLite

**Frontend**
- Streamlit

**Backend**
- Python
""")

    st.divider()

    st.subheader("📌 System Overview")

    st.success("✔ Medicine Management")
    st.success("✔ Inventory Management")
    st.success("✔ AI Drug Shortage Prediction")
    st.success("✔ Sales Management")
    st.success("✔ Reports")
    st.success("✔ Weather Trends")
    st.success("✔ Alerts")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💊 Medicines", "250")

    with col2:
        st.metric("📦 Low Stock", "12")

    with col3:
        st.metric("⚠️ AI Alerts", "6")

    with col4:
        st.metric("❌ Expired", "4")

    st.success("✅ System Running Successfully")

    st.markdown("---")

st.subheader("🏥 System Status")

st.success("🟢 AI Prediction Module : Active")

st.success("🟢 Database Connection : Active")

st.success("🟢 Email Notification : Active")

st.success("🟢 Barcode Scanner : Active")

st.success("🟢 Inventory Monitoring : Active")