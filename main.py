import os
import sys
from crewai import Crew, Process
from agents import MarketResearchAgents
from tasks import MarketResearchTasks
from dotenv import load_dotenv
print("DEBUG — running with:", sys.executable)
print("DEBUG — PYTHONPATH  :", os.environ.get("PYTHONPATH"))

# Load environment variables from .env file
load_dotenv()

def run():
    """Run the market research crew."""
    # Get inputs from environment variables
    product_name = os.getenv("PRODUCT_NAME")
    product_description = os.getenv("PRODUCT_DESCRIPTION")
    usp = os.getenv("USP", "")
    usp_confidence = os.getenv("USP_CONFIDENCE", "Not Sure")
    industry = os.getenv("INDUSTRY")
    geography = os.getenv("GEOGRAPHY")
    scale = os.getenv("SCALE")
    competitor_focus = os.getenv("COMPETITOR_FOCUS", "")
    additional_context = os.getenv("ADDITIONAL_CONTEXT", "")
    refocus_mode = os.getenv("REFOCUS_MODE", "false")
    enable_charts = os.getenv("ENABLE_CHARTS", "True").lower() == "true"
    include_market_maps = os.getenv("INCLUDE_MARKET_MAPS", "True").lower() == "true"

    if not all([product_name, product_description, industry, geography, scale]):
        print("Error: One or more required environment variables are not set.")
        return

    inputs = {
        'product_name': product_name,
        'product_description': product_description,
        'usp': usp,
        'usp_confidence': usp_confidence,
        'industry': industry,
        'geography': geography,
        'scale': scale,
        'competitor_focus': competitor_focus,
        'additional_context': additional_context,
        'refocus_mode': refocus_mode,
        'enable_charts': enable_charts,
        'include_market_maps': include_market_maps,
    }

    # Initialize agents and tasks
    agents = MarketResearchAgents()
    tasks = MarketResearchTasks()

    # Create agent instances
    consultant = agents.strategy_consultant()
    usp_analyst = agents.usp_analyst()
    porters_trend_analyst = agents.porters_trend_analyst()
    competitor_analyst = agents.competitor_analyst()
    customer_analyst = agents.customer_persona_analyst()
    devils_advocate = agents.devils_advocate()
    synthesizer = agents.lead_strategy_synthesizer()

    # Create task instances
    planning_task = tasks.research_planning_task(consultant)
    usp_task = tasks.usp_analysis_task(usp_analyst)
    porters_trend_task = tasks.porters_trend_analysis_task(porters_trend_analyst)
    competitor_task = tasks.competitor_analysis_task(competitor_analyst)
    customer_task = tasks.customer_analysis_task(customer_analyst)
    critique_task = tasks.risk_critique_task(devils_advocate, [planning_task, usp_task, porters_trend_task, competitor_task, customer_task])
    synthesis_task = tasks.synthesis_task(synthesizer, [planning_task, usp_task, porters_trend_task, competitor_task, customer_task, critique_task])

    # Assemble the crew
    crew = Crew(
        agents=[
            consultant,
            usp_analyst,
            porters_trend_analyst,
            competitor_analyst,
            customer_analyst,
            devils_advocate,
            synthesizer
        ],
        tasks=[
            planning_task,
            usp_task,
            porters_trend_task,
            competitor_task,
            customer_task,
            critique_task,
            synthesis_task
        ],
        process=Process.sequential,
        verbose=True # Set to False to hide backend logs as requested
    )

    # Run the crew
    print("🚀 Starting MarketMinds analysis...")
    print("📊 Visualization tools available:")
    print(f"   - ChartGenerator: {agents.chart_generator}")
    print(f"   - MarketMapGenerator: {agents.market_map_generator}")
    result = crew.kickoff(inputs=inputs)
    
    # Save chart data for Streamlit access
    try:
        print("💾 Saving chart data...")
        agents.chart_generator.save_charts_to_file('generated_charts.json')
        agents.market_map_generator.save_maps_to_file('generated_maps.json')
        print("📊 Chart data saved for Streamlit display")
        
        # Show what was generated
        charts_count = len(agents.chart_generator.get_charts_data())
        maps_count = len(agents.market_map_generator.get_maps_data())
        print(f"📈 Generated {charts_count} charts and {maps_count} maps")
        
    except Exception as e:
        print(f"⚠️ Warning: Could not save chart data: {e}")
    
    print("✅ Analysis complete!")
    return result

if __name__ == "__main__":
    run()
