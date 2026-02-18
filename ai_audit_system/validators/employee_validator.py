import json
from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a government payroll audit specialist.

Mathematical validation and duplicate detection have already been performed.

You will receive:

- Number of employees
- Duplicate bank account detection result
- Missing IFSC detection result
- Salary-without-attendance result

Your task:
1. Evaluate severity.
2. Generate a concise audit remark.
3. Assign overall status.

Return STRICT JSON:

{
  "duplicate_account_status": "PASS or FAIL",
  "bank_validation_status": "PASS or FAIL",
  "attendance_payment_status": "PASS or FAIL",
  "overall_status": "PASS or FAIL",
  "remark": "Short professional audit remark"
}

Rules:
- Do not calculate.
- Do not explain.
- JSON only.
"""

def validate_employee(data):
    """
    Validates employee data and uses LLM for final remark.
    data: List of employee dictionaries.
    """
    employee_count = len(data)
    
    # Duplicate detection logic
    bank_accounts = [e.get("bank_account") for e in data if e.get("bank_account")]
    duplicates = len(bank_accounts) != len(set(bank_accounts))
    
    # Missing IFSC Logic
    missing_ifsc = any(not e.get("ifsc") for e in data)
    
    dup_result = "FAIL" if duplicates else "PASS"
    ifsc_result = "FAIL" if missing_ifsc else "PASS"
    salary_result = "PASS" # logic placeholder
    
    # Construct prompt for LLM
    user_prompt = f"""
Number of employees: {employee_count}
Duplicate bank account detection result: {dup_result}
Missing IFSC detection result: {ifsc_result}
Salary-without-attendance result: {salary_result}
"""

    response = call_llm(SYSTEM_PROMPT, user_prompt)
    
    try:
        json_res = json.loads(response)
        status = json_res.get("overall_status", "FAIL")
        remark = json_res.get("remark", "Audit completed.")
        
        # Calculate accuracy/score based on PASS/FAIL results
        score = 100 if status == "PASS" else 50 # simplified scoring
        
        return {
            "status": status,
            "accuracy": score,
            "remark": remark
        }
    except:
        return {
            "status": "FAIL",
            "accuracy": 0,
            "remark": "Error processing AI audit."
        }
