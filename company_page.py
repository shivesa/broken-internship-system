"""
pages/company_page.py
----------------------
Handles all Company-facing views:
  1. Register / Login
  2. Post Internship
  3. View Posted Internships
  4. View Applicants (auto-ranked by match score)
"""

import streamlit as st
import pandas as pd
from utils import data_handler as db
from utils import matching
from utils import ui_components as ui


ALL_SKILLS = [
    "Python", "Java", "JavaScript", "C++", "C", "Go", "Rust",
    "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring Boot",
    "HTML", "CSS", "Bootstrap", "Tailwind CSS",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
    "Power BI", "Tableau", "Excel", "Data Visualization",
    "Docker", "Kubernetes", "AWS", "Git", "Linux",
    "REST API", "GraphQL", "Microservices",
    "Arduino", "IoT", "Embedded Systems", "MATLAB",
    "Figma", "UI/UX Design", "Canva",
]

DOMAINS = [
    "Data Science", "Machine Learning / AI", "Web Development",
    "Backend Development", "Mobile Development", "Data Analytics",
    "Cloud / DevOps", "IoT / Embedded", "UI/UX Design", "Cybersecurity", "Other"
]

INDUSTRIES = [
    "Software / AI", "Web Development", "Data Analytics", "Fintech",
    "Edtech", "E-commerce", "Healthcare", "Consulting", "Gaming", "Other"
]

DURATIONS = ["1 Month", "2 Months", "3 Months", "4 Months", "6 Months"]

LOCATIONS = [
    "Remote", "Bangalore (Remote)", "Bangalore (On-site)", "Bangalore (Hybrid)",
    "Mumbai (Remote)", "Mumbai (Hybrid)", "Delhi (Remote)", "Delhi (Hybrid)",
    "Hyderabad (Remote)", "Hyderabad (On-site)", "Pune (Hybrid)", "Chennai (Remote)"
]


# ─── Auth ──────────────────────────────────────────────────────────────────────

def show_auth():
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    with tab1:
        show_login()
    with tab2:
        show_register()


def show_login():
    st.subheader("Company Login")
    email    = st.text_input("Company Email", key="c_login_email")
    password = st.text_input("Password", type="password", key="c_login_pass")

    if st.button("Login", key="c_login_btn", type="primary"):
        if not email or not password:
            st.error("Please fill in all fields.")
            return
        company = db.get_company_by_email(email)
        if company and company["password"] == password:
            st.session_state["company"] = company
            st.success(f"Welcome back, {company['name']}! 🎉")
            st.rerun()
        else:
            st.error("Invalid email or password.")


def show_register():
    st.subheader("Register Your Company")

    col1, col2 = st.columns(2)
    with col1:
        name     = st.text_input("Company Name*", key="c_reg_name")
        email    = st.text_input("Company Email*", key="c_reg_email")
        industry = st.selectbox("Industry*", INDUSTRIES, key="c_reg_industry")
    with col2:
        password = st.text_input("Password*", type="password", key="c_reg_pass")
        website  = st.text_input("Website (optional)", key="c_reg_website")

    description = st.text_area("Company Description*", key="c_reg_desc",
                                placeholder="Tell students what your company does...")

    if st.button("Register Company", key="c_reg_btn", type="primary"):
        if not all([name, email, password, description]):
            st.error("Please fill in all required fields (*).")
            return
        if db.get_company_by_email(email):
            st.error("A company with this email already exists.")
            return

        company_data = {
            "name": name, "email": email, "password": password,
            "industry": industry, "description": description, "website": website
        }
        company = db.add_company(company_data)
        st.session_state["company"] = company
        st.success("Company registered successfully! 🎉")
        st.rerun()


# ─── Main Company Dashboard ────────────────────────────────────────────────────

def show_dashboard():
    company = st.session_state["company"]

    st.sidebar.markdown(f"### 🏢 {company['name']}")
    st.sidebar.caption(f"{company['industry']}")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Navigate",
        ["🏠 Dashboard", "➕ Post Internship", "📋 My Postings", "👥 View Applicants"],
        key="company_menu"
    )

    if st.sidebar.button("🚪 Logout", key="c_logout"):
        del st.session_state["company"]
        st.rerun()

    if menu == "🏠 Dashboard":
        show_company_home(company)
    elif menu == "➕ Post Internship":
        show_post_internship(company)
    elif menu == "📋 My Postings":
        show_my_postings(company)
    elif menu == "👥 View Applicants":
        show_applicants(company)


# ─── Dashboard Home ────────────────────────────────────────────────────────────

def show_company_home(company):
    ui.page_header(f"Welcome, {company['name']}! 🏢",
                   "Your hiring dashboard — find the best intern talent.")

    internships  = db.get_internships_by_company(company["id"])
    all_apps     = db.get_all_applications()
    my_intern_ids = {i["id"] for i in internships}
    my_apps       = [a for a in all_apps if a["internship_id"] in my_intern_ids]

    total_students = len(db.get_all_students())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ui.info_card("Active Postings", str(len(internships)), "📋")
    with col2:
        ui.info_card("Total Applications", str(len(my_apps)), "📥")
    with col3:
        ui.info_card("Students on Platform", str(total_students), "🎓")
    with col4:
        avg = round(sum(a["match_score"] for a in my_apps) / len(my_apps), 1) if my_apps else 0
        ui.info_card("Avg Match Score", f"{avg}%", "🎯")

    st.markdown("---")
    st.markdown(f"**Industry:** {company['industry']}")
    st.markdown(f"**About:** {company['description']}")
    if company.get("website"):
        st.markdown(f"**Website:** {company['website']}")


# ─── Post Internship ───────────────────────────────────────────────────────────

def show_post_internship(company):
    ui.page_header("➕ Post New Internship",
                   "Fill in the details to attract the best candidates.")

    col1, col2 = st.columns(2)
    with col1:
        role     = st.text_input("Role / Position Title*", placeholder="e.g. ML Engineer Intern")
        domain   = st.selectbox("Domain*", DOMAINS)
        stipend  = st.number_input("Monthly Stipend (₹)*", min_value=0, step=500, value=10000)
    with col2:
        duration = st.selectbox("Duration*", DURATIONS)
        location = st.selectbox("Location*", LOCATIONS)

    required_skills = st.multiselect("Required Skills*", ALL_SKILLS)
    description     = st.text_area("Job Description*",
                                    placeholder="Describe the role, responsibilities, and what you're looking for...")

    st.markdown("---")
    st.markdown("**Preview of required skills:**")
    if required_skills:
        ui.skill_pills(required_skills)

    if st.button("🚀 Post Internship", type="primary"):
        if not all([role, domain, required_skills, description]):
            st.error("Please fill in all required fields (*).")
            return

        internship_data = {
            "company_id"      : company["id"],
            "company_name"    : company["name"],
            "role"            : role,
            "required_skills" : required_skills,
            "stipend"         : stipend,
            "duration"        : duration,
            "domain"          : domain,
            "location"        : location,
            "description"     : description,
        }
        db.add_internship(internship_data)
        st.success(f"✅ Internship **{role}** posted successfully!")
        st.balloons()


# ─── My Postings ───────────────────────────────────────────────────────────────

def show_my_postings(company):
    ui.page_header("📋 My Internship Postings",
                   "All internships posted by your company.")

    internships = db.get_internships_by_company(company["id"])
    if not internships:
        st.info("You haven't posted any internships yet. Go to 'Post Internship' to get started!")
        return

    for intern in internships:
        all_apps = db.get_applications_by_internship(intern["id"])
        with st.expander(f"🔹 {intern['role']}  |  {intern['duration']}  |  ₹{intern['stipend']:,}/mo  |  {len(all_apps)} applicants"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Domain:** {intern['domain']}")
                st.write(f"**Location:** {intern['location']}")
                st.write(f"**Posted:** {intern['posted_date']}")
            with col2:
                st.write("**Required Skills:**")
                ui.skill_pills(intern["required_skills"])
            st.write(f"**Description:** {intern['description']}")


# ─── View Applicants ───────────────────────────────────────────────────────────

def show_applicants(company):
    ui.page_header("👥 Applicants",
                   "Candidates auto-ranked by skill match percentage.")

    internships = db.get_internships_by_company(company["id"])
    if not internships:
        st.info("Post an internship first to see applicants.")
        return

    # Select which posting to view
    options = {f"{i['role']} (Posted {i['posted_date']})": i for i in internships}
    choice  = st.selectbox("Select Internship Posting", list(options.keys()))
    intern  = options[choice]

    st.markdown("---")

    # Get all applications for this internship
    apps = db.get_applications_by_internship(intern["id"])

    if not apps:
        st.info("No applications received for this posting yet.")
        return

    st.markdown(f"**Total Applicants:** {len(apps)}  |  **Role:** {intern['role']}")

    # Build ranked table
    ranked_rows = []
    for app in apps:
        student = db.get_student_by_id(app["student_id"])
        if student:
            result = matching.calculate_match_score(student["skills"], intern["required_skills"])
            ranked_rows.append({
                "_score"        : result["score"],
                "student"       : student,
                "match_result"  : result,
                "applied_date"  : app["applied_date"],
            })

    # Sort by score
    ranked_rows.sort(key=lambda x: x["_score"], reverse=True)

    # Display bar chart
    chart_df = pd.DataFrame({
        "Candidate": [r["student"]["name"] for r in ranked_rows],
        "Match %"  : [r["_score"] for r in ranked_rows]
    })
    st.bar_chart(chart_df.set_index("Candidate"))

    st.markdown("---")
    st.markdown("#### 🏆 Ranked Candidates")

    for rank, row in enumerate(ranked_rows, start=1):
        student = row["student"]
        result  = row["match_result"]

        with st.expander(
            f"#{rank}  {student['name']}  —  {result['score']}% Match  |  "
            f"{student['branch']} • {student['year']}"
        ):
            col1, col2 = st.columns([1, 2])
            with col1:
                ui.show_match_badge(result["score"])
                st.write(f"**Branch:** {student['branch']}")
                st.write(f"**Year:** {student['year']}")
                st.write(f"**Domain:** {student['preferred_domain']}")
                st.write(f"**Applied:** {row['applied_date']}")
            with col2:
                st.markdown("**✅ Matching Skills:**")
                if result["matched"]:
                    ui.skill_pills(result["matched"], color="#22c55e")
                else:
                    st.write("None")
                st.markdown("**❌ Missing Skills:**")
                if result["missing"]:
                    ui.missing_skill_pills(result["missing"])
                else:
                    st.write("None — full match!")
            if student.get("bio"):
                st.markdown(f"**Bio:** {student['bio']}")
            if student.get("projects"):
                st.markdown(f"**Projects:** {student['projects']}")

    # Summary table
    st.markdown("---")
    st.markdown("#### 📊 Summary Table")
    summary = pd.DataFrame([
        {
            "Rank"         : i + 1,
            "Name"         : r["student"]["name"],
            "Branch"       : r["student"]["branch"],
            "Year"         : r["student"]["year"],
            "Match Score"  : f"{r['_score']}%",
            "Matched Skills": len(r["match_result"]["matched"]),
            "Missing Skills": len(r["match_result"]["missing"]),
        }
        for i, r in enumerate(ranked_rows)
    ])
    st.dataframe(summary, use_container_width=True)


# ─── Entry Point ───────────────────────────────────────────────────────────────

def render():
    if "company" not in st.session_state:
        show_auth()
    else:
        show_dashboard()
