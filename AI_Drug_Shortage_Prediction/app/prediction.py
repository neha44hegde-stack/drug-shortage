import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import datetime


def show_prediction():

    st.title("🤖 AI Drug Shortage Prediction")

    st.success("🧠 AI Model: XGBoost Classifier")

    model = joblib.load("../model/drug_shortage_model.pkl")

    drug_name = st.selectbox(
        "Drug Name",
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
            "Insulin",
        ],
    )

    drug_mapping = {
        "Paracetamol": 0,
        "Ibuprofen": 1,
        "Amoxicillin": 2,
        "Cetirizine": 3,
        "Metformin": 4,
        "Aspirin": 5,
        "Azithromycin": 6,
        "Omeprazole": 7,
        "Vitamin C": 8,
        "Insulin": 9,
    }

    age = st.selectbox("Age Group", ["Child", "Adult", "Senior"])
    age_map = {"Child": 0, "Adult": 1, "Senior": 2}

    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    severity_map = {"Low": 0, "Medium": 1, "High": 2}

    demand = st.number_input("Demand Quantity", min_value=1, value=100)
    stock = st.number_input("Available Stock", min_value=0, value=80)
    temperature = st.number_input("Temperature", value=30)
    humidity = st.number_input("Humidity", value=60)
    rainfall = st.number_input("Rainfall", value=20)

    if st.button("Predict"):

        data = pd.DataFrame(
            [[
                drug_mapping[drug_name],
                demand,
                stock,
                temperature,
                humidity,
                rainfall,
                age_map[age],
                severity_map[severity],
            ]],
            columns=[
                "Drug_Name",
                "Demand_Quantity",
                "Available_Stock",
                "Temperature",
                "Humidity",
                "Rainfall",
                "Age_Group",
                "Severity_Level",
            ],
        )

        prediction = model.predict(data)[0]

        # Save prediction history
        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        result = (
            "Drug Shortage Predicted"
            if prediction == 1
            else "Stock is Sufficient"
        )

        now = datetime.now()

        cursor.execute("""
        INSERT INTO prediction_history
        (
            medicine_name,
            prediction_result,
            prediction_date,
            prediction_time
        )
        VALUES (?, ?, ?, ?)
        """, (
            drug_name,
            result,
            now.strftime("%d-%m-%Y"),
            now.strftime("%I:%M %p")
        ))

        conn.commit()
        conn.close()

        if prediction == 1:

            st.error("⚠️ Drug Shortage Predicted")

            st.info(
                "💡 Recommendation: Increase stock or order additional units to avoid shortages."
            )

        else:

            st.success("✅ Stock is Sufficient")

            st.info(
                "✔ Current inventory is adequate. Continue regular stock monitoring."
            )