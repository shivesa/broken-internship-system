"""
utils/ui_components.py
-----------------------
Reusable UI helper functions for the Streamlit app.
These keep individual page files clean and DRY.
"""

import streamlit as st


def show_match_badge(score: float) -> None:
    """Render a colored match score badge."""
    if score >= 80:
        color, emoji = "#22c55e", "🌟"
    elif score >= 60:
        color, emoji = "#f59e0b", "👍"
    elif score >= 40:
        color, emoji = "#f97316", "⚡"
    else:
        color, emoji = "#ef4444", "❌"

    st.markdown(
        f"""
        <div style="display:inline-block; background:{color}22;
                    border:2px solid {color}; border-radius:8px;
                    padding:6px 16px; font-weight:700; color:{color};
                    font-size:1.1rem;">
            {emoji} {score}% Match
        </div>
        """,
        unsafe_allow_html=True,
    )


def skill_pills(skills: list, color: str = "#6366f1") -> None:
    """Render a list of skills as colored pills."""
    pills_html = " ".join(
        f'<span style="background:{color}22; color:{color}; border:1px solid {color}; '
        f'border-radius:20px; padding:3px 12px; font-size:0.85rem; margin:2px; '
        f'display:inline-block;">{s}</span>'
        for s in skills
    )
    st.markdown(pills_html, unsafe_allow_html=True)


def missing_skill_pills(skills: list) -> None:
    """Render missing skills as red pills."""
    if not skills:
        return
    skill_pills(skills, color="#ef4444")


def section_header(title: str, subtitle: str = "") -> None:
    """Render a styled section header."""
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")


def info_card(title: str, value: str, icon: str = "📌", bg: str = "#f8fafc") -> None:
    """Render a small stat/info card."""
    st.markdown(
        f"""
        <div style="background:{bg}; border-radius:10px; padding:16px 20px;
                    border-left:4px solid #6366f1; margin-bottom:8px;">
            <div style="font-size:0.8rem; color:#64748b;">{icon} {title}</div>
            <div style="font-size:1.2rem; font-weight:700; color:#1e293b;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def internship_card(internship: dict, match_result: dict = None, show_apply_btn: bool = False, already_applied: bool = False) -> bool:
    """
    Render an internship listing card.
    Returns True if user clicked Apply, False otherwise.
    """
    applied = False
    with st.container():
        st.markdown(
            f"""
            <div style="border:1px solid #e2e8f0; border-radius:12px; padding:20px;
                        margin-bottom:16px; background:#ffffff; box-shadow:0 1px 3px #0001;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h4 style="margin:0; color:#1e293b;">🏢 {internship['role']}</h4>
                        <p style="margin:4px 0; color:#6366f1; font-weight:600;">{internship['company_name']}</p>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:#f0fdf4; color:#16a34a; border:1px solid #86efac;
                                     padding:4px 12px; border-radius:20px; font-size:0.85rem;">
                            ₹{internship['stipend']:,}/month
                        </span>
                    </div>
                </div>
                <div style="margin-top:10px; color:#475569; font-size:0.9rem;">
                    📍 {internship['location']} &nbsp;|&nbsp;
                    ⏱ {internship['duration']} &nbsp;|&nbsp;
                    🏷 {internship['domain']}
                </div>
                <p style="margin-top:10px; color:#64748b; font-size:0.9rem;">{internship['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show match info if provided
        if match_result:
            col1, col2 = st.columns([1, 2])
            with col1:
                show_match_badge(match_result["score"])
            with col2:
                if match_result["missing"]:
                    st.markdown("**🔴 Missing Skills:**")
                    missing_skill_pills(match_result["missing"])
                else:
                    st.success("✅ You have all required skills!")

            # Required skills
            st.markdown("**Required Skills:**")
            skill_pills(internship["required_skills"])

        # Apply button
        if show_apply_btn:
            st.markdown(" ")
            if already_applied:
                st.info("✅ Already Applied")
            else:
                if st.button(f"Apply Now →", key=f"apply_{internship['id']}"):
                    applied = True

        st.markdown("&nbsp;")
    return applied


def page_header(title: str, subtitle: str = "") -> None:
    """Full-width page header banner."""
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    padding: 28px 32px; border-radius: 14px; margin-bottom: 24px; color:white;">
            <h1 style="margin:0; font-size:2rem;">{title}</h1>
            <p style="margin:6px 0 0; opacity:0.85;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
