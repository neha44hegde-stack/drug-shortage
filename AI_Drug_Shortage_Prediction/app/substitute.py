import streamlit as st

def show_substitute():

    st.title("💊 AI Medicine Substitute Recommendation")

    substitutes = {
        "Paracetamol": ["Crocin 500 mg", "Dolo 500 mg", "Calpol 500 mg"],
        "Ibuprofen": ["Brufen", "Advil", "Nurofen"],
        "Amoxicillin": ["Augmentin", "Mox", "Amoxyclav"],
        "Cetirizine": ["Zyrtec", "Alerid", "Okacet"],
        "Metformin": ["Glycomet", "Obimet", "Cetapin"],
        "Aspirin": ["Disprin", "Ecosprin"],
        "Azithromycin": ["Azee", "Azax", "Zithromax"],
        "Omeprazole": ["Omez", "Ocid", "Omecip"],
        "Vitamin C": ["Limcee", "Celin"],
        "Insulin": ["Humalog", "Novorapid"]
    }

    medicine = st.selectbox(
        "Select Out of Stock Medicine",
        list(substitutes.keys())
    )

    if st.button("Suggest Alternative"):

        st.error(f"❌ {medicine} is Out of Stock")

        st.subheader("✅ Suggested Alternatives")

        for med in substitutes[medicine]:
            st.success(med)