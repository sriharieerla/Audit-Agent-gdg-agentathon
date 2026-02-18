from crewai import Crew, Task
from agents.page10_agent import page10_agent

def build_page10_crew():
    task = Task(
        description="Extract and structure Page 10 financial data",
        expected_output="Structured Page 10 text ready for audit",
        agent=page10_agent
    )

    return Crew(
        agents=[page10_agent],
        tasks=[task],
        verbose=True
    )
