import streamlit as st

def show_weather():

    st.title("🌦 Weather Based Medicine Trends")

    weather = st.selectbox(
        "Select Weather",
        ["Sunny", "Rainy", "Cold", "Humid"]
    )

    if weather == "Sunny":
        st.success("☀ Expected High Demand")
        st.write("• ORS")
        st.write("• Electrolytes")
        st.write("• Sunscreen")
        st.write("• Glucose Powder")

    elif weather == "Rainy":
        st.warning("🌧 Expected High Demand")
        st.write("• Paracetamol")
        st.write("• Cough Syrup")
        st.write("• Antibiotics")
        st.write("• Vitamin C")

    elif weather == "Cold":
        st.info("❄ Expected High Demand")
        st.write("• Cough Syrup")
        st.write("• Vitamin C")
        st.write("• Steam Capsules")
        st.write("• Fever Tablets")

    elif weather == "Humid":
        st.error("🌫 Expected High Demand")
        st.write("• Antifungal Cream")
        st.write("• Skin Ointment")
        st.write("• Anti-allergy Tablets")
        