"""
utils/matching.py
-----------------
Core matching engine for the Smart Internship Platform.

Matching Formula:
  match_score = (matching_skills / total_required_skills) × 100

If match_score < 70%, we also return the list of missing skills
so students can see their "skill gap".
"""


def calculate_match_score(student_skills: list, required_skills: list) -> dict:
    """
    Compare student skills against internship requirements.

    Parameters:
        student_skills  : List of skills the student has (strings)
        required_skills : List of skills the internship requires (strings)

    Returns a dict:
        {
          "score"         : float  (0–100),
          "matched"       : list   (skills the student has),
          "missing"       : list   (skills the student lacks),
          "total_required": int
        }
    """
    if not required_skills:
        return {"score": 0, "matched": [], "missing": [], "total_required": 0}

    # Normalize to lowercase for case-insensitive comparison
    student_set  = {skill.strip().lower() for skill in student_skills}
    required_set = {skill.strip().lower() for skill in required_skills}

    matched_set = student_set & required_set
    missing_set = required_set - student_set

    score = (len(matched_set) / len(required_set)) * 100

    # Map back to original casing (use required_skills casing for display)
    matched_display = [s for s in required_skills if s.strip().lower() in matched_set]
    missing_display = [s for s in required_skills if s.strip().lower() in missing_set]

    return {
        "score"         : round(score, 1),
        "matched"       : matched_display,
        "missing"       : missing_display,
        "total_required": len(required_skills)
    }


def rank_students_for_internship(students: list, required_skills: list) -> list:
    """
    Rank a list of students by their match score for a given internship.

    Parameters:
        students        : List of student dicts (each must have a "skills" key)
        required_skills : List of required skills for the internship

    Returns:
        List of dicts sorted by match_score descending, each containing:
        { student_data + "match_result" }
    """
    ranked = []
    for student in students:
        result = calculate_match_score(student.get("skills", []), required_skills)
        ranked.append({**student, "match_result": result})

    # Sort by score descending
    ranked.sort(key=lambda x: x["match_result"]["score"], reverse=True)
    return ranked


def get_recommended_internships(student_skills: list, all_internships: list) -> list:
    """
    Score all internships for a student and return them sorted by match score.

    Returns:
        List of dicts: { internship_data + "match_result" }
    """
    scored = []
    for internship in all_internships:
        result = calculate_match_score(
            student_skills,
            internship.get("required_skills", [])
        )
        scored.append({**internship, "match_result": result})

    # Sort by score descending
    scored.sort(key=lambda x: x["match_result"]["score"], reverse=True)
    return scored


def get_score_label(score: float) -> tuple[str, str]:
    """
    Return a human-readable label and color for a given match score.

    Returns: (label, color_hex)
    """
    if score >= 80:
        return ("Excellent Match 🌟", "#22c55e")   # green
    elif score >= 60:
        return ("Good Match 👍", "#f59e0b")         # amber
    elif score >= 40:
        return ("Partial Match ⚡", "#f97316")      # orange
    else:
        return ("Low Match ❌", "#ef4444")           # red
