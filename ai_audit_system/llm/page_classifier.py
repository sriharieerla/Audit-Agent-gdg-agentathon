from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a document classification engine.

Your task:
Classify the given PDF page content into exactly ONE of the following categories:

- SUMMARY
- EMPLOYEE_DETAILS
- BUDGET
- INVOICE
- APPROVAL
- OTHER

Definitions:

SUMMARY:
Page containing overall totals, monthly summary, grand totals, CGST, SGST.

EMPLOYEE_DETAILS:
Page listing individual employees, bank accounts, IFSC, salary details.

BUDGET:
Page showing approved budget, expenditure, balance.

INVOICE:
Page containing attendance, remuneration, EPF/ESI/PT, taxable total, GST.

APPROVAL:
Page containing government approval order, sanctioned amount, official authorization.

OTHER:
Any page not matching the above.

Rules:
- Return ONLY one word.
- No explanation.
- No extra text.
- No formatting.
"""

def classify_page(page_text):
    """
    Classifies the page text into a category.
    """
    user_prompt = f"""
Classify this page:

{page_text[:2000]} 
""" 
    # Truncate to avoid token limits in a real scenario
    
    response = call_llm(SYSTEM_PROMPT, user_prompt)
    return response.strip()
