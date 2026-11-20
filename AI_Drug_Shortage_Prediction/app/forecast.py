import streamlit as st

def show_forecast():

    st.title("📈 AI Demand Forecast")

    medicines = {
        "Paracetamol": {"stock": 500, "7": 180, "15": 420, "30": 850},
        "Ibuprofen": {"stock": 350, "7": 120, "15": 280, "30": 600},
        "Amoxicillin": {"stock": 250, "7": 90, "15": 210, "30": 450},
        "Cetirizine": {"stock": 400, "7": 110, "15": 260, "30": 500},
        "Metformin": {"stock": 300, "7": 130, "15": 300, "30": 620},
        "Aspirin": {"stock": 280, "7": 95, "15": 210, "30": 430},
        "Azithromycin": {"stock": 220, "7": 80, "15": 180, "30": 390},
        "Omeprazole": {"stock": 320, "7": 100, "15": 240, "30": 510},
        "Vitamin C": {"stock": 600, "7": 200, "15": 450, "30": 900},
        "Insulin": {"stock": 180, "7": 75, "15": 170, "30": 350}
    }

    medicine = st.selectbox(
        "Select Medicine",
        list(medicines.keys())
    )

    if st.button("Forecast Demand"):

        stock = medicines[medicine]["stock"]
        d7 = medicines[medicine]["7"]
        d15 = medicines[medicine]["15"]
        d30 = medicines[medicine]["30"]

        st.subheader(f"📦 Current Stock : {stock} units")

        st.info(f"📅 Next 7 Days : {d7} units")
        st.info(f"📅 Next 15 Days : {d15} units")
        st.info(f"📅 Next 30 Days : {d30} units")

        if d30 > stock:
            order = d30 - stock
            st.error(f"⚠️ Recommendation: Order {order} more units.")
        else:
            st.success("✅ Current stock is sufficient.")