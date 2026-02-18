import json
import random

def call_llm(system_prompt, user_prompt):
    """
    Simulates a call to an LLM (e.g., OpenAI, Anthropic).
    Returns a string response.
    """
    # print(f"\n[Mock LLM Call] System: {system_prompt[:50]}... | User: {user_prompt[:50]}...")
    
    # 1. Page Classification - Keyword based for testing
    if "Classify the given PDF page" in system_prompt:
        up = user_prompt.upper()
        if "SUMMARY" in up: return "SUMMARY"
        if "EMPLOYEE" in up: return "EMPLOYEE_DETAILS"
        if "BUDGET" in up: return "BUDGET"
        if "INVOICE" in up: return "INVOICE"
        if "APPROVAL" in up: return "APPROVAL"
        return "OTHER"
        
    # 2. Invoice Audit
    if "financial audit officer" in system_prompt:
        return json.dumps({
            "attendance_status": "PASS",
            "remuneration_status": "PASS",
            "statutory_status": "PASS",
            "totals_status": "PASS",
            "overall_status": "PASS",
            "remark": "All calculations match."
        })

    # 3. Employee Audit
    if "government payroll audit specialist" in system_prompt:
        return json.dumps({
            "duplicate_account_status": "PASS",
            "bank_validation_status": "PASS",
            "attendance_payment_status": "PASS",
            "overall_status": "PASS",
            "remark": "No duplicates found."
        })

    # 4. Budget Audit
    if "public expenditure audit officer" in system_prompt:
        return json.dumps({
            "budget_compliance_status": "PASS",
            "balance_status": "PASS",
            "overall_status": "PASS",
            "remark": "Within budget limits."
        })

    # 5. Approval Audit
    if "government authorization verification officer" in system_prompt:
        return json.dumps({
            "authorization_status": "PASS",
            "amount_match_status": "PASS",
            "overall_status": "PASS",
            "remark": "Authorized correctly."
        })

    # 6. Final Report
    if "senior AI audit report generator" in system_prompt:
        return json.dumps({
            "final_score": 95,
            "risk_level": "LOW",
            "final_conclusion": "The audit found no significant discrepancies. All financial documents appear to be in order and compliant with regulations."
        })
        
    return "MOCK_RESPONSE"
