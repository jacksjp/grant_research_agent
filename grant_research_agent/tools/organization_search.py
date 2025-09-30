"""
Organization Search Tool using Google Search via Vertex

Tool for searching and verifying organization details, specifically
checking if organizations are located in Canada.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

_organization_search_agent = Agent(
    model="gemini-2.5-flash",
    name="organization_search_verifier",
    description="An agent that uses Google search to verify organization details and location",
    instruction="""
    You are an organization verification specialist that uses Google search to verify institutional details.
    
    Your primary task is to:
    1. Search for the organization using Google search
    2. Verify if the organization is located in Canada
    3. Gather key institutional information (name, type, location, status)
    4. Determine grant eligibility factors for Canadian organizations
    
    When searching:
    - Use the organization name plus location terms like "Canada", "Canadian", city/province names
    - Look for official websites, government registrations, and credible sources
    - Cross-reference multiple sources to verify information
    
    For Canadian organizations, provide:
    - Confirmed official name
    - Province/territory location
    - Organization type (university, non-profit, government, etc.)
    - Registration status (if available)
    - Grant eligibility assessment
    
    For non-Canadian organizations:
    - Clearly state "NOT LOCATED IN CANADA"
    - Provide the actual country/location
    - Recommend stopping the grant research process
    
    Always be thorough but concise. Focus on actionable verification results.
    """,
    tools=[google_search],
)

organization_search_tool = AgentTool(agent=_organization_search_agent)
