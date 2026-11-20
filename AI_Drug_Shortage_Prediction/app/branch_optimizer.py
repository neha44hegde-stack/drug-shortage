import streamlit as st

def show_branch_optimizer():

    st.title("🏥 Multi-Branch Stock Optimizer")

    medicines = {
        "Paracetamol": {
            "Branch A": 500,
            "Branch B": 60,
            "Branch C": 240
        },
        "Ibuprofen": {
            "Branch A": 80,
            "Branch B": 350,
            "Branch C": 120
        },
        "Amoxicillin": {
            "Branch A": 50,
            "Branch B": 400,
            "Branch C": 150
        }
    }

    medicine = st.selectbox(
        "Select Medicine",
        list(medicines.keys())
    )

    st.subheader("Current Stock")

    branches = medicines[medicine]

    for branch, stock in branches.items():
        st.write(f"**{branch}:** {stock} units")

    max_branch = max(branches, key=branches.get)
    min_branch = min(branches, key=branches.get)

    transfer = (branches[max_branch] - branches[min_branch]) // 2

    st.markdown("---")

    st.success(
        f"🚚 Transfer **{transfer} units** from **{max_branch}** to **{min_branch}**."
    )