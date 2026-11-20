import streamlit as st
import sqlite3
import pandas as pd
import os
import shutil


def show_medicine():

    st.title("💊 Medicine Management")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    # ---------------- ADD MEDICINE ----------------

    st.header("➕ Add Medicine")

    # Medicine Name Dropdown
    medicine_list = cursor.execute("""
        SELECT DISTINCT medicine_name
        FROM medicines
        WHERE medicine_name IS NOT NULL
        AND medicine_name != ''
        ORDER BY medicine_name
    """).fetchall()

    medicine_options = [i[0] for i in medicine_list]

    if medicine_options:
        medicine = st.selectbox(
            "Medicine Name",
            medicine_options
        )
    else:
        medicine = st.text_input("Medicine Name")

    # Category Dropdown
    category_list = cursor.execute("""
        SELECT DISTINCT category
        FROM medicines
        WHERE category IS NOT NULL
        AND category != ''
        ORDER BY category
    """).fetchall()

    category_options = [i[0] for i in category_list]

    if category_options:
        category = st.selectbox(
            "Category",
            category_options
        )
    else:
        category = st.text_input("Category")

    # Manufacturer Dropdown
    manufacturer_list = cursor.execute("""
        SELECT DISTINCT manufacturer
        FROM medicines
        WHERE manufacturer IS NOT NULL
        AND manufacturer != ''
        ORDER BY manufacturer
    """).fetchall()

    manufacturer_options = [i[0] for i in manufacturer_list]

    if manufacturer_options:
        manufacturer = st.selectbox(
            "Manufacturer",
            manufacturer_options
        )
    else:
        manufacturer = st.text_input("Manufacturer")

    batch = st.text_input("Batch Number")

    barcode = st.text_input("Barcode Number")

    expiry = st.date_input("Expiry Date")

    price = st.number_input(
        "Price",
        min_value=0.0,
        value=0.0
    )

    age = st.selectbox(
        "Age Group",
        ["Child", "Adult", "Both"]
    )

    stock = st.number_input(
        "Current Stock",
        min_value=0,
        value=0
    )

    reorder = st.number_input(
        "Reorder Level",
        min_value=0,
        value=0
    )

    # ---------------- MEDICINE IMAGE ----------------

    st.subheader("📷 Medicine Image")

    image = st.file_uploader(
        "Upload Medicine Image",
        type=["jpg", "jpeg", "png"]
    )

    if image is not None:

        st.image(
            image,
            caption="Medicine Preview",
            width=200
        )

    # ---------------- SAVE MEDICINE ----------------

    if st.button("💾 Save Medicine"):

        image_name = ""

        if image is not None:

            image_name = image.name

            os.makedirs("images", exist_ok=True)

            image_path = os.path.join(
                "images",
                image_name
            )

            with open(image_path, "wb") as f:
                shutil.copyfileobj(image, f)

        cursor.execute("""
            INSERT INTO medicines
            (
                medicine_name,
                category,
                manufacturer,
                batch_number,
                barcode,
                expiry_date,
                price,
                age_group,
                current_stock,
                reorder_level,
                image
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            medicine,
            category,
            manufacturer,
            batch,
            barcode,
            str(expiry),
            price,
            age,
            stock,
            reorder,
            image_name
        ))

        conn.commit()

        st.success("✅ Medicine Added Successfully!")

    # ---------------- SEARCH MEDICINE ----------------

    st.header("🔍 Search Medicine")

    search = st.text_input(
        "Enter Medicine Name"
    )

    if search:

        result = cursor.execute("""
            SELECT *
            FROM medicines
            WHERE medicine_name LIKE ?
        """, (
            "%" + search + "%",
        )).fetchall()

        if result:

            st.dataframe(
                result,
                use_container_width=True
            )

            st.subheader("🖼 Medicine Images")

            for row in result:

                image_name = row[16]

                if (
                    image_name is not None
                    and str(image_name).strip() != ""
                ):

                    image_path = os.path.join(
                        "images",
                        str(image_name)
                    )

                    if os.path.exists(image_path):

                        st.write(
                            f"**{row[1]}**"
                        )

                        st.image(
                            image_path,
                            width=150
                        )

        else:

            st.warning(
                "Medicine not found!"
            )

    # ---------------- MEDICINE LIST ----------------

    st.header("📋 Medicine List")

    data = pd.read_sql_query(
        "SELECT * FROM medicines",
        conn
    )

    if not data.empty:

        # Display serial number from 1
        data["id"] = range(
            1,
            len(data) + 1
        )

        # Rename database columns
        data.columns = [
            "ID",
            "Medicine Name",
            "Category",
            "Manufacturer",
            "Batch Number",
            "Expiry Date",
            "Price",
            "Age Group",
            "Uses",
            "Dosage",
            "Prescription Required",
            "Side Effects",
            "Storage",
            "Current Stock",
            "Reorder Level",
            "Shelf Location",
            "Image",
            "Barcode"
        ]

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No medicines added yet."
        )

    # ---------------- ALL MEDICINE IMAGES ----------------

    st.subheader(
        "🖼 All Medicine Images"
    )

    if not data.empty:

        for _, row in data.iterrows():

            image_name = row["Image"]

            # Check for empty/NaN image values
            if (
                pd.notna(image_name)
                and str(image_name).strip() != ""
            ):

                image_path = os.path.join(
                    "images",
                    str(image_name)
                )

                if os.path.exists(image_path):

                    st.write(
                        f"**{row['Medicine Name']}**"
                    )

                    st.image(
                        image_path,
                        width=150
                    )

                    st.divider()

    # ---------------- EXPIRY ALERT ----------------

    st.header("⏰ Expiry Alerts")

    expiry_list = cursor.execute("""
        SELECT medicine_name, expiry_date
        FROM medicines
        WHERE expiry_date <= date('now', '+30 day')
    """).fetchall()

    if expiry_list:

        st.error(
            "⚠️ Medicines Expiring Within 30 Days"
        )

        st.table(
            expiry_list
        )

    else:

        st.success(
            "✅ No medicines expiring soon."
        )

    # ---------------- LOW STOCK ----------------

    st.header("📦 Low Stock Alert")

    low = cursor.execute("""
        SELECT
            medicine_name,
            current_stock,
            reorder_level
        FROM medicines
        WHERE current_stock <= reorder_level
    """).fetchall()

    if low:

        st.warning(
            "⚠️ Low Stock Medicines"
        )

        st.table(
            low
        )

    else:

        st.success(
            "✅ All medicines have sufficient stock."
        )

    # ---------------- CLOSE DATABASE ----------------

    conn.close()