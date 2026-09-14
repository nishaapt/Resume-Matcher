import sys
import os
sys.path.append(os.path.dirname(__file__))

from resume_parser import parse_resume
from skill_extractor import extract_skills, SKILL_KEYWORDS


def find_missing_skills(resume_skills, job_description):
    """Find which known skills appear in the job description but not in the resume."""
    job_text_lower = job_description.lower()
    resume_skills_set = set(resume_skills)

    required_skills = extract_skills(job_description)
    missing_skills = [s for s in required_skills if s not in resume_skills_set]

    return required_skills, missing_skills


if __name__ == "__main__":
    sample_path = "../data/sample_resume.pdf"

    sample_job_description = """
    We are looking for a Data Science Intern with strong skills in Python, SQL,
    Pandas, NumPy, TensorFlow, and Scikit-learn. Experience with deep learning,
    natural language processing (NLP), and cloud platforms is a big plus.
    Familiarity with Git, GitHub, and Excel is expected.
    """

    if os.path.exists(sample_path):
        resume_text = parse_resume(sample_path)
        resume_skills = extract_skills(resume_text)

        required, missing = find_missing_skills(resume_skills, sample_job_description)

        print("Your skills:", resume_skills)
        print("\nJob requires:", required)
        print("\nSkills you're missing:", missing if missing else "None - great match!")
    else:
        print(f"No test file found at {sample_path}")