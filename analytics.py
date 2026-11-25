"""Analytics page."""
from shared import *


def render():
    st.title("📊 Hospital Analytics")
    st.caption("Operational insights and financial performance at a glance.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registered patients", scalar("SELECT COUNT(*) FROM patients"))
    c2.metric("OP consultations", scalar("SELECT COUNT(*) FROM op_visits"))
    c3.metric("Lab investigations", scalar("SELECT COUNT(*) FROM lab_tests"))
    c4.metric("Appointments", scalar("SELECT COUNT(*) FROM appointments"))

    left, right = st.columns(2)
    with left:
        st.markdown("### Patient admission status")
        status_data = query_df("SELECT status AS Status, COUNT(*) AS Patients FROM patients GROUP BY status")
        if not status_data.empty:
            st.bar_chart(status_data.set_index("Status"), color="#2563eb")
        else:
            st.info("No patient data available.")
    with right:
        st.markdown("### OP visit status")
        op_data = query_df("SELECT status AS Status, COUNT(*) AS Visits FROM op_visits GROUP BY status")
        if not op_data.empty:
            st.bar_chart(op_data.set_index("Status"), color="#0f9d91")
        else:
            st.info("No OP visit data available.")

    left, right = st.columns(2)
    with left:
        st.markdown("### Laboratory test status")
        lab_data = query_df("SELECT status AS Status, COUNT(*) AS Tests FROM lab_tests GROUP BY status")
        if not lab_data.empty:
            st.bar_chart(lab_data.set_index("Status"), color="#7957d5")
        else:
            st.info("No laboratory data available.")
    with right:
        st.markdown("### Revenue by payment status")
        revenue_data = query_df("SELECT payment_status AS Status, SUM(amount) AS Amount FROM bills GROUP BY payment_status")
        if not revenue_data.empty:
            st.bar_chart(revenue_data.set_index("Status"), color="#ed8b36")
        else:
            st.info("No billing data available.")

    st.markdown("### Monthly billing trend")
    monthly = query_df("""
        SELECT substr(bill_date,1,7) AS Month, SUM(amount) AS Billed,
               SUM(CASE WHEN payment_status='Paid' THEN amount ELSE 0 END) AS Collected
        FROM bills GROUP BY substr(bill_date,1,7) ORDER BY Month
    """)
    if not monthly.empty:
        st.line_chart(monthly.set_index("Month")[["Billed", "Collected"]])
    else:
        st.info("Monthly billing trends will appear after bills are created.")

    st.markdown("### Export hospital data")
    export_col1, export_col2, export_col3 = st.columns(3)
    exports = [
        ("Patients CSV", "SELECT * FROM patients", export_col1),
        ("Doctors CSV", "SELECT * FROM doctors", export_col2),
        ("Billing CSV", "SELECT * FROM bills", export_col3),
    ]
    for label, sql, col in exports:
        with col:
            df_export = query_df(sql)
            st.download_button(
                f"⬇️ {label}", df_export.to_csv(index=False).encode("utf-8"),
                file_name=label.lower().replace(" ", "_"), mime="text/csv",
                use_container_width=True
            )
