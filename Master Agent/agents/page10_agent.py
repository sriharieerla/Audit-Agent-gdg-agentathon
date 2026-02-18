from crewai import Agent

page10_agent = Agent(
    role="Page 10 Data Preprocessor",
    goal="Prepare Page 10 financial data for auditing",
    backstory="Expert government data extraction officer",
    verbose=True,
    allow_delegation=False
)
