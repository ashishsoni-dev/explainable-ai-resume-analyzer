# Extract text content from PDF resumes
import pdfplumber

# Reads PDF and return extracted text, returns None if failed
def extract_text_from_pdf(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception:
        return None

    return text if text.strip() else None