import pdfplumber
import pandas as pd
import re

def extract_page3(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        table = page.extract_table()
        text = page.extract_text()

    if not table:
        raise ValueError("No table found")

    headers = [h.strip() for h in table[0]]
    df = pd.DataFrame(table[1:], columns=headers)

    df["Sl.No"] = df["Sl.No"].astype(int)
    df["Employee Name"] = df["Employee Name"].str.strip()
    df["Bank A/C No"] = df["Bank A/C No"].str.strip()
    df["PAN"] = df["PAN"].str.strip()
    df["Net Amount"] = (
        df["Net Amount"].str.replace(",", "").astype(float)
    )

    # 🔥 Extract Total Net Amount from footer text
    match = re.search(r"Total Net Amount[:\s]*([\d,]+\.\d+)", text)
    if not match:
        raise ValueError("Total Net Amount not found in PDF")

    reported_total = float(match.group(1).replace(",", ""))

    return df, reported_total
