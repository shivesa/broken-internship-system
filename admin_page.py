"""
pages/admin_page.py
--------------------
Basic admin dashboard for platform oversight.
Shows platform-wide analytics and all data in one place.
"""

import streamlit as st
import pandas as pd
from utils import data_handler as db
from utils import ui_components as ui

ADMIN_PASSWORD = "admin@123"   # Hard-coded for demo simplicity


def show_login():
    st.subheader("🔐 Admin Login")
    password = st.text_input("Admin Password", type="password", key="admin_pass")
    if st.button("Login", type="primary", key="admin_login"):
        if password == ADMIN_PASSWORD:
            st.session_state["admin"] = True
            st.rerun()
        else:
            st.error("Incorrect admin password.")
    st.caption("Demo password: `admin@123`")


def show_dashboard():
    if st.sidebar.button("🚪 Logout", key="admin_logout"):
        del st.session_state["admin"]
        st.rerun()

    ui.page_header("🛠 Admin Dashboard",
                   "Platform-wide analytics and oversight.")

    students    = db.get_all_students()
    companies   = db.get_all_companies()
    internships = db.get_all_internships()
    apps        = db.get_all_applications()

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ui.info_card("Students", str(len(students)), "🎓")
    with col2:
        ui.info_card("Companies", str(len(companies)), "🏢")
    with col3:
        ui.info_card("Internships", str(len(internships)), "💼")
    with col4:
        ui.info_card("Applications", str(len(apps)), "📥")

    st.markdown("---")

    # Tabs for each data set
    tab1, tab2, tab3, tab4 = st.tabs(["🎓 Students", "🏢 Companies", "💼 Internships", "📥 Applications"])

    with tab1:
        st.markdown("#### All Registered Students")
        if students:
            df = pd.DataFrame([{
                "ID": s["id"], "Name": s["name"], "Email": s["email"],
                "Branch": s["branch"], "Year": s["year"],
                "Skills Count": len(s["skills"]),
                "Domain": s["preferred_domain"]
            } for s in students])
            st.dataframe(df, use_container_width=True)

            # Skills frequency analysis
            st.markdown("#### 📊 Most Common Student Skills")
            from collections import Counter
            all_skills = [skill for s in students for skill in s["skills"]]
            skill_counts = Counter(all_skills).most_common(10)
            if skill_counts:
                skill_df = pd.DataFrame(skill_counts, columns=["Skill", "Count"])
                st.bar_chart(skill_df.set_index("Skill"))
        else:
            st.info("No students registered yet.")

    with tab2:
        st.markdown("#### All Registered Companies")
        if companies:
            df = pd.DataFrame([{
                "ID": c["id"], "Name": c["name"],
                "Email": c["email"], "Industry": c["industry"],
                "Website": c.get("website", "—")
            } for c in companies])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No companies registered yet.")

    with tab3:
        st.markdown("#### All Posted Internships")
        if internships:
            df = pd.DataFrame([{
                "ID": i["id"], "Role": i["role"],
                "Company": i["company_name"], "Domain": i["domain"],
                "Stipend (₹)": i["stipend"], "Duration": i["duration"],
                "Location": i["location"], "Posted": i["posted_date"],
                "Required Skills": len(i["required_skills"])
            } for i in internships])
            st.dataframe(df, use_container_width=True)

            # Stipend distribution
            st.markdown("#### 💰 Stipend by Role")
            stipend_df = pd.DataFrame({
                "Role": [i["role"] for i in internships],
                "Stipend (₹)": [i["stipend"] for i in internships]
            })
            st.bar_chart(stipend_df.set_index("Role"))
        else:
            st.info("No internships posted yet.")

    with tab4:
        st.markdown("#### All Applications")
        if apps:
            rows = []
            for a in apps:
                student = db.get_student_by_id(a["student_id"])
                intern  = db.get_internship_by_id(a["internship_id"])
                rows.append({
                    "App ID"      : a["id"],
                    "Student"     : student["name"] if student else "Unknown",
                    "Internship"  : intern["role"] if intern else "Unknown",
                    "Company"     : intern["company_name"] if intern else "Unknown",
                    "Match Score" : f"{a['match_score']}%",
                    "Applied On"  : a["applied_date"],
                    "Status"      : a["status"]
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)

            # Match score distribution
            st.markdown("#### 🎯 Match Score Distribution")
            scores = [float(r["Match Score"].replace("%", "")) for r in rows]
            score_df = pd.DataFrame({"Match Score %": scores})

            bins = [0, 20, 40, 60, 80, 100]
            labels = ["0-20", "21-40", "41-60", "61-80", "81-100"]
            score_df["Range"] = pd.cut(score_df["Match Score %"], bins=bins, labels=labels)
            range_counts = score_df["Range"].value_counts().sort_index()
            st.bar_chart(range_counts)
        else:
            st.info("No applications submitted yet.")


def render():
    if "admin" not in st.session_state:
        show_login()
    else:
        show_dashboard()
