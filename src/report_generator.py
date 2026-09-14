from fpdf import FPDF


def generate_report(score, resume_skills, missing_skills, job_rankings, output_path="data/analysis_report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "AI Resume Analysis Report", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Match Score: {score}%", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Your Skills", ln=True)
    pdf.set_font("Helvetica", "", 11)
    if resume_skills:
        pdf.multi_cell(0, 7, ", ".join(resume_skills))
    else:
        pdf.multi_cell(0, 7, "None detected")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Missing Skills", ln=True)
    pdf.set_font("Helvetica", "", 11)
    if missing_skills:
        pdf.multi_cell(0, 7, ", ".join(missing_skills))
    else:
        pdf.multi_cell(0, 7, "None - great match!")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Similar Job Matches", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for i, job in enumerate(job_rankings, 1):
        pdf.cell(0, 7, f"{i}. {job['title']} - {job['score']}%", ln=True)

    pdf.output(output_path)
    return output_path