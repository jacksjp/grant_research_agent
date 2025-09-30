"""
Deadline Tracker Sub-Agent

Specialized agent for tracking grant deadlines and managing application timelines.
"""

from google.adk.agents import Agent
from grant_research_agent.prompt import DEADLINE_TRACKER_INSTR


deadline_tracker_agent = Agent(
    model="gemini-2.5-flash",
    name="deadline_tracker_agent",
    description="Specialized agent for tracking grant deadlines, managing timelines, and coordinating multiple applications", 
    instruction=DEADLINE_TRACKER_INSTR,
)
