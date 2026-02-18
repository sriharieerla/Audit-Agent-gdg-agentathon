# main.py
# ---------------------------------------
# LLM-based PDF Audit Pipeline
# ---------------------------------------

from extractor import extract_table
from ai_auditor import audit_row_with_llm
from pdf_writer import generate_pdf

INPUT_PDF = "input/sample.pdf"
OUTPUT_PDF = "output/audited.pdf"


def main():
    print("🚀 Starting LLM PDF Audit...\n")

    df = extract_table(INPUT_PDF)

    all_audits = []

    for idx, row in df.iterrows():
        print(f"🤖 Auditing row {idx + 1} via LLM...")
        audit_result = audit_row_with_llm(row.to_dict())
        all_audits.append(audit_result)

    generate_pdf(
        df=df,
        audits=all_audits,
        output_path=OUTPUT_PDF
    )

    print("\n✅ LLM Audited PDF generated:")
    print(f"➡️ {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
