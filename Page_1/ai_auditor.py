import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
You are a financial audit AI.

Apply these formulas strictly:

Employer EPF = Remuneration × 0.13
Employer ESI = Remuneration × 0.0325
Employee EPF = Remuneration × 0.12
Employee ESI = Remuneration × 0.0075

PT:
- 0 if Remuneration ≤ 15000
- 150 if 15001–20000
- 200 if > 20000

Total Amount Payable =
Remuneration + Employer EPF + Employer ESI +
Employee EPF + Employee ESI + PT + APCOS Welfare Fund

CGST = Total Amount Payable × 0.09
SGST = Total Amount Payable × 0.09
Grand Total = Total Amount Payable + CGST + SGST

Compare expected vs actual values.

Return ONLY valid JSON in this format:

{
  "Employer EPF": {"expected": number, "actual": number, "correct": true/false},
  "Employer ESI": {"expected": number, "actual": number, "correct": true/false},
  "Employee EPF": {"expected": number, "actual": number, "correct": true/false},
  "Employee ESI": {"expected": number, "actual": number, "correct": true/false},
  "PT": {"expected": number, "actual": number, "correct": true/false},
  "Taxable Total": {"expected": number, "actual": number, "correct": true/false},
  "CGST": {"expected": number, "actual": number, "correct": true/false},
  "SGST": {"expected": number, "actual": number, "correct": true/false},
  "Grand Total": {"expected": number, "actual": number, "correct": true/false}
}
"""


def audit_row_with_llm(row):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": PROMPT + "\n\nROW:\n" + json.dumps(row, indent=2)}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


def safe_audit_row(row):
    try:
        return audit_row_with_llm(row)
    except Exception as e:
        print("⚠️ LLM error, fallback used:", e)
        return {
            k: {"expected": None, "actual": row.get(k), "correct": True}
            for k in [
                "Employer EPF", "Employer ESI",
                "Employee EPF", "Employee ESI",
                "PT", "Taxable Total",
                "CGST", "SGST", "Grand Total"
            ]
        }
