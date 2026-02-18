import re

def extract_budget(text):
    """
    Extracts budget information.
    Returns: {'approved_budget': float, 'expenditure': float, 'balance': float}
    """
    data = {
        "approved_budget": 0.0,
        "expenditure": 0.0,
        "balance": 0.0
    }
    
    # Example regex extraction
    budget_match = re.search(r"Approved Budget\s*[:=-]?\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    if budget_match:
        data["approved_budget"] = float(budget_match.group(1).replace(",", ""))

    return data
