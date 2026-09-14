# Maps each skill to a couple of free learning resources + a quick tip
SKILL_RESOURCES = {
    "python": {
        "resources": [
            "freeCodeCamp - Python for Everybody (YouTube)",
            "docs.python.org - Official Python Tutorial",
        ],
        "tip": "Build a small script automating a daily task (e.g. file renaming) to practice."
    },
    "sql": {
        "resources": [
            "Mode Analytics SQL Tutorial (free, interactive)",
            "W3Schools SQL Tutorial",
        ],
        "tip": "Practice writing queries on a public dataset like Kaggle's SQL datasets."
    },
    "tensorflow": {
        "resources": [
            "TensorFlow official 'Get Started' guide",
            "DeepLearning.AI TensorFlow Developer course (Coursera, free to audit)",
        ],
        "tip": "Recreate a simple image classifier using the MNIST dataset."
    },
    "deep learning": {
        "resources": [
            "3Blue1Brown - Neural Networks series (YouTube)",
            "DeepLearning.AI Deep Learning Specialization (free to audit)",
        ],
        "tip": "Implement a basic neural network from scratch using only NumPy to understand the fundamentals."
    },
    "nlp": {
        "resources": [
            "Hugging Face NLP Course (free)",
            "spaCy 101 official documentation",
        ],
        "tip": "Build a simple sentiment analysis tool using a pre-trained model from Hugging Face."
    },
    "excel": {
        "resources": [
            "ExcelJet - Formula reference and tutorials",
            "Microsoft's free Excel training on support.microsoft.com",
        ],
        "tip": "Recreate a dashboard using pivot tables and charts from a sample sales dataset."
    },
    "power bi": {
        "resources": [
            "Microsoft Learn - Power BI free learning path",
            "Guy in a Cube (YouTube channel)",
        ],
        "tip": "Import a public dataset and build a 3-visual dashboard from scratch."
    },
    "tableau": {
        "resources": [
            "Tableau Public - free training videos",
            "Tableau's official 'Get Started' guide",
        ],
        "tip": "Recreate a dashboard from Tableau Public's gallery using your own data."
    },
    "machine learning": {
        "resources": [
            "Andrew Ng's Machine Learning course (Coursera, free to audit)",
            "scikit-learn official user guide",
        ],
        "tip": "Pick a Kaggle beginner competition and submit an end-to-end solution."
    },
    "git": {
        "resources": [
            "Git official documentation - Git Basics",
            "GitHub Skills (free interactive courses)",
        ],
        "tip": "Practice by version-controlling one of your existing projects and pushing it to GitHub."
    },
}

DEFAULT_TIP = "Search for a beginner project on this skill and try to build it end-to-end."
DEFAULT_RESOURCES = ["freeCodeCamp.org", "YouTube - search for a beginner tutorial"]


def get_resources_for_skills(missing_skills):
    """Return resources and tips for each missing skill."""
    result = {}
    for skill in missing_skills:
        entry = SKILL_RESOURCES.get(skill, {"resources": DEFAULT_RESOURCES, "tip": DEFAULT_TIP})
        result[skill] = entry
    return result


if __name__ == "__main__":
    test_missing = ["tensorflow", "deep learning", "nlp", "excel"]
    resources = get_resources_for_skills(test_missing)

    for skill, info in resources.items():
        print(f"\n{skill.upper()}")
        print("Tip:", info["tip"])
        print("Resources:")
        for r in info["resources"]:
            print(" -", r)