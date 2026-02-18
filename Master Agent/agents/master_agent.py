from crewai import Agent

master_agent = Agent(
    role="Master Audit Orchestrator",
    goal="Coordinate sub-agents and deliver final audited PDF",
    backstory="Delegates work to specialist agents and returns results.",
    llm=None,          # 🔥 VERY IMPORTANT
    verbose=True
)
