import json
from llm.llm_client import call_llm

SYSTEM_PROMPT = """
You are a senior AI audit report generator.

You will receive validation results for multiple pages of a financial document.

Your task:
1. Summarize overall compliance.
2. Highlight major risk areas.
3. Provide a final audit conclusion.

Return STRICT JSON:

{
  "final_score": "numeric percentage",
  "risk_level": "LOW, MODERATE, or HIGH",
  "final_conclusion": "Professional audit summary paragraph"
}

Rules:
- No explanation outside JSON.
- Do not change numeric score.
- Be professional and concise.
"""

def generate_final_report(page_results, final_score):
    """
    Generates the final audit report JSON.
    """
    # Convert page results to a string summary
    results_summary = json.dumps(page_results, indent=2)
    
    user_prompt = f"""
Here are the audit results for the document pages:

{results_summary}

The calculated final score is: {final_score}%

Generate the consolidated audit report.
"""

    response = call_llm(SYSTEM_PROMPT, user_prompt)
    
    try:
        data = json.loads(response)
        # Ensure final score matches the calculated one if the LLM hallucinated it
        data["final_score"] = final_score 
        return data
    except Exception:
        # Fallback if JSON parsing fails
        return {
            "final_score": final_score,
            "risk_level": "UNKNOWN",
            "final_conclusion": "Error generating AI report."
        }
