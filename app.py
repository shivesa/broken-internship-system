"""
app.py
======
Smart Internship Matching Platform
-----------------------------------
Entry point for the Streamlit application.

Run with:
    streamlit run app.py

Roles supported:
    • Student  — Browse and apply to internships, see match scores & skill gaps
    • Company  — Post internships, view ranked applicants
    • Admin    — Platform-wide analytics (password: admin@123)
"""

import streamlit as st

# ─── Page Config (must be the very first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="InternMatch — Smart Internship Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Imports (after set_page_config) ──────────────────────────────────────────
from modulesimport student_page, company_page, admin_page

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Clean font and background */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Hide default Streamlit menu & footer for cleaner demo look */
    #MainMenu {visibility: hidden;}
    footer     {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar — Role Selection ──────────────────────────────────────────────────

def show_sidebar_role_selector():
    """Show the platform branding and role selector in the sidebar."""
    st.sidebar.markdown("""
    <div style="text-align:center; padding: 16px 0 8px;">
        <h2 style="color:#6366f1; margin:0;">🎯 InternMatch</h2>
        <p style="color:#64748b; font-size:0.85rem; margin:4px 0 0;">
            India's Smart Internship Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # If a user is logged in, don't show role switcher
    if "student" in st.session_state:
        return "Student"
    if "company" in st.session_state:
        return "Company"
    if "admin" in st.session_state:
        return "Admin"

    st.sidebar.markdown("#### Select Your Role")
    role = st.sidebar.radio(
        "I am a...",
        ["🎓 Student", "🏢 Company", "🛠 Admin"],
        label_visibility="collapsed"
    )
    st.sidebar.markdown("---")
    return role.split(" ")[1]  # Strip emoji → "Student", "Company", "Admin"


# ─── Landing Page ─────────────────────────────────────────────────────────────

def show_landing():
    """Show hero landing section when no user is logged in."""
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px 20px;">
        <h1 style="font-size:3rem; color:#1e293b; margin-bottom:8px;">
            🎯 InternMatch
        </h1>
        <h3 style="color:#6366f1; margin:0 0 12px;">
            India's Smart Internship Matching Platform
        </h3>
        <p style="color:#64748b; font-size:1.1rem; max-width:600px; margin:0 auto 32px;">
            Fixing India's broken internship system — one skill-matched opportunity at a time.
            Students get transparent match scores. Companies get ranked candidates. Everyone wins.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#eff6ff; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size:2.5rem;">🎓</div>
            <h4 style="color:#3b82f6;">For Students</h4>
            <p style="color:#64748b; font-size:0.9rem;">
                Create your profile, discover internships ranked by match score,
                and identify your skill gaps instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#f0fdf4; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size:2.5rem;">🏢</div>
            <h4 style="color:#22c55e;">For Companies</h4>
            <p style="color:#64748b; font-size:0.9rem;">
                Post internships, receive applications, and see candidates
                auto-ranked by skill match — no manual screening needed.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#fefce8; border-radius:12px; padding:20px; text-align:center;">
            <div style="font-size:2.5rem;">📊</div>
            <h4 style="color:#f59e0b;">Transparent Matching</h4>
            <p style="color:#64748b; font-size:0.9rem;">
                Our skill-based algorithm shows exactly why you're a match —
                or what you need to learn to become one.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:32px; color:#94a3b8; font-size:0.9rem;">
        👈 Select your role from the sidebar to get started
    </div>
    """, unsafe_allow_html=True)


# ─── App Router ───────────────────────────────────────────────────────────────

def main():
    role = show_sidebar_role_selector()

    # If no one is logged in, show landing page + role-specific auth
    if role == "Student":
        # Show landing only if not logged in
        if "student" not in st.session_state:
            show_landing()
            st.markdown("---")
            st.markdown("### 🎓 Student Portal")
        student_page.render()

    elif role == "Company":
        if "company" not in st.session_state:
            show_landing()
            st.markdown("---")
            st.markdown("### 🏢 Company Portal")
        company_page.render()

    elif role == "Admin":
        if "admin" not in st.session_state:
            st.markdown("### 🛠 Admin Portal")
        admin_page.render()


if __name__ == "__main__":
    main()
