import streamlit as st
from datetime import datetime

from dashboard import show_dashboard
from medicine import show_medicine
from inventory import show_inventory
from sales import show_sales
from prediction import show_prediction
from alerts import show_alerts
from reports import show_reports
from weather import show_weather
from substitute import show_substitute
from forecast import show_forecast
from scanner import show_scanner
from branch_optimizer import show_branch_optimizer
from storage_monitor import show_storage_monitor
from waste_matcher import show_waste_matcher
from dosage_checker import show_dosage_checker
from refill import show_refill
from analytics import show_analytics
from login import show_login
from about import show_about
from history import show_history

st.set_page_config(
    page_title="AI Pharmacy Management",
    page_icon="💊",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# ---------------- Sidebar ---------------- #
if not st.session_state.logged_in:
    show_login()
    st.stop()

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2966/2966485.png",
    width=100
)

st.sidebar.title("💊 AI Pharmacy Management")
st.sidebar.success("Welcome Admin 👋")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()
    
st.sidebar.markdown("---")

st.sidebar.success(
    f"Welcome {st.session_state.role} 👋"
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "💊 Medicine Management",
        "📦 Inventory",
        "💰 Sales",
        "🤖 AI Prediction",
        "📊 Reports",
        "🌦 Weather Trends",
        "🔔 Alerts",
        "💊 Medicine Substitute",
        "📈 AI Demand Forecast",
        "📷 Barcode Scanner",
        "🏥 Multi-Branch Optimizer",
        "🌡️ Storage Risk Monitor",
        "🔄 Waste-to-Need Matcher",
        "💊 Dosage Safety Checker",
        "📅 Refill Reminder",
        "📊 Analytics",
        "ℹ️ About Project",
        "📜 Prediction History",
    ],
)

# ---------------- Navigation ---------------- #

if menu == "🏠 Dashboard":
    show_dashboard()

elif menu == "💊 Medicine Management":
    show_medicine()

elif menu == "📦 Inventory":
    show_inventory()

elif menu == "💰 Sales":
    show_sales()

elif menu == "🤖 AI Prediction":
    show_prediction()

elif menu == "📊 Reports":
    show_reports()

elif menu == "🌦 Weather Trends":
    show_weather()

elif menu == "🔔 Alerts":
    show_alerts()

elif menu == "💊 Medicine Substitute":
    show_substitute()

elif menu == "📈 AI Demand Forecast":
    show_forecast()

elif menu == "📷 Barcode Scanner":
    show_scanner()

elif menu == "🏥 Multi-Branch Optimizer":
    show_branch_optimizer()

elif menu == "🌡️ Storage Risk Monitor":
    show_storage_monitor()

elif menu == "🔄 Waste-to-Need Matcher":
    show_waste_matcher()

elif menu == "💊 Dosage Safety Checker":
    show_dosage_checker()

elif menu == "📅 Refill Reminder":
    show_refill()

elif menu == "📊 Analytics":
    show_analytics()

elif menu == "ℹ️ About Project":
    show_about()

elif menu == "📜 Prediction History":
    show_history()

# ---------------- Footer ---------------- #

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center;'>
        <h4>💊 AI Pharmacy Management System</h4>
        <p>Developed by <b>Angel Beulah K & Team</b></p>
        <p>© 2026 All Rights Reserved</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M')}"
)