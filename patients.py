"""Patients page."""
from shared import *


def render():
    st.title("👥 Patient Management")
    st.caption("Register, search, update and manage patient information.")
    tab_add, tab_view, tab_edit = st.tabs(["➕ Register patient", "📋 Patient directory", "✏️ Edit / discharge"])

    with tab_add:
        with st.form("add_patient_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full name *")
            age = c2.number_input("Age *", min_value=0, max_value=120, value=18)
            gender = c1.selectbox("Gender *", ["Female", "Male", "Other"])
            phone = c2.text_input("Phone number *")
            blood = c1.selectbox("Blood group", ["Not specified", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            admission = c2.date_input("Admission date", value=date.today())
            address = st.text_area("Address")
            disease = st.text_area("Diagnosis / Disease")
            submitted = st.form_submit_button("Save patient", type="primary")
            if submitted:
                if not name.strip() or not phone.strip():
                    st.error("Name and phone number are required.")
                else:
                    execute("""INSERT INTO patients
                        (name,age,gender,phone,address,blood_group,disease,admission_date,status)
                        VALUES (?,?,?,?,?,?,?,?,?)""",
                        (name.strip(), int(age), gender, phone.strip(), address.strip(),
                         "" if blood == "Not specified" else blood, disease.strip(),
                         admission.isoformat(), "Admitted"))
                    flash_success("Patient registered successfully.")

    with tab_view:
        search = st.text_input("Search patients by name, phone or ID", key="patient_search")
        if search.strip():
            data = query_df("""SELECT id AS 'ID', name AS 'Name', age AS 'Age', gender AS 'Gender',
                phone AS 'Phone', blood_group AS 'Blood group', admission_date AS 'Admission date',
                status AS 'Status' FROM patients
                WHERE name LIKE ? OR phone LIKE ? OR CAST(id AS TEXT) LIKE ? ORDER BY id DESC""",
                (f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            data = query_df("""SELECT id AS 'ID', name AS 'Name', age AS 'Age', gender AS 'Gender',
                phone AS 'Phone', blood_group AS 'Blood group', admission_date AS 'Admission date',
                status AS 'Status' FROM patients ORDER BY id DESC""")
        st.caption(f"{len(data)} patient(s)")
        st.dataframe(data, use_container_width=True, hide_index=True)

    with tab_edit:
        patients_df = query_df("SELECT id, name FROM patients ORDER BY name")
        if patients_df.empty:
            st.info("Register a patient first.")
        else:
            chosen = st.selectbox("Choose patient", patients_df.itertuples(index=False), format_func=lambda x: f"PT-{x.id:04d} · {x.name}")
            p = query_df("SELECT * FROM patients WHERE id=?", (chosen.id,)).iloc[0]
            with st.form("edit_patient_form"):
                c1, c2 = st.columns(2)
                ename = c1.text_input("Full name", value=p["name"])
                eage = c2.number_input("Age", min_value=0, max_value=120, value=int(p["age"]))
                egender = c1.selectbox("Gender", ["Female", "Male", "Other"], index=["Female", "Male", "Other"].index(p["gender"]) if p["gender"] in ["Female", "Male", "Other"] else 0)
                ephone = c2.text_input("Phone", value=p["phone"])
                eblood_options = ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
                eblood = c1.selectbox("Blood group", eblood_options, index=eblood_options.index(p["blood_group"] or "") if (p["blood_group"] or "") in eblood_options else 0)
                estatus = c2.selectbox("Status", ["Admitted", "Discharged"], index=0 if p["status"] == "Admitted" else 1)
                eaddress = st.text_area("Address", value=p["address"] or "")
                edisease = st.text_area("Diagnosis / Disease", value=p["disease"] or "")
                eadmission = st.date_input("Admission date", value=date.fromisoformat(p["admission_date"]))
                save = st.form_submit_button("Update patient", type="primary")
                if save:
                    execute("""UPDATE patients SET name=?,age=?,gender=?,phone=?,blood_group=?,status=?,
                        address=?,disease=?,admission_date=? WHERE id=?""",
                        (ename.strip(), int(eage), egender, ephone.strip(), eblood, estatus,
                         eaddress.strip(), edisease.strip(), eadmission.isoformat(), int(chosen.id)))
                    flash_success("Patient details updated.")
                    st.rerun()
            if st.button("Delete selected patient", type="secondary"):
                linked = scalar("""SELECT
                    (SELECT COUNT(*) FROM appointments WHERE patient_id=?) +
                    (SELECT COUNT(*) FROM bills WHERE patient_id=?) +
                    (SELECT COUNT(*) FROM medical_records WHERE patient_id=?)""",
                    (int(chosen.id), int(chosen.id), int(chosen.id)))
                if linked:
                    st.error("This patient has linked appointments, bills or medical records. Set status to Discharged instead.")
                else:
                    execute("DELETE FROM patients WHERE id=?", (int(chosen.id),))
                    flash_success("Patient deleted.")
                    st.rerun()
