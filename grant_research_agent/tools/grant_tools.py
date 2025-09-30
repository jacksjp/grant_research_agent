"""
Grant Database Search Tools

Tools for searching and retrieving information from various grant databases
and funding sources.
"""

from typing import Dict, List, Any
import json


class GrantDatabaseSearch:
    """Tool for searching grant databases."""
    
    def __init__(self):
        """Initialize the grant database search tool."""
        self.name = "grant_database_search"
        self.description = "Search various grant databases for funding opportunities"
    
    def search_grants_gov(self, keywords: str, category: str = None, 
                         amount_min: int = None, amount_max: int = None) -> Dict[str, Any]:
        """Search the grants.gov database."""
        # This would integrate with actual grants.gov API
        results = {
            "source": "grants.gov",
            "query": keywords,
            "filters": {
                "category": category,
                "amount_min": amount_min,
                "amount_max": amount_max
            },
            "results": [
                {
                    "title": "NSF Research in Artificial Intelligence",
                    "agency": "National Science Foundation",
                    "opportunity_number": "NSF-25-001",
                    "amount": "$100,000 - $500,000",
                    "deadline": "2026-03-15",
                    "description": f"Research opportunities in {keywords} and related AI fields",
                    "eligibility": "Academic institutions, research organizations",
                    "url": "https://grants.gov/view-opportunity.html?oppId=12345"
                },
                {
                    "title": "NIH Innovative Research in Biomedical Sciences",
                    "agency": "National Institutes of Health",
                    "opportunity_number": "NIH-25-002",
                    "amount": "$250,000 - $750,000",
                    "deadline": "2026-02-05",
                    "description": f"Biomedical research including {keywords} applications",
                    "eligibility": "Universities, medical schools, research institutes",
                    "url": "https://grants.gov/view-opportunity.html?oppId=12346"
                }
            ],
            "total_found": 2
        }
        return results
    
    def search_foundation_directory(self, research_area: str, 
                                  geographic_focus: str = None) -> Dict[str, Any]:
        """Search foundation grant directories."""
        results = {
            "source": "foundation_directory",
            "query": research_area,
            "filters": {
                "geographic_focus": geographic_focus
            },
            "results": [
                {
                    "foundation": "Gates Foundation",
                    "program": "Grand Challenges in Global Health",
                    "amount": "$100,000 - $1,000,000",
                    "focus_area": f"Global health applications of {research_area}",
                    "deadline": "Rolling basis",
                    "geographic_scope": "Global",
                    "contact": "grants@gatesfoundation.org"
                },
                {
                    "foundation": "Alfred P. Sloan Foundation",
                    "program": "Research Fellowships",
                    "amount": "$75,000 over 2 years",
                    "focus_area": f"Early career research in {research_area}",
                    "deadline": "2026-06-15",
                    "geographic_scope": "United States",
                    "contact": "fellowships@sloan.org"
                }
            ],
            "total_found": 2
        }
        return results


class ProposalTemplateGenerator:
    """Tool for generating proposal templates and outlines."""
    
    def __init__(self):
        """Initialize the proposal template generator."""
        self.name = "proposal_template_generator"
        self.description = "Generate proposal templates based on grant type and requirements"
    
    def generate_nsf_template(self, program: str = "General") -> Dict[str, Any]:
        """Generate NSF proposal template."""
        template = {
            "grant_type": "NSF",
            "program": program,
            "sections": [
                {
                    "section": "Project Summary",
                    "page_limit": 1,
                    "requirements": [
                        "Overview of proposed work",
                        "Statement of intellectual merit",
                        "Statement of broader impacts"
                    ],
                    "tips": [
                        "Write for a broad scientific audience",
                        "Clearly state the problem and approach",
                        "Emphasize transformative potential"
                    ]
                },
                {
                    "section": "Project Description",
                    "page_limit": 15,
                    "subsections": [
                        "Introduction and Background",
                        "Research Plan",
                        "Methodology",
                        "Timeline and Milestones",
                        "Expected Outcomes",
                        "Broader Impacts"
                    ],
                    "requirements": [
                        "Clear research objectives",
                        "Detailed methodology",
                        "Timeline with milestones",
                        "Risk assessment and mitigation"
                    ]
                },
                {
                    "section": "References Cited",
                    "page_limit": "No limit",
                    "requirements": [
                        "Complete bibliographic information",
                        "Include URLs for public access"
                    ]
                },
                {
                    "section": "Biographical Sketches",
                    "page_limit": "2 pages per person",
                    "requirements": [
                        "Education and training",
                        "Research and professional experience",
                        "Publications (10 most relevant)",
                        "Synergistic activities"
                    ]
                },
                {
                    "section": "Budget and Budget Justification",
                    "requirements": [
                        "Personnel costs with effort percentages",
                        "Equipment justification",
                        "Travel justification",
                        "Indirect costs calculation"
                    ]
                }
            ],
            "formatting": {
                "font": "Computer Modern, Palatino, Times, or TeX-Gyre Termes",
                "font_size": "10-point or larger",
                "margins": "1 inch on all sides",
                "line_spacing": "Single-spaced text"
            }
        }
        return template
    
    def generate_nih_template(self, mechanism: str = "R01") -> Dict[str, Any]:
        """Generate NIH proposal template."""
        template = {
            "grant_type": "NIH",
            "mechanism": mechanism,
            "sections": [
                {
                    "section": "Specific Aims",
                    "page_limit": 1,
                    "requirements": [
                        "Clear statement of goals",
                        "Specific, measurable objectives",
                        "Hypothesis to be tested",
                        "Rationale and significance"
                    ],
                    "tips": [
                        "Start with a compelling hook",
                        "State the problem clearly",
                        "Present your solution/approach",
                        "End with expected impact"
                    ]
                },
                {
                    "section": "Research Strategy",
                    "page_limit": 12,
                    "subsections": [
                        "Significance",
                        "Innovation",
                        "Approach"
                    ],
                    "requirements": [
                        "Significance: Importance to health/science",
                        "Innovation: Novel concepts, approaches, methods",
                        "Approach: Detailed experimental plan"
                    ]
                },
                {
                    "section": "Bibliography & References Cited",
                    "requirements": [
                        "Complete citations",
                        "No page limit"
                    ]
                }
            ],
            "review_criteria": [
                "Significance",
                "Investigator(s)",
                "Innovation", 
                "Approach",
                "Environment"
            ],
            "formatting": {
                "font": "Arial, Georgia, Helvetica, or Palatino Linotype",
                "font_size": "11-point or larger",
                "margins": "0.5 inch minimum",
                "line_spacing": "No requirements"
            }
        }
        return template


class GrantCalendar:
    """Tool for managing grant deadlines and calendars."""
    
    def __init__(self):
        """Initialize the grant calendar tool."""
        self.name = "grant_calendar"
        self.description = "Manage grant deadlines and application calendars"
    
    def get_federal_deadlines(self, fiscal_year: int = 2026) -> Dict[str, Any]:
        """Get standard federal grant deadlines."""
        deadlines = {
            "fiscal_year": fiscal_year,
            "standard_deadlines": {
                "NSF": [
                    {"program": "CAREER", "deadline": "2026-02-19", "frequency": "Annual"},
                    {"program": "General Research", "deadline": "Rolling", "frequency": "Continuous"},
                    {"program": "SBIR Phase I", "deadline": "2025-11-15", "frequency": "Multiple per year"}
                ],
                "NIH": [
                    {"program": "R01", "deadline": "2026-02-05", "frequency": "3 times per year"},
                    {"program": "R21", "deadline": "2026-02-16", "frequency": "3 times per year"},
                    {"program": "F31 NRSA", "deadline": "2026-04-08", "frequency": "3 times per year"}
                ],
                "DOE": [
                    {"program": "Early Career", "deadline": "2026-01-30", "frequency": "Annual"},
                    {"program": "SBIR", "deadline": "2025-12-10", "frequency": "Annual"}
                ]
            },
            "special_programs": [
                {
                    "name": "Fulbright Scholar Program",
                    "deadline": "2026-04-01",
                    "description": "International research opportunities"
                },
                {
                    "name": "Guggenheim Fellowship",
                    "deadline": "2025-09-15",
                    "description": "Artists and scholars fellowship"
                }
            ]
        }
        return deadlines
    
    def create_application_schedule(self, deadlines: List[str], 
                                  preparation_weeks: int = 12) -> Dict[str, Any]:
        """Create an application preparation schedule."""
        schedule = {
            "preparation_period": f"{preparation_weeks} weeks",
            "milestones": [
                {
                    "week": preparation_weeks,
                    "milestone": "Project conception and team assembly",
                    "deliverables": ["Research plan outline", "Team commitments"]
                },
                {
                    "week": preparation_weeks - 2,
                    "milestone": "Literature review and background research",
                    "deliverables": ["Comprehensive literature review", "Gap analysis"]
                },
                {
                    "week": preparation_weeks - 4,
                    "milestone": "Methodology development",
                    "deliverables": ["Detailed methodology", "Timeline", "Risk assessment"]
                },
                {
                    "week": preparation_weeks - 6,
                    "milestone": "Budget development",
                    "deliverables": ["Detailed budget", "Budget justification"]
                },
                {
                    "week": preparation_weeks - 8,
                    "milestone": "First draft completion",
                    "deliverables": ["Complete first draft", "All required sections"]
                },
                {
                    "week": preparation_weeks - 10,
                    "milestone": "Internal review",
                    "deliverables": ["Review feedback", "Revision plan"]
                },
                {
                    "week": preparation_weeks - 11,
                    "milestone": "Second draft and revisions",
                    "deliverables": ["Revised draft", "Improved sections"]
                },
                {
                    "week": preparation_weeks - 12,
                    "milestone": "Final preparation",
                    "deliverables": ["Final draft", "Compliance check", "Submission materials"]
                }
            ],
            "weekly_tasks": [
                "Progress review meeting",
                "Deliverable completion check",
                "Next week planning",
                "Risk assessment update"
            ]
        }
        return schedule


# Export tools for use in agents
__all__ = ['GrantDatabaseSearch', 'ProposalTemplateGenerator', 'GrantCalendar']
