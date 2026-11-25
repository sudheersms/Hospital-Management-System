"""Billing page."""
from shared import *


def render():
    st.title("🧾 Billing & Payments")
    st.caption("Manage OP consultation charges, laboratory charges, admission and other patient invoices.")
    paid_total = scalar("SELECT COALESCE(SUM(amount),0) FROM bills WHERE payment_status='Paid'")
    pending_total = scalar("SELECT COALESCE(SUM(amount),0) FROM bills WHERE payment_status='Pending'")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Collected revenue", f"₹{paid_total:,.2f}")
    with c2:
        st.metric("Outstanding amount", f"₹{pending_total:,.2f}")
    tab_add, tab_view = st.tabs(["➕ Create bill", "📋 Billing records"])
    with tab_add:
        patients_df = query_df("SELECT id,name FROM patients ORDER BY name")
        if patients_df.empty:
            st.info("Register a patient before creating a bill.")
        else:
            with st.form("bill_form", clear_on_submit=True):
                patient_choice = st.selectbox("Patient", patients_df.itertuples(index=False), format_func=lambda x: f"{x.name} (PT-{x.id})")
                category = st.selectbox("Bill category", ["OP Consultation", "Laboratory Test", "Room / Admission", "Pharmacy / Medicines", "Other"])
                amount = st.number_input("Amount (₹)", min_value=0.01, value=100.0, step=50.0)
                bill_date = st.date_input("Bill date", value=date.today())
                status = st.selectbox("Payment status", ["Pending", "Paid"])
                details = st.text_area("Description", placeholder="Enter service details, test name or charge breakdown...")
                description = f"{category}: {details}".strip()
                if st.form_submit_button("Save bill", type="primary"):
                    execute("INSERT INTO bills(patient_id,amount,description,bill_date,payment_status) VALUES(?,?,?,?,?)",
                            (int(patient_choice.id), float(amount), description.strip(), bill_date.isoformat(), status))
                    flash_success("Bill created successfully.")
    with tab_view:
        bills = query_df("""SELECT b.id AS 'ID',p.name AS 'Patient',b.description AS 'Description',
            b.bill_date AS 'Bill date',b.amount AS 'Amount (₹)',b.payment_status AS 'Payment status'
            FROM bills b JOIN patients p ON p.id=b.patient_id ORDER BY b.bill_date DESC,b.id DESC""")
        if bills.empty:
            st.info("No bills created yet.")
        else:
            st.dataframe(bills, use_container_width=True, hide_index=True)
            bill_ids = query_df("SELECT id FROM bills ORDER BY id DESC")["id"].tolist()
            chosen_bill = st.selectbox("Select bill ID", bill_ids)
            new_payment_status = st.selectbox("Set payment status", ["Pending", "Paid"])
            x, y = st.columns([1, 4])
            with x:
                if st.button("Update payment", type="primary"):
                    execute("UPDATE bills SET payment_status=? WHERE id=?", (new_payment_status, int(chosen_bill)))
                    flash_success("Payment status updated.")
                    st.rerun()
            with y:
                if st.button("Delete bill"):
                    execute("DELETE FROM bills WHERE id=?", (int(chosen_bill),))
                    flash_success("Bill deleted.")
                    st.rerun()
