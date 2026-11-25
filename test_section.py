"""Test Section page."""
from shared import *


def render():
    st.title("🧪 Laboratory & Diagnostic Tests")
    st.caption("Create test requests, record results and monitor test status.")
    tab_add, tab_view = st.tabs(["➕ Add test", "📋 Test register"])
    with tab_add:
        patients_df = query_df("SELECT id,name FROM patients ORDER BY name")
        if patients_df.empty:
            st.warning("Register a patient before adding a test.")
        else:
            with st.form("lab_test_form", clear_on_submit=True):
                patient = st.selectbox("Patient", patients_df.itertuples(index=False), format_func=lambda x: f"{x.name} (PT-{x.id})")
                test_name = st.selectbox("Test name", [
                    "Complete Blood Count (CBC)", "Blood Glucose", "Lipid Profile",
                    "Liver Function Test (LFT)", "Kidney Function Test (KFT)",
                    "Thyroid Function Test (TFT)", "Urine Analysis", "X-Ray", "ECG", "Other"
                ])
                if test_name == "Other":
                    test_name = st.text_input("Enter test name")
                c1, c2 = st.columns(2)
                test_date = c1.date_input("Test date", value=date.today())
                amount = c2.number_input("Test charge (₹)", min_value=0.0, value=300.0, step=50.0)
                notes = st.text_area("Sample details / notes")
                if st.form_submit_button("Save test request", type="primary"):
                    if not test_name.strip():
                        st.error("Please enter a test name.")
                    else:
                        execute("""INSERT INTO lab_tests(patient_id,test_name,test_date,notes,amount,status)
                                   VALUES(?,?,?,?,?,'Pending')""",
                                (int(patient.id), test_name.strip(), test_date.isoformat(), notes.strip(), float(amount)))
                        flash_success("Test request added.")
                        st.rerun()
    with tab_view:
        tests = query_df("""SELECT t.id AS 'Test ID',p.name AS 'Patient',t.test_name AS 'Test',
            t.test_date AS 'Date',t.result AS 'Result',t.notes AS 'Notes',
            t.amount AS 'Charge (₹)',t.status AS 'Status'
            FROM lab_tests t JOIN patients p ON p.id=t.patient_id
            ORDER BY t.test_date DESC,t.id DESC""")
        if tests.empty:
            st.info("No tests have been added.")
        else:
            st.dataframe(tests, use_container_width=True, hide_index=True)
            test_ids = query_df("SELECT id FROM lab_tests ORDER BY id DESC")["id"].tolist()
            selected_test = st.selectbox("Select test to update", test_ids)
            current_test = query_df("SELECT result,notes,status FROM lab_tests WHERE id=?", (int(selected_test),)).iloc[0]
            with st.form("test_result_form"):
                result = st.text_area("Result", value=current_test["result"] or "")
                notes = st.text_area("Lab notes", value=current_test["notes"] or "")
                status = st.selectbox("Test status", ["Pending", "Sample Collected", "Completed"],
                                      index=["Pending", "Sample Collected", "Completed"].index(current_test["status"]))
                if st.form_submit_button("Update test result", type="primary"):
                    execute("UPDATE lab_tests SET result=?,notes=?,status=? WHERE id=?",
                            (result.strip(), notes.strip(), status, int(selected_test)))
                    flash_success("Test result updated.")
                    st.rerun()
