"""
Grant Search Sub-Agent

Specialized agent for discovering and searching grants based on various criteria.
"""

from google.adk.agents import Agent
from grant_research_agent.prompt import GRANT_SEARCH_INSTR


grant_search_agent = Agent(
    model="gemini-2.5-flash",
    name="grant_search_agent",
    description="Specialized agent for discovering and searching grant opportunities based on research criteria",
    instruction=GRANT_SEARCH_INSTR,
)
