#!/usr/bin/env python3
"""
Grant Research Agent Example

This script demonstrates how to use the Grant Research Agent system 
for comprehensive grant research and application assistance.
"""

import os
from dotenv import load_dotenv
from google.adk.core import Session
from grant_research_agent.agent import root_agent

# Load environment variables
load_dotenv()

def main():
    """Main demonstration of the Grant Research Agent."""
    print("=== Grant Research Agent Demo ===\n")
    
    # Initialize session
    session = Session()
    
    # Example research scenarios
    examples = [
        {
            "title": "NSF CAREER Award Research",
            "query": "I'm an early-career faculty member in computer science looking for NSF CAREER award opportunities. Can you help me find relevant grants, check my eligibility, and understand the application timeline?"
        },
        {
            "title": "NIH Medical Research Grant",
            "query": "I need funding for biomedical research on cancer treatments. Can you search for NIH grants, analyze proposal requirements, and help track deadlines?"
        },
        {
            "title": "Multi-Grant Strategy Planning",
            "query": "I want to develop a comprehensive funding strategy with multiple grant applications over the next year. Can you help prioritize opportunities and manage deadlines?"
        }
    ]
    
    print("Grant Research Agent Capabilities:")
    print("1. Grant Search & Discovery")
    print("2. Eligibility Assessment") 
    print("3. Proposal Analysis & Templates")
    print("4. Deadline Tracking & Timeline Management")
    print("5. Multi-grant Strategy Coordination")
    print("\n" + "="*50 + "\n")
    
    # Show example usage patterns
    for i, example in enumerate(examples, 1):
        print(f"Example {i}: {example['title']}")
        print(f"Query: {example['query']}")
        print("-" * 40)
        
        # Note: In a real implementation, you would call:
        # response = root_agent.run(query=example['query'], session=session)
        # print(f"Response: {response}")
        
        print("The agent would coordinate its sub-agents to:")
        print("- Search grant databases for relevant opportunities")
        print("- Check eligibility requirements and criteria")
        print("- Analyze proposal requirements and templates")
        print("- Create timeline and deadline management plan")
        print("- Provide comprehensive research strategy")
        print("\n")
    
    print("To use the Grant Research Agent:")
    print("1. Ensure your Google Cloud credentials are configured")
    print("2. Import the root_agent from grant_research_agent.agent")
    print("3. Create a Session and call root_agent.run() with your query")
    print("4. The orchestrator will coordinate all sub-agents automatically")
    print("\nExample Code:")
    print("""
from google.adk.core import Session
from grant_research_agent.agent import root_agent

session = Session()
response = root_agent.run(
    query="Help me find NSF grants for AI research",
    session=session
)
print(response)
""")
    
    # Display system architecture
    print("\n" + "="*50)
    print("GRANT RESEARCH AGENT ARCHITECTURE")
    print("="*50)
    print("""
Main Orchestrator (grant_research_agent)
├── Grant Search Agent
│   ├── Database search (NSF, NIH, private foundations)
│   ├── Keyword and category filtering
│   └── Opportunity ranking and recommendations
│
├── Eligibility Checker Agent  
│   ├── Requirement analysis and matching
│   ├── Institutional eligibility verification
│   └── PI qualification assessment
│
├── Proposal Analyzer Agent
│   ├── Requirement breakdown and templates
│   ├── Section-by-section guidance
│   └── Best practices and examples
│
└── Deadline Tracker Agent
    ├── Timeline creation and management
    ├── Milestone tracking and alerts
    └── Multi-application coordination
""")
    
    print("\nAll agents use the Google ADK framework with Gemini 2.5 Flash")
    print("for intelligent coordination and comprehensive grant research assistance.")

if __name__ == "__main__":
    main()
