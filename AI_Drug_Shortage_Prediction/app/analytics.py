import streamlit as st
import pandas as pd

def show_analytics():

    st.title("📊 Analytics Dashboard")

    st.subheader("📈 Monthly Sales")

    sales = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Sales": [12000, 18000, 15000, 22000, 26000, 24000]
    })

    st.line_chart(sales.set_index("Month"))

    st.markdown("---")

    st.subheader("📦 Medicine Stock")

    stock = pd.DataFrame({
        "Medicine": [
            "Paracetamol",
            "Ibuprofen",
            "Amoxicillin",
            "Insulin",
            "Vitamin C"
        ],
        "Stock": [500, 320, 180, 90, 450]
    })

    st.bar_chart(stock.set_index("Medicine"))

    st.markdown("---")

    st.subheader("🤖 AI Shortage Prediction")

    shortage = pd.DataFrame({
        "Status": ["Shortage", "Available"],
        "Count": [6, 24]
    })

    st.bar_chart(shortage.set_index("Status"))

    st.markdown("---")

    st.subheader("⏰ Expiry Statistics")

    expiry = pd.DataFrame({
        "Category": [
            "Expired",
            "Expiring Soon",
            "Safe"
        ],
        "Medicines": [4, 8, 238]
    })

    st.bar_chart(expiry.set_index("Category"))

    st.markdown("---")

    st.subheader("📊 Overall Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Medicines", "250")

    with c2:
        st.metric("Low Stock", "12")

    with c3:
        st.metric("AI Alerts", "6")

    with c4:
        st.metric("Expired", "4")

    st.success("✅ Analytics Generated Successfully")