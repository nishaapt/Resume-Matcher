from sentence_transformers import SentenceTransformer, util

# Load once - this model is small, fast, and good quality for this use case
_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_semantic_score(resume_text, job_description):
    """Compute a meaning-based similarity score (0-100) between resume and job description."""
    embeddings = _model.encode([resume_text, job_description], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    score = similarity.item() * 100
    return round(score, 2)


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    from resume_parser import parse_resume

    sample_path = "../data/sample_resume.pdf"
    sample_job_description = """
    We are looking for a Data Science Intern with strong skills in Python, SQL,
    Pandas, NumPy, and Scikit-learn. Experience with machine learning models,
    data visualization tools like Power BI or Tableau, and exploratory data
    analysis (EDA) is highly desired. Familiarity with Git and GitHub is a plus.
    """

    if os.path.exists(sample_path):
        resume_text = parse_resume(sample_path)
        score = compute_semantic_score(resume_text, sample_job_description)
        print(f"Semantic match score: {score}%")
    else:
        print(f"No test file found at {sample_path}")