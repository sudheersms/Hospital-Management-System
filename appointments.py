"""Appointments page."""
from shared import *


def render():
    st.title("📅 Appointment Management")
    st.caption("Book consultations and update appointment status.")
    tab_add, tab_view = st.tabs(["➕ Schedule appointment", "📋 Appointment list"])
    with tab_add:
        patients_df = patient_options(admitted_only=True)
        doctors_df = doctor_options()
        if patients_df.empty or doctors_df.empty:
            st.warning("Add at least one admitted patient and one doctor before scheduling.")
        else:
            with st.form("appointment_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                patient_choice = c1.selectbox("Patient", patients_df.itertuples(index=False), format_func=lambda x: x.name)
                doctor_choice = c2.selectbox("Doctor", doctors_df.itertuples(index=False), format_func=lambda x: f"{x.name} — {x.specialization}")
                ap_date = c1.date_input("Appointment date", min_value=date.today())
                ap_time = c2.time_input("Appointment time")
                reason = st.text_area("Reason for visit")
                if st.form_submit_button("Schedule appointment", type="primary"):
                    execute("""INSERT INTO appointments(patient_id,doctor_id,appointment_date,appointment_time,reason,status)
                        VALUES(?,?,?,?,?,'Scheduled')""",
                        (int(patient_choice.id), int(doctor_choice.id), ap_date.isoformat(), ap_time.strftime("%H:%M"), reason.strip()))
                    flash_success("Appointment scheduled.")
    with tab_view:
        appts = query_df("""SELECT a.id AS 'ID', p.name AS 'Patient', d.name AS 'Doctor',
            a.appointment_date AS 'Date', a.appointment_time AS 'Time',
            a.reason AS 'Reason', a.status AS 'Status'
            FROM appointments a JOIN patients p ON p.id=a.patient_id
            JOIN doctors d ON d.id=a.doctor_id ORDER BY a.appointment_date DESC,a.appointment_time DESC""")
        if appts.empty:
            st.info("No appointments recorded.")
        else:
            st.dataframe(appts, use_container_width=True, hide_index=True)
            appt_ids = query_df("SELECT id FROM appointments ORDER BY id DESC")
            chosen_id = st.selectbox("Select appointment ID to update", appt_ids["id"].tolist())
            new_status = st.selectbox("New status", ["Scheduled", "Completed", "Cancelled"])
            c1, c2 = st.columns([1, 4])
            with c1:
                if st.button("Update status", type="primary"):
                    execute("UPDATE appointments SET status=? WHERE id=?", (new_status, int(chosen_id)))
                    flash_success("Appointment status updated.")
                    st.rerun()
            with c2:
                if st.button("Delete appointment"):
                    execute("DELETE FROM appointments WHERE id=?", (int(chosen_id),))
                    flash_success("Appointment deleted.")
                    st.rerun()
