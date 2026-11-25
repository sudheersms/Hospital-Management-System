"""MediCare Hospital Management System — Streamlit entry point."""
from datetime import date
import streamlit as st

from database import init_db
from style import apply_theme
from pages import dashboard, analytics, patients, doctors, op_section, test_section, appointments, medical_records, billing

st.set_page_config(
    page_title="MediCare | Hospital Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()
init_db()

PAGES = {
    "Dashboard": dashboard.render,
    "Analytics": analytics.render,
    "Patients": patients.render,
    "Doctors": doctors.render,
    "OP Section": op_section.render,
    "Appointments": appointments.render,
    "Test Section": test_section.render,
    "Medical Records": medical_records.render,
    "Billing": billing.render,
}

page_names = list(PAGES.keys())
quick_page = st.session_state.pop("quick_page", None)
selected_index = page_names.index(quick_page) if quick_page in page_names else 0

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin:2px 0 8px;">
      <div style="width:43px;height:43px;border-radius:14px;background:linear-gradient(135deg,#8d7cff,#27c6b2);display:flex;align-items:center;justify-content:center;font-size:23px;box-shadow:0 8px 22px #10152f;">
        ✚
      </div>
      <div>
        <div style="font-family:Manrope,sans-serif;font-size:21px;font-weight:900;color:#fff;line-height:1.1;">MediCare</div>
        <div style="font-size:9px;letter-spacing:2px;color:#aeb9e0;font-weight:800;">HOSPITAL SUITE</div>
      </div>
    </div>
    <div style="height:1px;background:linear-gradient(90deg,#8274ef66,transparent);margin:14px 0 18px;"></div>
    """, unsafe_allow_html=True)
    st.caption("WORKSPACE NAVIGATION")
    selected_page = st.radio(
        "NAVIGATION",
        page_names,
        index=selected_index,
        label_visibility="visible",
    )
    st.divider()
    st.markdown("""
    <div style="background:linear-gradient(135deg,#ffffff12,#ffffff06);border:1px solid #ffffff18;border-radius:14px;padding:13px;margin-top:10px;">
      <div style="font-size:11px;letter-spacing:1px;color:#aeb9e0;font-weight:800;">✦ CARE MADE SIMPLER</div>
      <div style="font-size:12px;color:#eef1ff;margin-top:5px;">A connected space for better hospital operations.</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Today · {date.today().strftime('%d %b %Y')}")

PAGES[selected_page]()

st.sidebar.divider()
st.sidebar.caption("MediCare HMS · Academic demonstration")
