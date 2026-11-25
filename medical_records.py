"""Medical Records page."""
from shared import *


def render():
    st.title("📁 Medical Records")
    st.caption("Document patient diagnosis, treatment and ward details.")
    tab_add, tab_view = st.tabs(["➕ Add record", "📋 Records directory"])
    with tab_add:
        patients_df = query_df("SELECT id,name FROM patients ORDER BY name")
        if patients_df.empty:
            st.info("Register a patient before adding a medical record.")
        else:
            with st.form("record_form", clear_on_submit=True):
                patient_choice = st.selectbox("Patient", patients_df.itertuples(index=False), format_func=lambda x: f"{x.name} (PT-{x.id})")
                record_date = st.date_input("Record date", value=date.today())
                diagnosis = st.text_input("Diagnosis")
                treatment = st.text_input("Treatment")
                ward = st.text_input("Ward / Room")
                notes = st.text_area("Doctor notes")
                if st.form_submit_button("Save medical record", type="primary"):
                    execute("""INSERT INTO medical_records(patient_id,diagnosis,treatment,doctor_notes,record_date,ward)
                        VALUES(?,?,?,?,?,?)""",
                        (int(patient_choice.id), diagnosis.strip(), treatment.strip(), notes.strip(), record_date.isoformat(), ward.strip()))
                    flash_success("Medical record saved.")
    with tab_view:
        records = query_df("""SELECT m.id AS 'ID',p.name AS 'Patient',m.record_date AS 'Date',
            m.diagnosis AS 'Diagnosis',m.treatment AS 'Treatment',m.ward AS 'Ward',m.doctor_notes AS 'Notes'
            FROM medical_records m JOIN patients p ON p.id=m.patient_id ORDER BY m.record_date DESC,m.id DESC""")
        if records.empty:
            st.info("No medical records yet.")
        else:
            st.dataframe(records, use_container_width=True, hide_index=True)
            rid = st.selectbox("Select record ID to delete", records["ID"].tolist())
            if st.button("Delete selected record"):
                execute("DELETE FROM medical_records WHERE id=?", (int(rid),))
                flash_success("Medical record deleted.")
                st.rerun()
