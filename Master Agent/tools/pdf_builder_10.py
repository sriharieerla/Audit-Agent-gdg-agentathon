from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfReader, PdfWriter
import io

def generate_audited_page10(input_pdf, audit_result, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    writer.add_page(reader.pages[0])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("<b>AI AUDIT VERIFICATION REPORT (ANNEXURE)</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    table_data = [["Audit Check", "Status"]]

    for check in audit_result.get("checks", []):
        status = check["status"].lower()
        color = colors.green if status == "correct" else colors.red
        label = "VERIFIED" if status == "correct" else "MISMATCH"

        table_data.append([
            check["field"],
            Paragraph(f'<font color="{color.hexval()}"><b>{label}</b></font>', styles["Normal"])
        ])

    table = Table(table_data, colWidths=[320, 120])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    accuracy = audit_result.get("accuracy", 0)
    color = colors.green if accuracy == 100 else colors.red

    elements.append(
        Paragraph(
            f'<font color="{color.hexval()}"><b>FINAL AUDIT RESULT: {accuracy}% COMPLIANT</b></font>',
            styles["Heading2"]
        )
    )

    doc.build(elements)
    buffer.seek(0)

    audit_page = PdfReader(buffer).pages[0]
    writer.add_page(audit_page)

    with open(output_pdf, "wb") as f:
        writer.write(f)
