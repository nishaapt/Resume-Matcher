import re

# A starter list of common tech/data skills - we'll expand this later
SKILL_KEYWORDS = [
    "python", "sql", "java", "c++", "javascript",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "machine learning", "deep learning", "data analysis",
    "data visualization", "power bi", "tableau",
    "nlp", "generative ai", "git", "github", "excel",
    "jupyter notebook", "vs code", "kaggle",
    "feature engineering", "model evaluation", "eda"
]


def extract_skills(resume_text):
    """Find which known skills appear in the resume text."""
    text_lower = resume_text.lower()
    found_skills = []

    for skill in SKILL_KEYWORDS:
        # Use word boundaries so "sql" doesn't match inside another word
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from resume_parser import parse_resume

    sample_path = "../data/sample_resume.pdf"
    if os.path.exists(sample_path):
        text = parse_resume(sample_path)
        skills = extract_skills(text)
        print("Skills found:")
        for s in skills:
            print(" -", s)
    else:
        print(f"No test file found at {sample_path}")