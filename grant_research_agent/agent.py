"""
Grant Research Agent

A comprehensive grant research assistant that helps researchers find, analyze,
and apply for grants using specialized sub-agents.
"""

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from grant_research_agent import prompt
from grant_research_agent.sub_agents.grant_search.agent import grant_search_agent
from grant_research_agent.sub_agents.eligibility_checker.agent import eligibility_checker_agent
from grant_research_agent.sub_agents.proposal_analyzer.agent import proposal_analyzer_agent
from grant_research_agent.sub_agents.deadline_tracker.agent import deadline_tracker_agent


def _load_grant_research_context(callback_context: CallbackContext):
    """Load initial grant research context and preferences."""
    if not callback_context.state:
        callback_context.state = {}
    
    # Initialize grant research state
    callback_context.state.setdefault("grant_preferences", {
        "research_areas": [],
        "funding_range": {"min": 0, "max": 1000000},
        "organization_type": "academic",
        "career_stage": "early_career",
        "geographic_focus": "us",
        "current_applications": [],
        "deadlines_tracking": []
    })
    
    callback_context.state.setdefault("search_history", [])
    callback_context.state.setdefault("eligibility_assessments", [])
    callback_context.state.setdefault("proposal_reviews", [])
    callback_context.state.setdefault("deadline_alerts", [])
    
    print(f"Grant Research Agent initialized with user preferences: {callback_context.state.get('grant_preferences', {})}")


root_agent = Agent(
    model="gemini-2.5-flash",
    name="grant_research_agent",
    description="A comprehensive Grant Research Assistant that coordinates multiple specialized sub-agents to help researchers find, analyze, and apply for grants",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        grant_search_agent,
        eligibility_checker_agent,
        proposal_analyzer_agent,
        deadline_tracker_agent,
    ],
    before_agent_callback=_load_grant_research_context,
)
