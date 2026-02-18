import os
from PyPDF2 import PdfReader, PdfWriter

# Page Classifier
from llm.page_classifier import classify_page

# Extractors
from extractors.summary_extractor import extract_summary
from extractors.employee_extractor import extract_employee
from extractors.budget_extractor import extract_budget
from extractors.invoice_extractor import extract_invoice
from extractors.approval_extractor import extract_approval

# Validators
from validators.summary_validator import validate_summary
from validators.employee_validator import validate_employee
from validators.budget_validator import validate_budget
from validators.invoice_validator import validate_invoice
from validators.approval_validator import validate_approval

# Annotation
from annotation.pdf_overlay import annotate_page

# Final Report
from llm.final_report import generate_final_report



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")


def orchestrate_audit(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    page_results = []

    print("Starting Full AI Audit Process...")

    for page_number, page in enumerate(reader.pages):

        print(f"\nProcessing Page {page_number + 1}")

        # Extract text
        page_text = page.extract_text()

        # Classify page
        page_type = classify_page(page_text)

        print(f"Classified as: {page_type}")

        audit_result = None

        # Route to correct engine
        if page_type == "SUMMARY":
            data = extract_summary(page_text)
            audit_result = validate_summary(data)

        elif page_type == "EMPLOYEE_DETAILS":
            data = extract_employee(page_text)
            audit_result = validate_employee(data)

        elif page_type == "BUDGET":
            data = extract_budget(page_text)
            audit_result = validate_budget(data)

        elif page_type == "INVOICE":
            data = extract_invoice(page_text)
            audit_result = validate_invoice(data)

        elif page_type == "APPROVAL":
            data = extract_approval(page_text)
            audit_result = validate_approval(data)

        else:
            print("Skipping non-important page.")
            writer.add_page(page)
            continue

        # Store page-level result
        page_results.append({
            "page_number": page_number + 1,
            "page_type": page_type,
            "accuracy": audit_result["accuracy"],
            "status": audit_result["status"],
            "remark": audit_result["remark"]
        })

        # Annotate page
        annotated_page = annotate_page(page, audit_result)
        writer.add_page(annotated_page)

    # ===============================
    # FINAL CONSOLIDATED REPORT
    # ===============================

    if page_results:
        final_score = sum(p["accuracy"] for p in page_results) / len(page_results)
        final_score = round(final_score, 2)

        print(f"\nFinal Audit Score: {final_score}%")

        final_summary = generate_final_report(page_results, final_score)

        # Add final report page
        report_page = annotate_page(None, final_summary, is_summary=True)
        writer.add_page(report_page)

    # Save output
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print(f"\nAudit Completed Successfully. Output saved to: {output_pdf_path}")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Example usage - check if input file exists before running
    input_file = os.path.join(INPUT_FOLDER, "sample.pdf")
    output_file = os.path.join(OUTPUT_FOLDER, "audited_report.pdf")
    
    if os.path.exists(input_file):
        orchestrate_audit(input_file, output_file)
    else:
        print(f"Please place a PDF file at {input_file} to run the audit.")
