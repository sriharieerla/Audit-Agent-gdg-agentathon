from dotenv import load_dotenv
load_dotenv()

from crew import build_page10_crew
from tools.auditing_page10 import audit_page10_with_gemini

if __name__ == "__main__":
    # Step 1: CrewAI preprocessing (no LLM)
    crew = build_page10_crew()
    extracted_data = crew.kickoff()

    print("\n✅ CREW PREPROCESSING DONE\n")

    # Step 2: Gemini audit (v1 API)
    audit_result = audit_page10_with_gemini(str(extracted_data))

    print("\n🔍 FINAL PAGE 10 AUDIT RESULT\n")
    print(audit_result)
