"""
Organization Verifier Sub-Agent

Specialized agent for verifying and validating organization details
for grant research and eligibility assessment using Google search.
"""

from google.adk.agents import Agent
from grant_research_agent.prompt import ORGANIZATION_VERIFIER_INSTR
from grant_research_agent.tools.organization_search import organization_search_tool


organization_verifier_agent = Agent(
    model="gemini-2.5-flash",
    name="organization_verifier_agent",
    description="Specialized agent for organization verification, institutional details validation, and eligibility pre-screening using Google search",
    instruction=ORGANIZATION_VERIFIER_INSTR,
    tools=[organization_search_tool],
)
