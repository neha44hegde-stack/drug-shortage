import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


def show_sales():

    st.title("💰 Sales Management")

    # ---------------- DATABASE ----------------

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    # Create sales table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            medicine_name TEXT,
            batch_number TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_amount REAL,
            sale_date TEXT
        )
    """)

    # Fix old sales table if columns are missing
    existing_columns = [
        row[1]
        for row in cursor.execute("PRAGMA table_info(sales)").fetchall()
    ]

    required_columns = {
        "medicine_id": "INTEGER",
        "medicine_name": "TEXT",
        "batch_number": "TEXT",
        "quantity": "INTEGER",
        "unit_price": "REAL",
        "total_amount": "REAL",
        "sale_date": "TEXT"
    }

    for column, datatype in required_columns.items():

        if column not in existing_columns:

            cursor.execute(
                f"ALTER TABLE sales ADD COLUMN {column} {datatype}"
            )

    conn.commit()

    # ---------------- SELL MEDICINE ----------------

    st.header("💊 Sell Medicine")

    # UNIQUE MEDICINE NAMES ONLY
    medicines = cursor.execute("""
        SELECT
            medicine_name,
            SUM(current_stock)
        FROM medicines
        GROUP BY medicine_name
        ORDER BY medicine_name
    """).fetchall()

    if not medicines:

        st.warning("No medicines available in the database.")

        conn.close()
        return

    # Medicine name dropdown
    medicine_names = [
        row[0]
        for row in medicines
    ]

    selected_medicine = st.selectbox(
        "Select Medicine",
        medicine_names
    )

    # ---------------- MEDICINE STOCK ----------------

    medicine_rows = cursor.execute("""
        SELECT
            id,
            medicine_name,
            batch_number,
            current_stock,
            price
        FROM medicines
        WHERE medicine_name = ?
        AND current_stock > 0
        ORDER BY id
    """, (selected_medicine,)).fetchall()

    if not medicine_rows:

        st.error("❌ This medicine is currently out of stock.")

        conn.close()
        return

    # Total available stock
    total_stock = sum(
        int(row[3])
        for row in medicine_rows
    )

    # Use first available batch for the sale
    selected_row = medicine_rows[0]

    medicine_id = selected_row[0]
    medicine_name = selected_row[1]
    batch_number = selected_row[2]
    current_stock = selected_row[3]
    unit_price = selected_row[4]

    # ---------------- MEDICINE DETAILS ----------------

    st.subheader("📋 Medicine Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Available Stock",
            total_stock
        )

    with col2:
        st.metric(
            "Price / Unit",
            f"₹{unit_price:.2f}"
        )

    with col3:
        st.metric(
            "Available Batch",
            batch_number
        )

    # ---------------- QUANTITY ----------------

    quantity_options = list(
        range(
            1,
            total_stock + 1
        )
    )

    quantity = st.selectbox(
        "Quantity to Sell",
        quantity_options
    )

    total_amount = quantity * unit_price

    st.info(
        f"💰 Total Sale Amount: ₹{total_amount:.2f}"
    )

    # ---------------- COMPLETE SALE ----------------

    if st.button(
        "💳 Complete Sale",
        use_container_width=True
    ):

        if quantity > total_stock:

            st.error(
                f"❌ Only {total_stock} units are available."
            )

        else:

            remaining_quantity = quantity

            # Deduct stock from batches
            for row in medicine_rows:

                if remaining_quantity <= 0:
                    break

                row_id = row[0]
                batch_stock = int(row[3])

                deduct = min(
                    remaining_quantity,
                    batch_stock
                )

                cursor.execute("""
                    UPDATE medicines
                    SET current_stock = current_stock - ?
                    WHERE id = ?
                """, (
                    deduct,
                    row_id
                ))

                remaining_quantity -= deduct

            sale_date = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Save sale
            cursor.execute("""
                INSERT INTO sales (
                    medicine_id,
                    medicine_name,
                    batch_number,
                    quantity,
                    unit_price,
                    total_amount,
                    sale_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                medicine_id,
                medicine_name,
                batch_number,
                quantity,
                unit_price,
                total_amount,
                sale_date
            ))

            conn.commit()

            st.success(
                f"✅ Sale completed successfully! "
                f"{quantity} unit(s) of {medicine_name} sold."
            )

            st.info(
                f"📦 Remaining Stock: "
                f"{total_stock - quantity} units"
            )

    # ---------------- SALES SUMMARY ----------------

    st.header("📊 Sales Summary")

    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    # TODAY
    today_data = cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(quantity), 0),
            COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE sale_date LIKE ?
    """, (
        today + "%",
    )).fetchone()

    # MONTH
    month_data = cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(quantity), 0),
            COALESCE(SUM(total_amount), 0)
        FROM sales
        WHERE sale_date LIKE ?
    """, (
        month + "%",
    )).fetchone()

    # Today's summary

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Today's Transactions",
            today_data[0]
        )

    with col2:
        st.metric(
            "Today's Units Sold",
            today_data[1]
        )

    with col3:
        st.metric(
            "Today's Sales",
            f"₹{today_data[2]:.2f}"
        )

    # Monthly summary

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Monthly Transactions",
            month_data[0]
        )

    with col2:
        st.metric(
            "Monthly Units Sold",
            month_data[1]
        )

    with col3:
        st.metric(
            "Monthly Sales",
            f"₹{month_data[2]:.2f}"
        )

    # ---------------- SALES HISTORY ----------------

    st.header("📜 Sales History")

    sales_data = pd.read_sql_query("""
        SELECT
            id AS "Sale ID",
            medicine_name AS "Medicine Name",
            batch_number AS "Batch Number",
            quantity AS "Quantity",
            unit_price AS "Unit Price",
            total_amount AS "Total Amount",
            sale_date AS "Sale Date"
        FROM sales
        ORDER BY id DESC
    """, conn)

    if not sales_data.empty:

        st.dataframe(
            sales_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No sales transactions recorded yet."
        )

    # ---------------- LOW STOCK ----------------

    st.header("⚠️ Stock Status")

    low_stock = cursor.execute("""
        SELECT
            medicine_name,
            current_stock,
            reorder_level
        FROM medicines
        WHERE current_stock <= reorder_level
        ORDER BY current_stock ASC
    """).fetchall()

    if low_stock:

        low_stock_data = pd.DataFrame(
            low_stock,
            columns=[
                "Medicine Name",
                "Current Stock",
                "Reorder Level"
            ]
        )

        st.warning(
            "Some medicines have reached their reorder level."
        )

        st.dataframe(
            low_stock_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "✅ All medicines have sufficient stock."
        )

    conn.close()