#extractor_page10.py
import pdfplumber
import re


def extract_page10_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    if not text:
        raise ValueError("No text found in Page-10 PDF")

    # Extract numeric amounts
    amounts = re.findall(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?", text)

    return {
        "full_text": text,
        "numbers_found": amounts
    }
