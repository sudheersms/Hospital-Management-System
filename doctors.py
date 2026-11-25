"""Doctors page."""
from shared import *


def render():
    st.title("🩺 Doctor Management")
    st.caption("Maintain the hospital's doctor directory.")
    tab_add, tab_view, tab_edit = st.tabs(["➕ Add doctor", "📋 Doctor directory", "✏️ Edit doctor"])
    with tab_add:
        with st.form("add_doctor_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Doctor name *")
            specialization = c2.text_input("Specialization *")
            phone = c1.text_input("Phone")
            email = c2.text_input("Email")
            availability = st.text_input("Availability", placeholder="Mon–Fri, 9 AM–2 PM")
            if st.form_submit_button("Save doctor", type="primary"):
                if not name.strip() or not specialization.strip():
                    st.error("Doctor name and specialization are required.")
                else:
                    execute("INSERT INTO doctors(name,specialization,phone,email,availability) VALUES(?,?,?,?,?)",
                            (name.strip(), specialization.strip(), phone.strip(), email.strip(), availability.strip()))
                    flash_success("Doctor added successfully.")
    with tab_view:
        docs = query_df("SELECT id AS 'ID', name AS 'Doctor', specialization AS 'Specialization', phone AS 'Phone', email AS 'Email', availability AS 'Availability' FROM doctors ORDER BY id DESC")
        st.dataframe(docs, use_container_width=True, hide_index=True)
    with tab_edit:
        docs = query_df("SELECT id, name FROM doctors ORDER BY name")
        if docs.empty:
            st.info("Add a doctor first.")
        else:
            chosen = st.selectbox("Choose doctor", docs.itertuples(index=False), format_func=lambda x: f"DR-{x.id:04d} · {x.name}")
            d = query_df("SELECT * FROM doctors WHERE id=?", (chosen.id,)).iloc[0]
            with st.form("edit_doctor_form"):
                n = st.text_input("Doctor name", value=d["name"])
                s = st.text_input("Specialization", value=d["specialization"])
                c1, c2 = st.columns(2)
                ph = c1.text_input("Phone", value=d["phone"] or "")
                em = c2.text_input("Email", value=d["email"] or "")
                av = st.text_input("Availability", value=d["availability"] or "")
                if st.form_submit_button("Update doctor", type="primary"):
                    execute("UPDATE doctors SET name=?,specialization=?,phone=?,email=?,availability=? WHERE id=?",
                            (n.strip(), s.strip(), ph.strip(), em.strip(), av.strip(), int(chosen.id)))
                    flash_success("Doctor updated.")
                    st.rerun()
            if st.button("Delete selected doctor"):
                count = scalar("SELECT COUNT(*) FROM appointments WHERE doctor_id=?", (int(chosen.id),))
                if count:
                    st.error("This doctor has appointments and cannot be deleted.")
                else:
                    execute("DELETE FROM doctors WHERE id=?", (int(chosen.id),))
                    flash_success("Doctor deleted.")
                    st.rerun()
