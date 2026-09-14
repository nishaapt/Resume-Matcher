import sys
import os
sys.path.append(os.path.dirname(__file__))

from matcher import compute_match_score

# Sample job postings - you can add more or edit these later
JOB_POSTINGS = [
    {
        "title": "Data Science Intern",
        "description": """
        We are looking for a Data Science Intern with strong skills in Python, SQL,
        Pandas, NumPy, and Scikit-learn. Experience with machine learning models,
        data visualization tools like Power BI or Tableau, and exploratory data
        analysis (EDA) is highly desired. Familiarity with Git and GitHub is a plus.
        """
    },
    {
        "title": "Machine Learning Engineer",
        "description": """
        Seeking a Machine Learning Engineer skilled in Python, TensorFlow, PyTorch,
        and deep learning. Strong understanding of neural networks, NLP, and model
        deployment. Experience with cloud platforms and MLOps is a bonus.
        """
    },
    {
        "title": "Business Data Analyst",
        "description": """
        Looking for a Data Analyst proficient in SQL, Excel, Power BI, and Tableau.
        Strong skills in data visualization, reporting, and stakeholder communication.
        Python and Pandas experience is a plus.
        """
    },
    {
        "title": "AI Research Assistant",
        "description": """
        We need an AI Research Assistant with experience in Python, machine learning,
        deep learning, and generative AI. Familiarity with research methodologies,
        NLP, and academic writing is desired.
        """
    },
    {
        "title": "Software Developer (Python)",
        "description": """
        Python Developer needed with strong programming fundamentals, experience with
        Git, GitHub, APIs, and databases (SQL). Knowledge of software engineering
        best practices and version control required.
        """
    },
]


def rank_jobs(resume_text):
    """Score the resume against every job posting and return them ranked best-to-worst."""
    results = []
    for job in JOB_POSTINGS:
        score = compute_match_score(resume_text, job["description"])
        results.append({"title": job["title"], "score": score})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


if __name__ == "__main__":
    from resume_parser import parse_resume

    sample_path = "../data/sample_resume.pdf"
    if os.path.exists(sample_path):
        resume_text = parse_resume(sample_path)
        ranked = rank_jobs(resume_text)

        print("Job Match Rankings:\n")
        for i, job in enumerate(ranked, 1):
            print(f"{i}. {job['title']} - {job['score']}%")
    else:
        print(f"No test file found at {sample_path}")