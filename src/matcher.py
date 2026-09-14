from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_match_score(resume_text, job_description):
    """Compute a similarity score (0-100) between a resume and a job description."""
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = similarity[0][0] * 100

    return round(score, 2)


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from resume_parser import parse_resume

    sample_path = "../data/sample_resume.pdf"

    # A sample job description to test against - edit this to test different jobs
    sample_job_description = """
    We are looking for a Data Science Intern with strong skills in Python, SQL,
    Pandas, NumPy, and Scikit-learn. Experience with machine learning models,
    data visualization tools like Power BI or Tableau, and exploratory data
    analysis (EDA) is highly desired. Familiarity with Git and GitHub is a plus.
    """

    if os.path.exists(sample_path):
        resume_text = parse_resume(sample_path)
        score = compute_match_score(resume_text, sample_job_description)
        print(f"Match score: {score}%")
    else:
        print(f"No test file found at {sample_path}")