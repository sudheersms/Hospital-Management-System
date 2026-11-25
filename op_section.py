"""Op Section page."""
from shared import *


def render():
    st.title("🩻 Out-Patient (OP) Department")
    st.caption("Register consultations, assign doctors and track OP visit status.")
    tab_add, tab_view = st.tabs(["➕ Register OP visit", "📋 OP visit register"])
    with tab_add:
        patients_df = query_df("SELECT id,name FROM patients ORDER BY name")
        doctors_df = query_df("SELECT id,name,specialization FROM doctors ORDER BY name")
        if patients_df.empty or doctors_df.empty:
            st.warning("Add at least one patient and one doctor before registering an OP visit.")
        else:
            with st.form("op_visit_form", clear_on_submit=True):
                patient = st.selectbox("Patient", patients_df.itertuples(index=False), format_func=lambda x: f"{x.name} (PT-{x.id})")
                doctor = st.selectbox("Consulting doctor", doctors_df.itertuples(index=False), format_func=lambda x: f"{x.name} — {x.specialization}")
                c1, c2 = st.columns(2)
                visit_date = c1.date_input("Visit date", value=date.today())
                visit_time = c2.time_input("Visit time")
                symptoms = st.text_area("Symptoms / reason for visit")
                diagnosis = st.text_input("Diagnosis")
                fee = st.number_input("Consultation fee (₹)", min_value=0.0, value=500.0, step=50.0)
                status = st.selectbox("Status", ["Waiting", "In Consultation", "Completed", "Cancelled"])
                if st.form_submit_button("Save OP visit", type="primary"):
                    execute("""INSERT INTO op_visits(patient_id,doctor_id,visit_date,visit_time,symptoms,diagnosis,consultation_fee,status)
                               VALUES(?,?,?,?,?,?,?,?)""",
                            (int(patient.id), int(doctor.id), visit_date.isoformat(), visit_time.strftime("%H:%M"),
                             symptoms.strip(), diagnosis.strip(), float(fee), status))
                    flash_success("OP visit registered.")
                    st.rerun()
    with tab_view:
        visits = query_df("""SELECT o.id AS 'OP No.',p.name AS 'Patient',d.name AS 'Doctor',
            d.specialization AS 'Specialization',o.visit_date AS 'Date',o.visit_time AS 'Time',
            o.symptoms AS 'Symptoms',o.diagnosis AS 'Diagnosis',
            o.consultation_fee AS 'Fee (₹)',o.status AS 'Status'
            FROM op_visits o JOIN patients p ON p.id=o.patient_id
            JOIN doctors d ON d.id=o.doctor_id ORDER BY o.visit_date DESC,o.visit_time DESC""")
        if visits.empty:
            st.info("No OP visits have been registered.")
        else:
            st.dataframe(visits, use_container_width=True, hide_index=True)
            op_ids = query_df("SELECT id FROM op_visits ORDER BY id DESC")["id"].tolist()
            selected_op = st.selectbox("Select OP visit to update", op_ids)
            status = st.selectbox("New OP status", ["Waiting", "In Consultation", "Completed", "Cancelled"])
            if st.button("Update OP status", type="primary"):
                execute("UPDATE op_visits SET status=? WHERE id=?", (status, int(selected_op)))
                flash_success("OP visit status updated.")
                st.rerun()
