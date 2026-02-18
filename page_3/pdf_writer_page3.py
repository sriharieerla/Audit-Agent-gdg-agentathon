from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def generate_page3_pdf(df, audit_result, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    table_data = [df.columns.tolist()]
    table_data += df.values.tolist()

    table = Table(table_data, repeatRows=1)

    style = TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
    ])

    audit_map = {r["SlNo"]: r for r in audit_result["row_audit"]}

    for i, row in df.iterrows():
        if not audit_map[row["Sl.No"]]["valid"]:
            style.add("BACKGROUND", (0,i+1), (-1,i+1), colors.red)

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
