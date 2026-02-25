# 🎯 InternMatch — Smart Internship Matching Platform

A Streamlit-based Hackathon project that fixes India's broken internship system
through transparent, skill-based matching between students and companies.

---

## 📁 Folder Structure

```
internship_platform/
│
├── app.py                     ← Main entry point (run this)
│
├── requirements.txt           ← Python dependencies
│
├── data/                      ← JSON-based storage (no database needed)
│   ├── students.json          ← Student profiles
│   ├── companies.json         ← Company profiles
│   ├── internships.json       ← Internship postings
│   └── applications.json      ← Student applications
│
├── pages/                     ← One file per role
│   ├── student_page.py        ← All student views
│   ├── company_page.py        ← All company views
│   └── admin_page.py          ← Admin analytics dashboard
│
└── utils/                     ← Helper modules
    ├── data_handler.py        ← All JSON read/write operations
    ├── matching.py            ← Core matching algorithm
    └── ui_components.py       ← Reusable UI widgets
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open in browser
The app will open automatically at `http://localhost:8501`

---

## 👤 Demo Credentials

### Students (login on Student Portal)
| Name | Email | Password |
|------|-------|----------|
| Priya Sharma | priya@example.com | priya123 |
| Rahul Verma | rahul@example.com | rahul123 |
| Ananya Iyer | ananya@example.com | ananya123 |
| Karan Mehta | karan@example.com | karan123 |
| Neha Gupta | neha@example.com | neha123 |

### Companies (login on Company Portal)
| Name | Email | Password |
|------|-------|----------|
| TechNova Solutions | technova@example.com | tech123 |
| WebWave Agency | webwave@example.com | web123 |
| DataBridge Analytics | databridge@example.com | data123 |

### Admin
- Password: `admin@123`

---

## 🧠 How the Matching Algorithm Works

```
match_score = (number of matching skills / total required skills) × 100
```

**Example:**
- Internship requires: `["Python", "ML", "Pandas", "NumPy", "Scikit-learn"]`
- Student has: `["Python", "ML", "Pandas", "SQL"]`
- Matched: `["Python", "ML", "Pandas"]` → 3 out of 5
- Score = (3/5) × 100 = **60%**
- Missing: `["NumPy", "Scikit-learn"]` → shown as skill gap

### Score Labels:
| Score | Label |
|-------|-------|
| 80–100% | 🌟 Excellent Match |
| 60–79% | 👍 Good Match |
| 40–59% | ⚡ Partial Match |
| 0–39% | ❌ Low Match |

If score < 70%, missing skills are shown so students can upskill.

---

## ✨ Features

### Student
- Register / Login
- View profile with skills
- Browse internships ranked by match score
- Filter by domain and minimum match %
- See match score with colored badge
- Skill Gap Analysis — see exactly which skills you're missing + learning tips
- Apply to internships (one-click)
- Track all applications with status

### Company
- Register / Login
- Post internship with required skills, stipend, duration, location
- View all posted internships
- See all applicants auto-ranked by match score
- Expandable candidate cards with skill breakdown

### Admin
- View all students, companies, internships, applications
- Skill frequency analysis
- Stipend distribution chart
- Match score distribution analysis

---

## 🛠 Technical Stack

| Layer | Technology |
|-------|------------|
| Frontend + Backend | Streamlit (Python) |
| Data Storage | JSON files |
| Matching Logic | Pure Python set operations |
| Charts | Streamlit native bar charts |
| Styling | Custom HTML/CSS in st.markdown |

---

## 💡 Hackathon Demo Tips

1. Start with the **Admin** view to show all pre-loaded data
2. Log in as **Priya Sharma** (ML student) → show her match with the ML Intern role (should be ~80%)
3. Switch to **TechNova** company view → show ranked applicants for ML Intern role
4. Show **Skill Gap** tab for Neha Gupta on the ML Intern role (she's missing several skills)
5. Register a new student live to demonstrate real-time JSON storage
