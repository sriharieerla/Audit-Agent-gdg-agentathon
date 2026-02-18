# from crewai.tools import BaseTool
# from tools.extractor_page10 import extract_page10_data
# from tools.auditing_page10 import audit_page10_with_gemini
# from tools.pdf_builder_10 import generate_audited_page10


class Page10ExtractorTool(BaseTool):
    name: str = "page10_extractor"
    description: str = "Extract text and numbers from Page-10 PDF"

    def _run(self, pdf_path: str) -> dict:
        return extract_page10_data(pdf_path)


class Page10AuditorTool(BaseTool):
    name: str = "page10_auditor"
    description: str = "Audit Page-10 financial data using Gemini"

    def _run(self, extracted_data: dict) -> dict:
        return audit_page10_with_gemini(extracted_data)


class Page10PDFBuilderTool(BaseTool):
    name: str = "page10_pdf_builder"
    description: str = "Generate final audited Page-10 PDF with annexure"

    def _run(self, input_pdf: str, audit_result: dict) -> str:
        output_pdf = input_pdf.replace(".pdf", "_AUDITED.pdf")
        generate_audited_page10(input_pdf, audit_result, output_pdf)
        return output_pdf
