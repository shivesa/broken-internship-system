"""
utils/data_handler.py
---------------------
Handles all read/write operations for JSON-based data storage.
All data is stored as flat JSON files in the /data directory.
"""

import json
import os
import uuid
from datetime import date

# ─── Path Configuration ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

STUDENTS_FILE     = os.path.join(DATA_DIR, "students.json")
COMPANIES_FILE    = os.path.join(DATA_DIR, "companies.json")
INTERNSHIPS_FILE  = os.path.join(DATA_DIR, "internships.json")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")


# ─── Generic Helpers ───────────────────────────────────────────────────────────

def load_json(filepath: str) -> list:
    """Load and return data from a JSON file. Returns empty list if file missing."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath: str, data: list) -> None:
    """Save data to a JSON file with pretty formatting."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def generate_id(prefix: str) -> str:
    """Generate a short unique ID like S-3f2a, C-9b1c, etc."""
    return f"{prefix}-{uuid.uuid4().hex[:4].upper()}"


# ─── Student Operations ────────────────────────────────────────────────────────

def get_all_students() -> list:
    return load_json(STUDENTS_FILE)


def get_student_by_email(email: str) -> dict | None:
    students = get_all_students()
    for s in students:
        if s["email"].lower() == email.lower():
            return s
    return None


def get_student_by_id(student_id: str) -> dict | None:
    students = get_all_students()
    for s in students:
        if s["id"] == student_id:
            return s
    return None


def add_student(student_data: dict) -> dict:
    """Add a new student and return it with generated ID."""
    students = get_all_students()
    student_data["id"] = generate_id("S")
    students.append(student_data)
    save_json(STUDENTS_FILE, students)
    return student_data


def update_student(student_id: str, updated_data: dict) -> bool:
    """Update an existing student record by ID."""
    students = get_all_students()
    for i, s in enumerate(students):
        if s["id"] == student_id:
            students[i].update(updated_data)
            save_json(STUDENTS_FILE, students)
            return True
    return False


# ─── Company Operations ────────────────────────────────────────────────────────

def get_all_companies() -> list:
    return load_json(COMPANIES_FILE)


def get_company_by_email(email: str) -> dict | None:
    companies = get_all_companies()
    for c in companies:
        if c["email"].lower() == email.lower():
            return c
    return None


def get_company_by_id(company_id: str) -> dict | None:
    companies = get_all_companies()
    for c in companies:
        if c["id"] == company_id:
            return c
    return None


def add_company(company_data: dict) -> dict:
    """Add a new company and return it with generated ID."""
    companies = get_all_companies()
    company_data["id"] = generate_id("C")
    companies.append(company_data)
    save_json(COMPANIES_FILE, companies)
    return company_data


# ─── Internship Operations ─────────────────────────────────────────────────────

def get_all_internships() -> list:
    return load_json(INTERNSHIPS_FILE)


def get_internships_by_company(company_id: str) -> list:
    return [i for i in get_all_internships() if i["company_id"] == company_id]


def get_internship_by_id(internship_id: str) -> dict | None:
    for i in get_all_internships():
        if i["id"] == internship_id:
            return i
    return None


def add_internship(internship_data: dict) -> dict:
    """Add a new internship posting."""
    internships = get_all_internships()
    internship_data["id"] = generate_id("I")
    internship_data["posted_date"] = str(date.today())
    internships.append(internship_data)
    save_json(INTERNSHIPS_FILE, internships)
    return internship_data


# ─── Application Operations ────────────────────────────────────────────────────

def get_all_applications() -> list:
    return load_json(APPLICATIONS_FILE)


def get_applications_by_student(student_id: str) -> list:
    return [a for a in get_all_applications() if a["student_id"] == student_id]


def get_applications_by_internship(internship_id: str) -> list:
    return [a for a in get_all_applications() if a["internship_id"] == internship_id]


def has_applied(student_id: str, internship_id: str) -> bool:
    """Check if a student has already applied to an internship."""
    apps = get_all_applications()
    return any(
        a["student_id"] == student_id and a["internship_id"] == internship_id
        for a in apps
    )


def add_application(student_id: str, internship_id: str, match_score: float) -> dict:
    """Submit a new internship application."""
    applications = get_all_applications()
    application = {
        "id": generate_id("A"),
        "student_id": student_id,
        "internship_id": internship_id,
        "match_score": match_score,
        "applied_date": str(date.today()),
        "status": "Under Review"
    }
    applications.append(application)
    save_json(APPLICATIONS_FILE, applications)
    return application
