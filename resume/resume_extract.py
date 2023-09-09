"""
Extract your resume from a PDF file.
"""
import pdfplumber
import os
import re

def extract_resume(file_path: str):
    """
    Extract resume from a PDF file.
    """
    # Extract the text
    text = ""
    # Open the PDF file
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    # Remove the newlines and extra spaces
    text = re.sub(r"\s+", " ", text)
    return text

if __name__ == "__main__":
    resume = os.path.dirname(os.path.abspath(__file__))
    resume = extract_resume(f"{resume}/resume.pdf")
    print(resume)
