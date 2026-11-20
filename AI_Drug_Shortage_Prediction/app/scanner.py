import streamlit as st
import sqlite3
import os


def show_scanner():

    st.title("📷 Barcode Scanner")

    st.info("Enter or scan the medicine barcode.")

    barcode = st.text_input("Barcode Number")

    if st.button("Search Barcode"):

        conn = sqlite3.connect("pharmacy.db")
        cursor = conn.cursor()

        result = cursor.execute("""
        SELECT
            medicine_name,
            category,
            manufacturer,
            price,
            current_stock,
            image
        FROM medicines
        WHERE barcode=?
        """, (barcode,)).fetchone()

        conn.close()

        if result:

            medicine, category, manufacturer, price, stock, image = result

            st.success("✅ Medicine Found")

            col1, col2 = st.columns([1, 2])

            with col1:

                if image:

                    image_path = os.path.join("images", image)

                    if os.path.exists(image_path):
                        st.image(image_path, width=180)

            with col2:

                st.write(f"**💊 Medicine:** {medicine}")
                st.write(f"**📂 Category:** {category}")
                st.write(f"**🏭 Manufacturer:** {manufacturer}")
                st.write(f"**💰 Price:** ₹{price}")
                st.write(f"**📦 Current Stock:** {stock}")

        else:

            st.error("❌ Barcode not found.")