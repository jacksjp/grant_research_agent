"""
Proposal Analyzer Sub-Agent

Specialized agent for analyzing grant proposals and providing feedback.
"""

from google.adk.agents import Agent
from grant_research_agent.prompt import PROPOSAL_ANALYZER_INSTR


proposal_analyzer_agent = Agent(
    model="gemini-2.5-flash",
    name="proposal_analyzer_agent", 
    description="Specialized agent for analyzing grant proposals, checking compliance, and providing improvement recommendations",
    instruction=PROPOSAL_ANALYZER_INSTR,
)
