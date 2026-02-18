import re

def extract_summary(text):
    """
    Extracts summary details from the page text.
    Returns a dictionary with keys: overall_totals, monthly_summary, grand_total, cgst, sgst.
    """
    # Placeholder logic - in a real scenario, use regex or layout analysis
    # Example regex patterns (simplified)
    
    data = {
        "overall_totals": 0.0,
        "monthly_summary": {},
        "grand_total": 0.0,
        "cgst": 0.0,
        "sgst": 0.0
    }
    
    # Mock implementation for demonstration
    # searching for "Grand Total: 12345"
    grand_total_match = re.search(r"Grand Total\s*[:=-]?\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    if grand_total_match:
        data["grand_total"] = float(grand_total_match.group(1).replace(",", ""))
        
    return data
