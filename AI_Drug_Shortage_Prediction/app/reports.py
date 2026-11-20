import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors


def create_pdf(dataframe):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    elements = []

    data = [list(dataframe.columns)] + dataframe.values.tolist()

    table = Table(
        data,
        repeatRows=1
    )

    table._argW = [
        40,   # ID
        90,   # Medicine
        70,   # Category
        80,   # Manufacturer
        70,   # Batch
        70,   # Expiry
        50,   # Price
        55,   # Age
        80,   # Uses
        55,   # Dosage
        70,   # Prescription
        70,   # Side Effects
        70,   # Storage
        55,   # Stock
        55,   # Reorder
        70    # Shelf
    ]

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ])
    )

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return buffer


def show_reports():

    st.title("📊 Reports & Analytics")

    conn = sqlite3.connect("pharmacy.db")

    medicines = pd.read_sql_query(
        "SELECT * FROM medicines",
        conn
    )

    st.subheader("📋 Medicine Report")

    if not medicines.empty:

        st.dataframe(
            medicines,
            width="stretch"
        )

        csv = medicines.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV Report",
            csv,
            "medicine_report.csv",
            "text/csv"
        )

        pdf = create_pdf(medicines)

        st.download_button(
            "📄 Download PDF Report",
            pdf,
            "medicine_report.pdf",
            "application/pdf"
        )

    else:
        st.info("No medicines available.")

    st.subheader("📈 Stock Report")

    if not medicines.empty:

        chart = medicines.set_index(
            "medicine_name"
        )["current_stock"]

        st.bar_chart(chart)

    conn.close()