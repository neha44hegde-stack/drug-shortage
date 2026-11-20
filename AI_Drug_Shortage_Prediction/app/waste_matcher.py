import streamlit as st

def show_waste_matcher():

    st.title("🔄 Medicine Waste-to-Need Matcher")

    medicines = {
        "Paracetamol": {
            "Hospital A": 500,
            "Hospital B": 40,
            "Hospital C": 150
        },
        "Ibuprofen": {
            "Hospital A": 80,
            "Hospital B": 300,
            "Hospital C": 50
        },
        "Amoxicillin": {
            "Hospital A": 450,
            "Hospital B": 70,
            "Hospital C": 90
        }
    }

    medicine = st.selectbox(
        "Select Medicine",
        list(medicines.keys())
    )

    stock = medicines[medicine]

    st.subheader("Available Stock")

    for hospital, quantity in stock.items():
        st.write(f"🏥 {hospital}: **{quantity} units**")

    highest = max(stock, key=stock.get)
    lowest = min(stock, key=stock.get)

    st.markdown("---")

    st.success(
        f"✅ AI Recommendation:\n\nTransfer **{medicine}** from **{highest}** to **{lowest}** to reduce medicine wastage and avoid shortages."
    )