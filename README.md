# AI_JOB_SKILL_ANALYZER
An AI-based job skill analyzer that extracts core skills from resumes and job descriptions, computes match percentage, and provides a structured learning roadmap using Google Gemini AI.
https://aijobskillanalyzer-gvbjsm7rpbwu4rsfskrnmq.streamlit.app/

Overall Architecture:-
                ┌──────────────────────┐
                │       USER           │
                │                      │
                │  Upload Resume PDF   │
                │  Enter Job Description│
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   STREAMLIT UI       │
                │   (Frontend)         │
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌─────────────────┐       ┌─────────────────┐
     │ Resume PDF      │       │ Job Description │
     │ Text Extraction │       │ Text Processing │
     │    PyPDF2       │       │                 │
     └────────┬────────┘       └────────┬────────┘
              │                         │
              └────────────┬────────────┘
                           ▼
                ┌──────────────────────┐
                │  Skill Extraction    │
                │                      │
                │ Core Skills +        │
                │ Synonym Handling     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Skill Matching       │
                │                      │
                │ Matched Skills       │
                │ Missing Skills       │
                │ Match Percentage     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Google Gemini     │
                │       AI API         │
                │                      │
                │ Learning Roadmap     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │      RESULTS         │
                │                      │
                │ Match %              │
                │ Matched Skills       │
                │ Missing Skills       │
                │ AI Learning Roadmap  │
                └──────────────────────┘
