import json
from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a public expenditure audit officer.

Budget validation has already been computed.

You will receive:
- Approved budget
- Total expenditure
- Balance correctness result
- Over-expenditure detection result

Your task:
1. Evaluate budget compliance.
2. Assign PASS or FAIL.
3. Provide a concise remark.

Return STRICT JSON:

{
  "budget_compliance_status": "PASS or FAIL",
  "balance_status": "PASS or FAIL",
  "overall_status": "PASS or FAIL",
  "remark": "Short professional remark"
}

Rules:
- No calculations.
- No explanation.
- JSON only.
"""

def validate_budget(data):
    """
    Validates budget data.
    """
    approved = data.get("approved_budget", 0.0)
    expenditure = data.get("expenditure", 0.0)
    balance = data.get("balance", 0.0)
    
    calculated_balance = approved - expenditure
    
    balance_correct = abs(calculated_balance - balance) < 1.0 # Tolerance for float math
    over_expenditure = expenditure > approved
    
    balance_res = "PASS" if balance_correct else "FAIL"
    over_res = "FAIL" if over_expenditure else "PASS"
    
    user_prompt = f"""
Approved budget: {approved}
Total expenditure: {expenditure}
Balance correctness result: {balance_res}
Over-expenditure detection result: {over_res}
"""

    response = call_llm(SYSTEM_PROMPT, user_prompt)
    
    try:
        json_res = json.loads(response)
        status = json_res.get("overall_status", "FAIL")
        return {
            "status": status,
            "accuracy": 100 if status == "PASS" else 0,
            "remark": json_res.get("remark", "Budget reviewed.")
        }
    except:
        return {"status": "FAIL", "accuracy": 0, "remark": "AI Error"}
