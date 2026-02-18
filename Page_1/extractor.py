# extractor.py
# ---------------------------------------
# PDF Table Extraction & Normalization
# ---------------------------------------

import pdfplumber
import pandas as pd
import re


def clean_cell(x):
    """
    Clean individual cell values:
    - Remove commas
    - Convert numeric strings to float
    """
    if isinstance(x, str):
        x = x.replace(",", "").strip()
        if re.fullmatch(r"-?\d+(\.\d+)?", x):
            return float(x)
        return x
    return x


def extract_table(pdf_path):
    # -------------------------------
    # Read first page table
    # -------------------------------
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        table = page.extract_table()

    if not table or len(table) < 3:
        raise ValueError("No valid table detected in PDF")

    # -------------------------------
    # Build headers
    # -------------------------------
    headers = [
        str(h).replace("\n", " ").strip() if h else f"COL_{i}"
        for i, h in enumerate(table[0])
    ]

    df = pd.DataFrame(table[1:], columns=headers)

    # -------------------------------
    # Clean all cells
    # -------------------------------
    df = df.apply(lambda col: col.map(clean_cell))

    # -------------------------------
    # Canonical column renaming
    # -------------------------------
    rename_map = {
        "Remuneration as per Attendance": "Remuneration",

        "Employer Contribution": "Employer EPF",
        "COL_3": "Employer ESI",

        "Employee Contribution": "Employee EPF",
        "COL_5": "Employee ESI",

        "Total Amount Payable": "Taxable Total",
        "CGST 9%": "CGST",
        "SGST 9%": "SGST",
        "Grand Total": "Grand Total"
    }

    df.rename(columns=rename_map, inplace=True)

    # -------------------------------
    # 🔴 ABSOLUTE FIX:
    # Remove EPF/ESI header-artifact row
    # -------------------------------
    def is_real_data_row(row):
        # Must contain a valid month like Jan-22
        month = str(row.get("MONTH", "")).strip()
        if not re.search(r"[A-Za-z]{3}-\d{2}", month):
            return False

        # Must NOT contain header tokens
        header_tokens = {"E.P.F", "E.S.I"}
        row_values = set(str(v) for v in row.values)
        if header_tokens & row_values:
            return False

        return True

    df = df[df.apply(is_real_data_row, axis=1)]

    df.reset_index(drop=True, inplace=True)

    # -------------------------------
    # Debug output
    # -------------------------------
    print("\n✅ Cleaned & Normalized Columns:")
    print(df.columns.tolist())
    print("✅ Valid data rows:", len(df))

    return df
 