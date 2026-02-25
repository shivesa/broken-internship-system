"""
pages/student_page.py
----------------------
Handles all Student-facing views:
  1. Register / Login
  2. Profile (view & edit)
  3. Internship Recommendations with match scores
  4. Skill Gap Analysis
  5. My Applications
"""

import streamlit as st
from utils import data_handler as db
from utils import matching
from utils import ui_components as ui

# All skills available for multiselect
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

BRANCHES = [
    "Computer Science", "Information Technology", "Electronics",
    "Electrical", "Mechanical", "Civil", "MCA", "BCA", "Other"
]

YEARS = ["1st Year", "2nd Year", "3rd Year", "4th Year", "Post Graduate"]


# ─── Auth ──────────────────────────────────────────────────────────────────────

def show_auth():
    """Show Login / Register tabs for students."""
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        show_login()

    with tab2:
        show_register()


def show_login():
    st.subheader("Student Login")
    email    = st.text_input("Email", key="s_login_email")
    password = st.text_input("Password", type="password", key="s_login_pass")

    if st.button("Login", key="s_login_btn", type="primary"):
        if not email or not password:
            st.error("Please fill in all fields.")
            return
        student = db.get_student_by_email(email)
        if student and student["password"] == password:
            st.session_state["student"] = student
            st.success(f"Welcome back, {student['name']}! 🎉")
            st.rerun()
        else:
            st.error("Invalid email or password.")


def show_register():
    st.subheader("Create Student Account")

    col1, col2 = st.columns(2)
    with col1:
        name   = st.text_input("Full Name*", key="s_reg_name")
        email  = st.text_input("Email*", key="s_reg_email")
        branch = st.selectbox("Branch*", BRANCHES, key="s_reg_branch")
    with col2:
        year     = st.selectbox("Year*", YEARS, key="s_reg_year")
        password = st.text_input("Password*", type="password", key="s_reg_pass")
        domain   = st.selectbox("Preferred Domain*", DOMAINS, key="s_reg_domain")

    skills   = st.multiselect("Your Skills*", ALL_SKILLS, key="s_reg_skills")
    projects = st.text_area("Projects (brief description)", key="s_reg_projects",
                             placeholder="E.g. Built a movie recommender using collaborative filtering...")
    bio      = st.text_area("Short Bio", key="s_reg_bio",
                             placeholder="Tell companies a little about yourself...")

    if st.button("Create Account", key="s_reg_btn", type="primary"):
        if not all([name, email, password, branch, year, skills]):
            st.error("Please fill in all required fields (*).")
            return
        if db.get_student_by_email(email):
            st.error("An account with this email already exists.")
            return

        new_student = {
            "name": name, "email": email, "password": password,
            "branch": branch, "year": year, "skills": skills,
            "projects": projects, "preferred_domain": domain, "bio": bio
        }
        student = db.add_student(new_student)
        st.session_state["student"] = student
        st.success("Account created successfully! 🎉")
        st.rerun()


# ─── Main Student Dashboard ────────────────────────────────────────────────────

def show_dashboard():
    student = st.session_state["student"]

    # Sidebar navigation
    st.sidebar.markdown(f"### 👤 {student['name']}")
    st.sidebar.caption(f"{student['branch']} • {student['year']}")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "Navigate",
        ["🏠 Dashboard", "💼 Internships", "📊 Skill Gap", "📁 My Applications", "✏️ Edit Profile"],
        key="student_menu"
    )

    if st.sidebar.button("🚪 Logout", key="s_logout"):
        del st.session_state["student"]
        st.rerun()

    # Route to page
    if menu == "🏠 Dashboard":
        show_student_home(student)
    elif menu == "💼 Internships":
        show_internships(student)
    elif menu == "📊 Skill Gap":
        show_skill_gap(student)
    elif menu == "📁 My Applications":
        show_my_applications(student)
    elif menu == "✏️ Edit Profile":
        show_edit_profile(student)


# ─── Dashboard Home ────────────────────────────────────────────────────────────

def show_student_home(student):
    ui.page_header(f"Welcome, {student['name']}! 👋",
                   "Here's your internship journey at a glance.")

    internships  = db.get_all_internships()
    applications = db.get_applications_by_student(student["id"])
    scored       = matching.get_recommended_internships(student["skills"], internships)
    top_match    = scored[0]["match_result"]["score"] if scored else 0

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ui.info_card("Skills", str(len(student["skills"])), "🛠")
    with col2:
        ui.info_card("Open Internships", str(len(internships)), "💼")
    with col3:
        ui.info_card("Applications", str(len(applications)), "📤")
    with col4:
        ui.info_card("Best Match", f"{top_match}%", "🎯")

    st.markdown("---")

    # Profile snapshot
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown("#### 🧑‍💻 Your Profile")
        st.write(f"**Branch:** {student['branch']}")
        st.write(f"**Year:** {student['year']}")
        st.write(f"**Domain:** {student['preferred_domain']}")
        if student.get("bio"):
            st.write(f"**Bio:** {student['bio']}")

    with col_b:
        st.markdown("#### 🛠 Your Skills")
        ui.skill_pills(student["skills"])

        if student.get("projects"):
            st.markdown("#### 🚀 Projects")
            st.info(student["projects"])

    st.markdown("---")

    # Top 3 recommendations preview
    st.markdown("#### 🔥 Top Internship Matches")
    for item in scored[:3]:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{item['role']}** — {item['company_name']}")
        with col2:
            ui.show_match_badge(item["match_result"]["score"])
        with col3:
            st.write(f"₹{item['stipend']:,}/mo")
        st.markdown("---")


# ─── Internship Recommendations ────────────────────────────────────────────────

def show_internships(student):
    ui.page_header("💼 Recommended Internships",
                   "Sorted by match score — best fits shown first.")

    internships = db.get_all_internships()
    if not internships:
        st.info("No internships available right now. Check back soon!")
        return

    # Filter sidebar controls
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        domain_filter = st.multiselect("Domain", list({i["domain"] for i in internships}))
        min_score     = st.slider("Minimum Match %", 0, 100, 0, step=10)
        st.markdown("---")

    scored = matching.get_recommended_internships(student["skills"], internships)

    # Apply filters
    if domain_filter:
        scored = [s for s in scored if s["domain"] in domain_filter]
    if min_score:
        scored = [s for s in scored if s["match_result"]["score"] >= min_score]

    if not scored:
        st.warning("No internships match your current filters.")
        return

    # Bar chart of match scores
    import pandas as pd
    chart_data = pd.DataFrame({
        "Internship": [f"{s['role']} @ {s['company_name']}" for s in scored],
        "Match %": [s["match_result"]["score"] for s in scored]
    })
    st.bar_chart(chart_data.set_index("Internship"))

    st.markdown("---")

    # Listing cards
    for item in scored:
        already = db.has_applied(student["id"], item["id"])
        clicked = ui.internship_card(
            internship=item,
            match_result=item["match_result"],
            show_apply_btn=True,
            already_applied=already
        )
        if clicked:
            db.add_application(student["id"], item["id"], item["match_result"]["score"])
            st.success(f"✅ Applied to **{item['role']}** at **{item['company_name']}**!")
            st.rerun()


# ─── Skill Gap Analysis ────────────────────────────────────────────────────────

def show_skill_gap(student):
    ui.page_header("📊 Skill Gap Analysis",
                   "See which skills you need to land your dream internship.")

    internships = db.get_all_internships()
    if not internships:
        st.info("No internships to analyse yet.")
        return

    # Select internship to analyse
    options = {f"{i['role']} @ {i['company_name']}": i for i in internships}
    choice  = st.selectbox("Select an Internship to Analyse", list(options.keys()))
    intern  = options[choice]
    result  = matching.calculate_match_score(student["skills"], intern["required_skills"])

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        ui.show_match_badge(result["score"])
    with col2:
        st.metric("✅ Skills Matched", f"{len(result['matched'])} / {result['total_required']}")
    with col3:
        st.metric("❌ Skills Missing", str(len(result["missing"])))

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### ✅ Skills You Have")
        if result["matched"]:
            ui.skill_pills(result["matched"], color="#22c55e")
        else:
            st.warning("None of your skills match this role.")

    with col_b:
        st.markdown("#### 🔴 Skills You Need")
        if result["missing"]:
            ui.missing_skill_pills(result["missing"])
            st.caption("Consider adding these to your learning roadmap!")
        else:
            st.success("🎉 You have all the required skills!")

    st.markdown("---")

    # Skill gap learning tips
    if result["missing"]:
        st.markdown("#### 📚 Quick Learning Resources")
        tips = {
            "Machine Learning": "Coursera ML by Andrew Ng, fast.ai",
            "React": "React docs (react.dev), Scrimba React course",
            "Docker": "Play With Docker (labs.play-with-docker.com)",
            "SQL": "SQLZoo, Mode Analytics SQL Tutorial",
            "Python": "Python.org official tutorial, Automate the Boring Stuff",
            "Power BI": "Microsoft Learn — Power BI learning path",
        }
        for skill in result["missing"]:
            tip = tips.get(skill, f"Search: 'Learn {skill} for beginners' on YouTube or Coursera")
            st.markdown(f"- **{skill}** → {tip}")

    # Visual progress bar
    st.markdown("---")
    st.markdown("#### 🎯 Match Progress")
    st.progress(result["score"] / 100, text=f"{result['score']}% complete")


# ─── My Applications ───────────────────────────────────────────────────────────

def show_my_applications(student):
    ui.page_header("📁 My Applications", "Track all your internship applications.")

    apps = db.get_applications_by_student(student["id"])

    if not apps:
        st.info("You haven't applied to any internships yet. Visit the Internships tab to apply!")
        return

    import pandas as pd
    rows = []
    for app in apps:
        intern = db.get_internship_by_id(app["internship_id"])
        if intern:
            rows.append({
                "Role": intern["role"],
                "Company": intern["company_name"],
                "Domain": intern["domain"],
                "Stipend (₹)": intern["stipend"],
                "Match Score": f"{app['match_score']}%",
                "Applied On": app["applied_date"],
                "Status": app["status"]
            })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    # Score chart
    if rows:
        st.markdown("#### 📊 Your Match Scores")
        score_data = pd.DataFrame({
            "Internship": [r["Role"] for r in rows],
            "Match %": [float(r["Match Score"].replace("%", "")) for r in rows]
        })
        st.bar_chart(score_data.set_index("Internship"))


# ─── Edit Profile ──────────────────────────────────────────────────────────────

def show_edit_profile(student):
    ui.page_header("✏️ Edit Profile", "Keep your profile up to date to get better matches.")

    col1, col2 = st.columns(2)
    with col1:
        name   = st.text_input("Full Name", value=student["name"])
        branch = st.selectbox("Branch", BRANCHES, index=BRANCHES.index(student["branch"]) if student["branch"] in BRANCHES else 0)
        domain = st.selectbox("Preferred Domain", DOMAINS, index=DOMAINS.index(student["preferred_domain"]) if student["preferred_domain"] in DOMAINS else 0)
    with col2:
        year   = st.selectbox("Year", YEARS, index=YEARS.index(student["year"]) if student["year"] in YEARS else 0)
        email  = st.text_input("Email", value=student["email"], disabled=True)

    # Skills multiselect — default to current skills
    default_skills = [s for s in student["skills"] if s in ALL_SKILLS]
    skills = st.multiselect("Skills", ALL_SKILLS, default=default_skills)

    projects = st.text_area("Projects", value=student.get("projects", ""))
    bio      = st.text_area("Bio", value=student.get("bio", ""))

    if st.button("💾 Save Changes", type="primary"):
        updated = {
            "name": name, "branch": branch, "year": year,
            "skills": skills, "projects": projects,
            "preferred_domain": domain, "bio": bio
        }
        db.update_student(student["id"], updated)
        st.session_state["student"].update(updated)
        st.success("Profile updated successfully! ✅")
        st.rerun()


# ─── Entry Point ───────────────────────────────────────────────────────────────

def render():
    if "student" not in st.session_state:
        show_auth()
    else:
        show_dashboard()
