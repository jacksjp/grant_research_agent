"""
Eligibility Checker Sub-Agent

Specialized agent for assessing eligibility for grants based on various criteria.
"""

from google.adk.agents import Agent
from grant_research_agent.prompt import ELIGIBILITY_CHECKER_INSTR


eligibility_checker_agent = Agent(
    model="gemini-2.5-flash", 
    name="eligibility_checker_agent",
    description="Specialized agent for checking grant eligibility based on organization, researcher, and project criteria",
    instruction=ELIGIBILITY_CHECKER_INSTR,
)
