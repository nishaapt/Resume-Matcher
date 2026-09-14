import PyPDF2
import docx
import os


def extract_text_from_pdf(file_path):
    """Extract raw text from a PDF resume."""
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path):
    """Extract raw text from a DOCX resume."""
    doc = docx.Document(file_path)
    text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return text


def parse_resume(file_path):
    """Detect file type and extract text accordingly."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


if __name__ == "__main__":
    sample_path = "../data/sample_resume.pdf"
    if os.path.exists(sample_path):
        result = parse_resume(sample_path)
        print(result)
    else:
        print(f"No test file found at {sample_path}. Add a sample resume to the data folder to test.")