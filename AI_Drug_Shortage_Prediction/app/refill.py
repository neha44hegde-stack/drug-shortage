import streamlit as st
from datetime import datetime, timedelta

def show_refill():

    st.title("📅 Personalized Refill Reminder")

    patient = st.text_input("Patient Name")

    medicine = st.selectbox(
        "Medicine",
        [
            "Paracetamol",
            "Ibuprofen",
            "Amoxicillin",
            "Cetirizine",
            "Metformin",
            "Aspirin",
            "Azithromycin",
            "Omeprazole",
            "Vitamin C",
            "Insulin"
        ]
    )

    quantity = st.number_input(
        "Purchased Quantity (Tablets)",
        min_value=1,
        value=30
    )

    dosage = st.number_input(
        "Tablets Per Day",
        min_value=1,
        value=1
    )

    purchase_date = st.date_input("Purchase Date")

    if st.button("Generate Reminder"):

        days = quantity // dosage

        refill_date = purchase_date + timedelta(days=days)

        st.subheader("📋 Refill Prediction")

        st.success(f"👤 Patient : {patient}")
        st.success(f"💊 Medicine : {medicine}")
        st.info(f"📦 Purchased Quantity : {quantity} Tablets")
        st.info(f"💉 Daily Dosage : {dosage} Tablet(s)")
        st.warning(f"⏳ Refill Needed After : {days} Days")
        st.error(f"📅 Expected Refill Date : {refill_date}")

        st.balloons()