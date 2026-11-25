"""Dashboard page."""
from shared import *


def render():
    st.markdown("""
    <div class="hero">
      <h1>Your hospital, beautifully in sync ✦</h1>
      <p>A smarter, calmer workspace for every part of patient care and hospital operations.</p>
    </div>
    """, unsafe_allow_html=True)

    total_patients = scalar("SELECT COUNT(*) FROM patients")
    admitted = scalar("SELECT COUNT(*) FROM patients WHERE status='Admitted'")
    doctors = scalar("SELECT COUNT(*) FROM doctors")
    appointments = scalar("SELECT COUNT(*) FROM appointments")
    op_visits = scalar("SELECT COUNT(*) FROM op_visits")
    lab_tests = scalar("SELECT COUNT(*) FROM lab_tests")
    revenue = scalar("SELECT COALESCE(SUM(amount),0) FROM bills WHERE payment_status='Paid'")
    pending = scalar("SELECT COUNT(*) FROM bills WHERE payment_status='Pending'")

    cols = st.columns(4)
    metrics = [
        ("👥 Total patients", total_patients, "All registered patients"),
        ("🛏️ Admitted patients", admitted, "Currently in hospital"),
        ("🩺 Doctors", doctors, "Registered medical staff"),
        ("📅 Appointments", appointments, "Appointments recorded"),
    ]
    for col, (label, value, note) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
                unsafe_allow_html=True,
            )
    extra = st.columns(2)
    extra[0].metric("🩻 OP visits", op_visits)
    extra[1].metric("🧪 Laboratory tests", lab_tests)

    st.write("")
    left, right = st.columns([1.05, 1])
    with left:
        st.markdown(
            f'<div class="hero"><p>FINANCIAL SUMMARY</p><h1>₹{revenue:,.2f}</h1>'
            f'<p>Collected revenue · {pending} pending bills</p></div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="eyebrow">SHORTCUTS</div>', unsafe_allow_html=True)
        st.markdown("### Make something happen")
        a, b, c = st.columns(3)
        with a:
            if st.button("➕ Patient", use_container_width=True):
                st.session_state["quick_page"] = "Patients"
                st.rerun()
        with b:
            if st.button("📅 Appointment", use_container_width=True):
                st.session_state["quick_page"] = "Appointments"
                st.rerun()
        with c:
            if st.button("🧾 Bill", use_container_width=True):
                st.session_state["quick_page"] = "Billing"
                st.rerun()

    st.markdown("### Recently registered patients")
    recent = query_df("SELECT id AS 'Patient ID', name AS 'Name', age AS 'Age', gender AS 'Gender', blood_group AS 'Blood group', admission_date AS 'Admission date', status AS 'Status' FROM patients ORDER BY id DESC LIMIT 8")
    if recent.empty:
        st.info("No patients registered yet. Open Patients to register the first patient.")
    else:
        st.dataframe(recent, use_container_width=True, hide_index=True)

    st.markdown("### Recent appointments")
    upcoming = query_df("""
        SELECT a.id AS 'Appointment ID', p.name AS 'Patient', d.name AS 'Doctor',
               a.appointment_date AS 'Date', a.appointment_time AS 'Time', a.status AS 'Status'
        FROM appointments a JOIN patients p ON p.id=a.patient_id
        JOIN doctors d ON d.id=a.doctor_id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC LIMIT 6
    """)
    if upcoming.empty:
        st.caption("No appointments recorded yet.")
    else:
        st.dataframe(upcoming, use_container_width=True, hide_index=True)
