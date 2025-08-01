import os
# Avoid Chroma completely by disabling memory in CrewAI
# This line does not hurt, but the real fix is memory=False below
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

import sys
from dotenv import load_dotenv
from agents import MarketResearchAgents
from tasks import MarketResearchTasks
from crewai import Crew, Process  # Import AFTER os.environ

print("DEBUG — running with:", sys.executable)
print("DEBUG — PYTHONPATH  :", os.environ.get("PYTHONPATH"))

# Load environment variables from .env file
load_dotenv()

def run():
    """Run the market research crew."""
    # Get inputs from environment variables
    product_name = os.getenv("PRODUCT_NAME")
    product_description = os.getenv("PRODUCT_DESCRIPTION")
    industry = os.getenv("INDUSTRY")
    geography = os.getenv("GEOGRAPHY")
    scale = os.getenv("SCALE")
    competitor_focus = os.getenv("COMPETITOR_FOCUS", "")
    additional_context = os.getenv("ADDITIONAL_CONTEXT", "")
    refocus_mode = os.getenv("REFOCUS_MODE", "false")

    if not all([product_name, product_description, industry, geography, scale]):
        print("Error: One or more required environment variables are not set.")
        return

    inputs = {
        'product_name': product_name,
        'product_description': product_description,
        'industry': industry,
        'geography': geography,
        'scale': scale,
        'competitor_focus': competitor_focus,
        'additional_context': additional_context,
        'refocus_mode': refocus_mode,
    }

    # Initialize agents and tasks
    agents = MarketResearchAgents()
    tasks = MarketResearchTasks()

    # Create agent instances
    consultant = agents.strategy_consultant()
    competitor_analyst = agents.competitor_analyst()
    customer_analyst = agents.customer_persona_analyst()
    devils_advocate = agents.devils_advocate()
    synthesizer = agents.lead_strategy_synthesizer()

    # Create task instances
    planning_task = tasks.research_planning_task(consultant)
    competitor_task = tasks.competitor_analysis_task(competitor_analyst)
    customer_task = tasks.customer_analysis_task(customer_analyst)
    critique_task = tasks.risk_critique_task(devils_advocate, [planning_task, competitor_task, customer_task])
    synthesis_task = tasks.synthesis_task(synthesizer, [planning_task, competitor_task, customer_task, critique_task])

    # Assemble the crew WITHOUT memory (prevents chromadb from loading)
    crew = Crew(
        agents=[
            consultant,
            competitor_analyst,
            customer_analyst,
            devils_advocate,
            synthesizer
        ],
        tasks=[
            planning_task,
            competitor_task,
            customer_task,
            critique_task,
            synthesis_task
        ],
        process=Process.sequential,
        verbose=True,
        memory=False,        # <<--- CRITICAL: disables default memory
        knowledge=None       # <<--- Ensure no knowledge sources
    )

    # Kick off the crew's work
    print(f"🚀 Starting Comprehensive Market Research for {product_name}...")
    result = crew.kickoff(inputs=inputs)
    print("\n\n✅ Crew execution finished.")
    print("📝 Final Report Generated: final_market_analysis_report.md")

if __name__ == "__main__":
    run()
