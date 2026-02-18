from extractor_page3 import extract_page3
from ai_auditor_page3_groq import audit_page3_with_groq
from pdf_writer_page3 import generate_page3_pdf

INPUT_PDF = "input/Page_3.pdf"
OUTPUT_PDF = "output/outputPage_3.pdf"

def main():
    df, reported_total = extract_page3(INPUT_PDF)

    rows = df.to_dict(orient="records")

    audit_result = audit_page3_with_groq(
        rows=rows,
        total_net_amount=reported_total
    )

    generate_page3_pdf(df, audit_result, OUTPUT_PDF)

    print("✅ Page-3 GROQ Audit Complete")
    print("Calculated Total:", audit_result["calculated_total_net_amount"])
    print("Reported Total:", reported_total)
    print("Total Match:", audit_result["total_match"])

if __name__ == "__main__":
    main()
