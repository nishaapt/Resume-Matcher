import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from resume_parser import parse_resume
from skill_extractor import extract_skills
from matcher import compute_match_score
from semantic_matcher import compute_semantic_score
from skill_gap import find_missing_skills
from job_matcher import rank_jobs
from skill_resources import get_resources_for_skills
from report_generator import generate_report

st.set_page_config(page_title="ResumeIntel", layout="wide", page_icon="🧭")

# ---------- Custom CSS: forced light theme ----------
st.markdown("""
<style>
    html, body, .main, .stApp { background-color: #f6f7fb !important; color: #1e1b4b !important; }
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3, h4, p, span, label, .stMarkdown { color: #1e1b4b !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #eceefb; }
    [data-testid="stSidebar"] * { color: #1e1b4b !important; }
    .card {
        background: white !important; border-radius: 16px; padding: 1.4rem 1.6rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #eceefb;
        margin-bottom: 1.2rem;
    }
    .card * { color: #1e1b4b !important; }
    .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .badge { background: #eef0fd; color: #6366f1 !important; padding: 5px 14px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }
    .job-card {
        background: white !important; border-radius: 12px; padding: 0.9rem 1.1rem; border: 1px solid #eceefb;
        margin-bottom: 0.6rem; display: flex; justify-content: space-between; align-items: center;
    }
    .job-card * { color: #1e1b4b !important; }
    .job-title { font-weight: 700; color: #1e1b4b !important; }
    .job-sub { color: #888 !important; font-size: 0.8rem; }
    .match-pill { background: #e6f9f0; color: #0f9d58 !important; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; }
    .skill-row { display: flex; justify-content: space-between; padding: 0.55rem 0; border-bottom: 1px solid #f0f0f5; font-size: 0.92rem; color: #1e1b4b !important; }
    .mini-card {
        background: white !important; border-radius: 12px; padding: 1rem; border: 1px solid #eceefb;
        text-align: center; margin-bottom: 0.5rem;
    }
    .mini-card * { color: #1e1b4b !important; }
    .gauge-wrap { display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .action-box { background: #f5f6ff !important; border-radius: 12px; padding: 1rem; margin-top: 0.5rem; }
    .action-box * { color: #1e1b4b !important; }

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: #ffffff !important; color: #1e1b4b !important; border: 1px solid #dcdfef !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important; border: 1px dashed #c7cbf0 !important;
    }
    [data-testid="stFileUploaderDropzone"] * { color: #1e1b4b !important; }

    .stButton>button {
        background-color: #6366f1 !important; color: white !important; border-radius: 8px; font-weight: 600; border: none;
    }
    .stButton>button:hover { background-color: #4f46e5 !important; }
    .stButton>button p { color: white !important; }

    [data-testid="stExpander"] { background-color: white !important; border: 1px solid #eceefb !important; border-radius: 10px; }
    [data-testid="stExpander"] * { color: #1e1b4b !important; }
</style>
""", unsafe_allow_html=True)


def circular_gauge_html(score, label="Resume Health"):
    color = "#0f9d58" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
    return f"""
    <div class="gauge-wrap">
        <div style="width:160px;height:160px;border-radius:50%;
            background: conic-gradient({color} {score * 3.6}deg, #eef0fb 0deg);
            display:flex;align-items:center;justify-content:center;">
            <div style="width:128px;height:128px;border-radius:50%;background:white;
                display:flex;flex-direction:column;align-items:center;justify-content:center;">
                <span style="font-size:1.8rem;font-weight:700;color:#1e1b4b;">{int(score)}</span>
                <span style="font-size:0.75rem;color:#888;">/100</span>
            </div>
        </div>
        <p style="margin-top:0.6rem;font-weight:600;color:#1e1b4b;">{label}</p>
    </div>
    """


def sub_score_bar(label, value):
    st.markdown(f"""
        <div style="margin-bottom:0.6rem;">
            <div style="display:flex;justify-content:space-between;font-size:0.85rem;color:#333;">
                <span>{label}</span><span>{value}%</span>
            </div>
            <div style="background:#eceefb;border-radius:6px;height:8px;">
                <div style="background:#6366f1;width:{min(value,100)}%;height:8px;border-radius:6px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 🧭 ResumeIntel")
    st.caption("Your Resume. More Opportunities.")
    name = st.text_input("Your name", value="there", label_visibility="collapsed", placeholder="Your name")
    st.write("")
    st.radio("Navigation", ["🏠 Home", "📄 My Resume", "💼 Job Matches", "🎯 Skill Gaps"], label_visibility="collapsed")
    st.write("")
    st.markdown('<div class="action-box">', unsafe_allow_html=True)
    st.markdown("**✨ AI Career Copilot**")
    st.caption("Ask anything, get personalized guidance.")
    question = st.text_input("Ask a question", label_visibility="collapsed", placeholder="e.g. What should I learn next?")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(f"""
    <div class="header-row">
        <div>
            <h2 style="margin-bottom:0;">Hey {name or 'there'} 👋</h2>
            <p style="color:#888;margin-top:0;">Let's turn your resume into more interviews.</p>
        </div>
        <div><span class="badge">✨ AI Powered</span></div>
    </div>
""", unsafe_allow_html=True)

# ---------- Input ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")
with col1:
    uploaded_file = st.file_uploader("Resume (PDF or DOCX)", type=["pdf", "docx"])
with col2:
    job_description = st.text_area("Job Description", height=120, placeholder="Paste the job description here...")
analyze = st.button("Analyze Resume", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------- Analysis ----------
if analyze:
    if uploaded_file is None or not job_description.strip():
        st.error("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing..."):
            temp_path = os.path.join("data", "temp_" + uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            resume_text = parse_resume(temp_path)
            resume_skills = extract_skills(resume_text)
            keyword_score = compute_match_score(resume_text, job_description)
            semantic_score = compute_semantic_score(resume_text, job_description)
            required, missing = find_missing_skills(resume_skills, job_description)
            job_rankings = rank_jobs(resume_text)
            os.remove(temp_path)

        skills_strength = round((len(resume_skills) / max(len(resume_skills) + len(missing), 1)) * 100, 1)
        project_mentions = resume_text.lower().count("project")
        impact_score = min(100, 40 + project_mentions * 8)
        experience_score = min(100, 50 + resume_text.lower().count("experience") * 10)

        main_col, side_col = st.columns([2, 1], gap="large")

        with main_col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            g1, g2 = st.columns([1, 2])
            with g1:
                st.markdown(circular_gauge_html(semantic_score, "Resume Health"), unsafe_allow_html=True)
            with g2:
                st.markdown("**Score Breakdown**")
                sub_score_bar("ATS Readability", keyword_score)
                sub_score_bar("Skills Strength", skills_strength)
                sub_score_bar("Experience", experience_score)
                sub_score_bar("Keywords", keyword_score)
                sub_score_bar("Impact of Projects", impact_score)
                st.button("✨ Improve my resume", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🎯 AI Job Finder")
            st.caption(f"Based on your resume, we found {len(job_rankings)} roles you're likely to qualify for.")
            for job in job_rankings:
                st.markdown(f"""
                    <div class="job-card">
                        <div>
                            <div class="job-title">{job['title']}</div>
                            <div class="job-sub">Sample role · Remote</div>
                        </div>
                        <div class="match-pill">{job['score']}% Match</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ⭐ Recommended for You")
            rec_cols = st.columns(len(job_rankings))
            for c, job in zip(rec_cols, job_rankings):
                with c:
                    st.markdown(f"""
                        <div class="mini-card">
                            <div style="font-weight:700;">{job['title']}</div>
                            <div class="match-pill" style="display:inline-block;margin-top:6px;">{job['score']}%</div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with side_col:
            top_missing = missing[0] if missing else None
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 💡 Your Next Best Action")
            if top_missing:
                st.write(f"**Add {top_missing.title()} to your skill profile**")
                st.caption("Closing this gap could improve your match rate on several roles.")
            else:
                st.success("You're covering all detected required skills!")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 🧩 Your Skill Gap")
            st.caption("For this job description")
            for s in required:
                freq = job_description.lower().count(s)
                demand = "High" if freq >= 2 else "Medium"
                have = s in resume_skills
                mark = '<span style="color:#0f9d58;">✔</span>' if have else '<span style="color:#ef4444;">✘</span>'
                st.markdown(f'<div class="skill-row"><span>{s.title()}</span><span>{demand}</span><span>{mark}</span></div>', unsafe_allow_html=True)
            if missing:
                st.button("Generate 30-day learning plan →", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### ✨ AI Resume Tailoring")
            st.caption("Tailor your resume for this specific job to increase your match rate.")
            st.button("Try it now →", use_container_width=True, disabled=True)
            st.caption("Coming soon")
            st.markdown('</div>', unsafe_allow_html=True)

        if missing:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 📚 Recommended Resources")
            resources = get_resources_for_skills(missing)
            for skill, info in resources.items():
                with st.expander(skill.title()):
                    st.write(f"**Tip:** {info['tip']}")
                    for r in info["resources"]:
                        st.write(f"- {r}")
            st.markdown('</div>', unsafe_allow_html=True)

        report_path = generate_report(keyword_score, resume_skills, missing, job_rankings)
        with open(report_path, "rb") as f:
            st.download_button(
                "📥 Download Full Report (PDF)",
                data=f,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )