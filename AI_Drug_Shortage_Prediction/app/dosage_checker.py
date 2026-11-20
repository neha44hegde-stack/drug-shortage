import streamlit as st
import sqlite3


def show_dosage_checker():

    st.title("💊 Dosage Safety Checker")

    # ---------------- DATABASE CONNECTION ----------------

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    # ---------------- MEDICINE SELECTION ----------------

    st.subheader("💊 Select Medicine")

    medicine_list = cursor.execute("""
        SELECT DISTINCT medicine_name
        FROM medicines
        WHERE medicine_name IS NOT NULL
        AND medicine_name != ''
        ORDER BY medicine_name
    """).fetchall()

    medicine_names = [row[0] for row in medicine_list]

    if not medicine_names:
        st.warning("No medicines found in the database.")
        conn.close()
        return

    medicine = st.selectbox(
        "Medicine Name",
        medicine_names
    )

    # ---------------- PATIENT DETAILS ----------------

    st.subheader("👤 Patient Details")

    age = st.number_input(
        "Patient Age",
        min_value=1,
        max_value=120,
        value=25
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=60.0
    )

    dosage = st.number_input(
        "Prescribed Dosage (mg)",
        min_value=1.0,
        value=500.0
    )

    st.markdown("---")

    # ---------------- CHECK DOSAGE ----------------

    if st.button("🔍 Check Dosage"):

        # Get dosage information from database
        result = cursor.execute("""
            SELECT dosage
            FROM medicines
            WHERE medicine_name = ?
            AND dosage IS NOT NULL
            AND dosage != ''
            LIMIT 1
        """, (medicine,)).fetchone()

        st.subheader("📋 Dosage Analysis")

        st.write(f"**Selected Medicine:** {medicine}")
        st.write(f"**Patient Age:** {age} years")
        st.write(f"**Patient Weight:** {weight} kg")
        st.write(f"**Entered Dosage:** {dosage:.0f} mg")

        # ---------------- DATABASE DOSAGE AVAILABLE ----------------

        if result and result[0]:

            database_dosage = result[0]

            st.info(
                f"📌 Database reference dosage: **{database_dosage}**"
            )

            # Try to extract numeric value from dosage field
            try:

                import re

                numbers = re.findall(
                    r"\d+(?:\.\d+)?",
                    str(database_dosage)
                )

                if numbers:

                    reference_dosage = float(numbers[0])

                    lower_limit = reference_dosage * 0.8
                    upper_limit = reference_dosage * 1.2

                    st.write(
                        f"**Reference Range:** "
                        f"{lower_limit:.0f} – {upper_limit:.0f} mg"
                    )

                    if dosage > upper_limit:

                        st.error(
                            "⚠️ Entered dosage is above the configured "
                            "reference range."
                        )

                    elif dosage < lower_limit:

                        st.warning(
                            "⚠️ Entered dosage is below the configured "
                            "reference range."
                        )

                    else:

                        st.success(
                            "✅ Entered dosage is within the configured "
                            "reference range."
                        )

                else:

                    st.warning(
                        "⚠️ The database dosage value is not numeric."
                    )

            except Exception:

                st.warning(
                    "⚠️ Unable to process the database dosage value."
                )

        # ---------------- NO DOSAGE IN DATABASE ----------------

        else:

            st.warning(
                f"⚠️ No dosage reference is configured for "
                f"**{medicine}** in the database."
            )

            st.info(
                "Add the medicine's reference dosage to the "
                "`dosage` column in the medicines table to enable "
                "the dosage comparison."
            )

    conn.close()