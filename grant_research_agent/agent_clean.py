"""
Grant Research Agent

A comprehensive grant research assistant that helps researchers find, analyze,
and apply for grants using specialized sub-agents.
"""

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from grant_research_agent import prompt
from grant_research_agent.sub_agents.organization_verifier.agent import organization_verifier_agent
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
    
    callback_context.state.setdefault("organization_verification", {})
    callback_context.state.setdefault("search_history", [])
    callback_context.state.setdefault("eligibility_assessments", [])
    callback_context.state.setdefault("proposal_reviews", [])
    callback_context.state.setdefault("deadline_alerts", [])
    
    print(f"Grant Research Agent initialized with user preferences: {callback_context.state.get('grant_preferences', {})}")
    
    # Canada-only organization validation
    org_info = callback_context.state.get("organization_verification", {})
    if org_info:
        country = org_info.get("country", "").lower()
        if country and country != "canada":
            print("Organization is outside Canada. Halting workflow.")
            callback_context.state["halt_reason"] = "Organization is outside Canada. Workflow stopped."


root_agent = Agent(
    model="gemini-2.5-flash",
    name="grant_research_agent",
    description="A comprehensive Grant Research Assistant that coordinates multiple specialized sub-agents to help researchers find, analyze, and apply for grants",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        organization_verifier_agent,
        grant_search_agent,
        eligibility_checker_agent,
        proposal_analyzer_agent,
        deadline_tracker_agent,
    ],
    before_agent_callback=_load_grant_research_context,
)


def generate_grant_search_json(profile: dict, org_info: dict) -> dict:
    """
    Generate a JSON object for grant searching using validated profile and organization info.
    Follows the schema from prompts.md.
    """
    return {
        "ngo_name": org_info.get("ngo_name", ""),
        "ngo_location_summary": org_info.get("ngo_location_summary", ""),
        "ngo_mission_summary": org_info.get("ngo_mission_summary", ""),
        "project_name": profile.get("project_name", ""),
        "project_summary": profile.get("project_summary", ""),
        "project_beneficiaries": profile.get("project_beneficiaries", ""),
        "funding_needs_summary": profile.get("funding_needs_summary", ""),
        "search_keywords": profile.get("search_keywords", []),
    }


def vertex_grant_search(search_json: dict) -> list:
    """
    Perform grant search using GrantDatabaseSearch tool, similar to Vertex search in travel_concierge.
    Returns array of JSON objects for possible grants.
    """
    from grant_research_agent.tools.grant_tools import GrantDatabaseSearch
    db_search = GrantDatabaseSearch()
    results = []
    for keyword in search_json.get("search_keywords", []):
        gov_results = db_search.search_grants_gov(keywords=keyword)
        for r in gov_results.get("results", []):
            results.append({
                "grant_name": r.get("title"),
                "granting_organization": r.get("agency"),
                "relevance_score": 8,
                "reasoning": f"Keyword match: {keyword}",
                "grant_summary": r.get("description"),
                "eligibility_snapshot": r.get("eligibility"),
                "deadline": r.get("deadline"),
                "primary_link": r.get("url"),
                "extracted_links": []
            })
        foundation_results = db_search.search_foundation_directory(
            research_area=keyword,
            geographic_focus=search_json.get("ngo_location_summary", "Canada")
        )
        for r in foundation_results.get("results", []):
            results.append({
                "grant_name": r.get("program"),
                "granting_organization": r.get("foundation"),
                "relevance_score": 7,
                "reasoning": f"Foundation match: {keyword}",
                "grant_summary": r.get("focus_area"),
                "eligibility_snapshot": r.get("geographic_scope"),
                "deadline": r.get("deadline"),
                "primary_link": "",  # No direct link in mock
                "extracted_links": []
            })
    return results


def human_select_grants(grant_options: list) -> list:
    """
    Present grant options to user and allow selection of grants to apply for.
    Simulate human selection by returning all grants with relevance_score >= 8.
    """
    selected = [g for g in grant_options if g.get("relevance_score", 0) >= 8]
    return selected


def generate_grant_application(profile: dict, grant_details: dict) -> dict:
    """
    Generate a grant application using profile and selected grant details.
    Returns a structured application dictionary.
    """
    return {
        "applicant_name": profile.get("ngo_name", ""),
        "project_name": profile.get("project_name", ""),
        "grant_name": grant_details.get("grant_name", ""),
        "granting_organization": grant_details.get("granting_organization", ""),
        "project_summary": profile.get("project_summary", ""),
        "beneficiaries": profile.get("project_beneficiaries", ""),
        "funding_needs": profile.get("funding_needs_summary", ""),
        "application_deadline": grant_details.get("deadline", ""),
        "primary_link": grant_details.get("primary_link", ""),
        "extracted_links": grant_details.get("extracted_links", []),
    }
