from llm.llm_client import call_llm

def validate_summary(data):
    """
    Validates summary extraction data.
    """
    grand_total = data.get("grand_total", 0)
    
    # Simple logic
    status = "PASS" if grand_total > 0 else "FAIL"
    accuracy = 100 if status == "PASS" else 0
    remark = "Summary totals appear valid." if status == "PASS" else "Grand total missing or zero."
    
    # Note: The prompt didn't specify a "Summary Audit Prompt", so we treat it as basic validation
    # If LLM audit is needed, we'd add it here.
    
    return {
        "status": status,
        "accuracy": accuracy,
        "remark": remark
    }
