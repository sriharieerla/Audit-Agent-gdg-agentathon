import json
from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a government authorization verification officer.

Invoice and approval amount comparison has already been computed.

You will receive:
- Sanctioned amount
- Claimed amount
- Difference result

Your task:
1. Determine authorization validity.
2. Assign PASS or FAIL.
3. Provide a short remark.

Return STRICT JSON:

{
  "authorization_status": "PASS or FAIL",
  "amount_match_status": "PASS or FAIL",
  "overall_status": "PASS or FAIL",
  "remark": "Short compliance remark"
}

Rules:
- Do not perform calculations.
- JSON only.
- No extra text.
"""

def validate_approval(data):
    """
    Validates approval documents.
    """
    sanctioned = data.get("sanctioned_amount", 0)
    claimed = data.get("claimed_amount", 0)
    
    diff = sanctioned - claimed
    match_status = "PASS" if diff >= 0 else "FAIL" # Sent back as "Difference Result" context
    
    user_prompt = f"""
Sanctioned amount: {sanctioned}
Claimed amount: {claimed}
Difference result: {'Within Limit' if diff >=0 else 'Exceeds Limit'}
"""

    response = call_llm(SYSTEM_PROMPT, user_prompt)
    
    try:
        json_res = json.loads(response)
        return {
            "status": json_res.get("overall_status", "FAIL"),
            "accuracy": 100 if json_res.get("overall_status") == "PASS" else 0,
            "remark": json_res.get("remark", "Approval checked.")
        }
    except:
        return {"status": "FAIL", "accuracy": 0, "remark": "AI Error"}
