import re

def extract_approval(text):
    """
    Extracts approval/sanction details.
    Returns: {'sanctioned_amount': float, 'claimed_amount': float}
    """
    data = {
        "sanctioned_amount": 0.0,
        "claimed_amount": 0.0
    }
    
    # Mock regex
    sanctioned_match = re.search(r"Sanctioned Amount\s*[:=-]?\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    if sanctioned_match:
        data["sanctioned_amount"] = float(sanctioned_match.group(1).replace(",", ""))

    return data
