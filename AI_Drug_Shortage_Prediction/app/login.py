import streamlit as st

def show_login():

    st.title("💊 AI Pharmacy Management")

    st.subheader("🔐 Login")

    role = st.selectbox(
        "Login As",
        ["Admin", "Pharmacist"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if role == "Admin":
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Admin Login Successful")
                st.rerun()
            else:
                st.error("❌ Invalid Admin Credentials")

        elif role == "Pharmacist":
            if username == "pharma" and password == "pharma123":
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Pharmacist Login Successful")
                st.rerun()
            else:
                st.error("❌ Invalid Pharmacist Credentials")