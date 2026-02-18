# pdf_writer.py
# ---------------------------------------
# APCOS PDF Generator (Exact Structure)
# ---------------------------------------

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(df, audits, output_path):
    # ===============================
    # ACCURACY CALCULATION
    # ===============================
    total_checks = 0
    correct_checks = 0

    for audit in audits:
        for field, result in audit.items():
            total_checks += 1
            if result.get("correct"):
                correct_checks += 1

    accuracy = (correct_checks / total_checks * 100) if total_checks else 0.0

    # ===============================
    # PDF SETUP (LANDSCAPE)
    # ===============================
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()
    elements = []

    # ===============================
    # TITLE
    # ===============================
    elements.append(
        Paragraph(f"<b>AI Audit Accuracy:</b> {accuracy:.2f}%", styles["Title"])
    )

    # ===============================
    # APCOS HEADER (2 ROWS)
    # ===============================
    header_row_1 = [
        "MONTH",
        "Remuneration\nas per Attendance",
        "Employer Contribution", "",
        "Employee Contribution", "",
        "PT",
        "APCOS\nWelfare Fund",
        "Total Amount\nPayable",
        "CGST 9%",
        "SGST 9%",
        "Grand\nTotal"
    ]

    header_row_2 = [
        "", "",
        "E.P.F", "E.S.I",
        "E.P.F", "E.S.I",
        "", "", "", "", "", ""
    ]

    table_data = [header_row_1, header_row_2]

    # ===============================
    # DATA ROWS (NO FORMAT CHANGE)
    # ===============================
    for _, row in df.iterrows():
        table_data.append([
            row["MONTH"],
            row["Remuneration"],
            row["Employer EPF"],
            row["Employer ESI"],
            row["Employee EPF"],
            row["Employee ESI"],
            row["PT"],
            row["APCOS Welfare Fund"],
            row["Taxable Total"],
            row["CGST"],
            row["SGST"],
            row["Grand Total"],
        ])

    # ===============================
    # COLUMN WIDTHS (LOCKED)
    # ===============================
    col_widths = [
        55,   # MONTH
        90,   # Remuneration
        70,   # Employer EPF
        60,   # Employer ESI
        70,   # Employee EPF
        60,   # Employee ESI
        45,   # PT
        85,   # Welfare
        90,   # Taxable
        60,   # CGST
        60,   # SGST
        80    # Grand Total
    ]

    table = Table(
        table_data,
        colWidths=col_widths,
        repeatRows=2,
        splitByRow=1
    )

    style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 1), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
        ("ALIGN", (1, 2), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),

        # Header spans
        ("SPAN", (2, 0), (3, 0)),
        ("SPAN", (4, 0), (5, 0)),
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (1, 0), (1, 1)),
        ("SPAN", (6, 0), (6, 1)),
        ("SPAN", (7, 0), (7, 1)),
        ("SPAN", (8, 0), (8, 1)),
        ("SPAN", (9, 0), (9, 1)),
        ("SPAN", (10, 0), (10, 1)),
        ("SPAN", (11, 0), (11, 1)),
    ])

    # ===============================
    # RED MARKING (LLM RESULTS)
    # ===============================
    col_index_map = {
        "Employer EPF": 2,
        "Employer ESI": 3,
        "Employee EPF": 4,
        "Employee ESI": 5,
        "PT": 6,
        "APCOS Welfare Fund": 7,
        "Taxable Total": 8,
        "CGST": 9,
        "SGST": 10,
        "Grand Total": 11
    }

    for row_idx, audit in enumerate(audits):
        for field, result in audit.items():
            if not result.get("correct", True):
                col_idx = col_index_map.get(field)
                if col_idx is not None:
                    style.add(
                        "TEXTCOLOR",
                        (col_idx, row_idx + 2),  # +2 for header rows
                        (col_idx, row_idx + 2),
                        colors.red
                    )

    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
