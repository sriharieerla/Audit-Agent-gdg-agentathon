import json
from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a senior financial audit officer.

The financial calculations have already been verified separately.

Your task:
Evaluate logical consistency of the invoice data provided.

You will receive structured data including:

- Attendance details
- Remuneration amounts
- EPF/ESI/PT values
- GST values
- Grand total
- Pre-calculated validation results (PASS/FAIL per section)

You must:

1. Review section validation results.
2. Determine if there are logical inconsistencies.
3. Assign an overall section-based status.
4. Generate a short audit remark.

Return STRICT JSON only in this format:

{
  "attendance_status": "PASS or FAIL",
  "remuneration_status": "PASS or FAIL",
  "statutory_status": "PASS or FAIL",
  "totals_status": "PASS or FAIL",
  "overall_status": "PASS or FAIL",
  "remark": "ONE concise audit remark (max 10 words)"
}

Rules:
- Do NOT perform arithmetic.
- Do NOT explain.
- Do NOT include extra text.
- Return JSON only.
"""

def validate_invoice(data):
    """
    Validates invoice data.
    """
    # math checks
    remuneration = data.get("remuneration", 0)
    taxable = data.get("total_taxable", 0)
    gst = data.get("gst", 0)
    grand_total = data.get("grand_total", 0)
    
    # Simple logic checks
    remuneration_check = "PASS" if remuneration > 0 else "FAIL"
    # Statutory check logic (mock)
    statutory_check = "PASS" 
    
    # Totals check: Taxable + GST should differ from Grand Total by small margin? 
    # Or Grand Total = Taxable + GST?
    calculated_total = taxable + gst
    totals_check = "PASS" if abs(calculated_total - grand_total) < 1.0 else "FAIL"
    
    user_prompt = f"""
Attendance Section: PASS
Remuneration Section: {remuneration_check}
Statutory Section: {statutory_check}
Totals Section: {totals_check}

Additional Context:
Calculated Total: {calculated_total}
Claimed Total: {grand_total}
"""

    response = call_llm(SYSTEM_PROMPT, user_prompt)
    
    try:
        json_res = json.loads(response)
        return {
            "status": json_res.get("overall_status", "FAIL"),
            "accuracy": 80 if json_res.get("overall_status") == "PASS" else 40,
            "remark": json_res.get("remark", "Invoice audited.")
        }
    except:
        return {"status": "FAIL", "accuracy": 0, "remark": "AI Error"}
