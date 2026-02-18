import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

PROMPT = """
You are a strict financial audit engine.

Rules:
1. Bank A/C No must be unique.
2. PAN must be unique.
3. Duplicate Employee Name allowed ONLY if
   (Employee Name + PAN + Bank A/C No) are identical.
4. calculated_total = sum(Net Amount)
5. total_match = calculated_total == total_net_amount

Return ONLY valid JSON in this exact format:
{
  "row_audit": [
    {"SlNo": number, "valid": true/false, "errors": []}
  ],
  "calculated_total_net_amount": number,
  "reported_total_net_amount": number,
  "total_match": true/false
}
"""

def audit_page3_with_groq(rows, total_net_amount):
    payload = {
        "rows": rows,
        "total_net_amount": total_net_amount
    }

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        response_format={"type": "json_object"},  # 🔥 THIS IS THE FIX
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON. No text."},
            {"role": "user", "content": PROMPT + "\n\nINPUT:\n" + json.dumps(payload)}
        ]
    )

    # Now this is GUARANTEED to be JSON
    return json.loads(response.choices[0].message.content)
