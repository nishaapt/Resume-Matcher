# 🧠 ResumeIntel — AI Resume Intelligence & Job Matching System

> 🚧 **Status: Under Active Development** — core features are working; more are being added regularly.

An AI-powered web app that analyzes your resume against a job description, scores your fit using both keyword and semantic (AI) matching, identifies skill gaps, and recommends how to close them — all in an interactive dashboard.

---

## ✨ Features

- **Resume Parsing** — extracts text from PDF and DOCX resumes
- **Skill Extraction** — detects known technical skills from resume text
- **Dual Match Scoring**
  - Keyword-based matching (TF-IDF + cosine similarity)
  - Semantic matching using sentence embeddings (`all-MiniLM-L6-v2`)
- **Skill Gap Analysis** — shows exactly which required skills are missing
- **Similar Job Matching** — ranks your resume against multiple sample job roles
- **Learning Resources** — curated tips and free resources per missing skill
- **30-Day Learning Plan** — auto-generated day-by-day plan to close skill gaps
- **PDF Report Export** — download a full analysis report
- **Interactive Dashboard** — built with Streamlit, styled with custom CSS

### 🔜 Planned / In Progress

- AI Career Copilot (chat-based Q&A on your results)
- "Improve my resume" guided flow
- Live deployment with a public demo link
- Real job postings via a live jobs API
- ATS resume quality scoring

---

## 🛠 Tech Stack

- **Language:** Python
- **Frontend/Dashboard:** Streamlit
- **NLP/ML:** scikit-learn (TF-IDF), sentence-transformers (semantic embeddings), spaCy
- **File Parsing:** PyPDF2, python-docx
- **Reporting:** fpdf2


---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/nishaapt/Resume-Matcher.git
cd Resume-Matcher
```

### 2. Create a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies
```bash
pip install streamlit pandas scikit-learn nltk spacy PyPDF2 python-docx sentence-transformers fpdf2
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📸 Screenshots

<img width="950" height="445" alt="image" src="https://github.com/user-attachments/assets/d2a27178-37ca-4fd6-b21f-6a338de22eb8" />
<img width="959" height="452" alt="image" src="https://github.com/user-attachments/assets/02fcdb7c-7448-4ee7-92a8-7d073767044e" />



## 👤 Author

**Nisha Patil**
AI & Data Science Undergraduate
[LinkedIn](https://www.linkedin.com/in/nisha-patil-3234a3371) · [GitHub](https://github.com/nishaapt)

---

## 📂 Project Structure
