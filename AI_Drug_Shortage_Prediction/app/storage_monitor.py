import streamlit as st

def show_storage_monitor():

    st.title("🌡️ Storage Risk Monitor")

    temperature = st.slider("Storage Temperature (°C)", 0, 50, 25)
    humidity = st.slider("Humidity (%)", 0, 100, 50)

    st.subheader("Storage Status")

    if temperature > 35:
        st.error("🔥 High Temperature! Medicine quality may be affected.")
    elif temperature < 5:
        st.warning("🥶 Temperature is too low.")
    else:
        st.success("✅ Temperature is Normal.")

    if humidity > 75:
        st.error("💧 High Humidity! Risk of medicine damage.")
    elif humidity < 20:
        st.warning("🌵 Humidity is too low.")
    else:
        st.success("✅ Humidity is Normal.")

    if 5 <= temperature <= 35 and 20 <= humidity <= 75:
        st.success("🎉 Storage conditions are safe.")