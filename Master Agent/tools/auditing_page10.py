import os
from crewai.tools import tool
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@tool("Audit Page 10 with Gemini")
def auditing_page10(text_data: str) -> str:
    """
    Audits Page 10 financial data using Gemini and returns audit findings.
    """

    prompt = f"""
You are a strict financial audit engine.

Rules:
- Do NOT hallucinate
- Verify calculations only
- Highlight mismatches clearly

INPUT DATA:
{text_data}
"""

    response = client.models.generate_content(
        model="models/gemini-1.5-pro-002",
        contents=prompt
    )

    return response.text
