import streamlit as st
import PyPDF2
from google import genai
import time
import re
import os

# ---------------- GEMINI SETUP ----------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1"}
)

MODEL = "models/gemini-2.5-flash"

# ---------------- CORE SKILLS ----------------
CORE_SKILLS = [
    "oop","dsa","dbms","sql","os","networking",
    "java","python","c++","c",
    "html","css","javascript",
    "nmap","wireshark","linux","git"
]

# ---------------- SYNONYMS ----------------
SKILL_SYNONYMS = {
    "dsa": ["data structure", "data structures", "data structure and algorithm"],
    "dbms": ["database", "databases", "backend database"],
    "sql": ["sql"],
    "oop": ["object oriented", "object-oriented", "oop"],
    "networking": ["network", "network security"],
    "javascript": ["js"]
}

# ---------------- EXPANSION MAP ----------------
EXPANSION_MAP = {
    "dsa": ["searching","sorting","hashmaps","trees","graphs","dynamic programming"],
    "sql": ["sql queries","joins","relational schemas"],
    "dbms": ["normalization","schema design"],
    "oop": ["classes","inheritance","polymorphism"],
    "networking": ["tcp/ip","protocols"],
    "os": ["process management","memory management"]
}

# ---------------- PDF TEXT ----------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    return text.lower().replace("(", " ").replace(")", " ")

# ---------------- TOKENIZE ----------------
def tokenize(text):
    return re.findall(r'\b[a-zA-Z0-9+#]+\b', text.lower())

# ---------------- SKILL EXTRACTION ----------------
def extract_core_skills(text):
    text = clean_text(text)
    words = tokenize(text)
    found = set()

    for skill in CORE_SKILLS:

        # exact match
        if skill in words:
            found.add(skill)
            continue

        # synonym match
        if skill in SKILL_SYNONYMS:
            for phrase in SKILL_SYNONYMS[skill]:
                if phrase in text:
                    found.add(skill)

    return list(found)

# ---------------- EXPAND SKILLS ----------------
def expand_skills(skills):
    expanded = []
    for s in skills:
        if s in EXPANSION_MAP:
            expanded.extend(EXPANSION_MAP[s])
    return list(set(expanded))

# ---------------- MATCH ----------------
def calculate_match(resume_skills, job_skills):
    if not job_skills:
        return 0, [], []

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    percent = (len(matched) / len(job_set)) * 100

    return round(percent, 2), matched, missing

# ---------------- AI ROADMAP ----------------
def ai_roadmap(matched, missing, expanded_missing, job_text):
    try:
        time.sleep(1)

        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
You are an expert career mentor.

Matched Skills: {matched}
Missing Skills: {missing}
Detailed Topics: {expanded_missing}

Job Description:
{job_text}

Create a structured learning roadmap.

Rules:
- Improve existing skills
- Cover missing skills step-by-step
- Include practical learning
- 5 to 6 steps

Format:
Step 1:
Step 2:
Step 3:
"""
        )

        if response and response.text:
            return response.text.strip()

    except:
        pass

    # -------- FALLBACK --------
    roadmap = []

    if matched:
        roadmap.append(f"Step 1: Strengthen core skills: {', '.join(matched)}")

    if missing:
        roadmap.append(f"Step 2: Learn missing skills: {', '.join(missing)}")

    if expanded_missing:
        roadmap.append(f"Step 3: Focus on topics: {', '.join(expanded_missing[:4])}")

    roadmap.append("Step 4: Practice coding and real-world problems")
    roadmap.append("Step 5: Build projects using these skills")
    roadmap.append("Step 6: Prepare for interviews")

    return "\n".join(roadmap)

# ---------------- STREAMLIT UI ----------------
st.title("🤖 AI Job Skill Analyzer ")

file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if file and job:

        resume_text = extract_text_from_pdf(file)

        # Extract skills
        resume_core = extract_core_skills(resume_text)
        job_core = extract_core_skills(job)

        # Match
        match, matched, missing = calculate_match(resume_core, job_core)

        # Expand
        expanded_missing = expand_skills(missing)

        # Roadmap
        roadmap = ai_roadmap(matched, missing, expanded_missing, job)

        # OUTPUT
        st.subheader("📊 Results")
        st.write(f"Match Percentage: {match}%")

        st.write("✅ Matched Core Skills:", matched)
        st.write("❌ Missing Core Skills:", missing)

        st.subheader("💡 Learning Roadmap")
        st.write(roadmap)

    else:
        st.warning("Upload resume and job description")
