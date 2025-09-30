# Grant Research Agent - User Documentation

## Overview

The Grant Research Agent is a comprehensive Streamlit-based application that helps Canadian organizations find, analyze, and apply for grants through a guided 4-step workflow. The system integrates with Google's Agent Development Kit (ADK) to provide intelligent verification and validation services.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Getting Started](#getting-started)
3. [User Interface Guide](#user-interface-guide)
4. [Workflow Steps](#workflow-steps)
5. [ADK Integration](#adk-integration)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)
8. [Technical Details](#technical-details)

---

## System Architecture

### Core Components

```
Grant Research Agent
├── Streamlit UI (grant_research_app.py)
├── ADK Integration Layer
├── Sub-Agents
│   ├── Organization Verifier
│   ├── Grant Search
│   ├── Eligibility Checker
│   ├── Proposal Analyzer
│   └── Deadline Tracker
└── Tools & Validation
    ├── Canada Location Validator
    ├── Organization Search Tool
    └── Application Generator
```

### Key Features

| Feature | Description |
| --- | --- |
| **Interaction Type** | Web-based GUI with step-by-step workflow |
| **Complexity** | Advanced multi-agent coordination |
| **Agent Type** | Multi-Agent with specialized sub-agents |
| **Components** | Tools, AgentTools, Validation, Export |
| **Geographic Focus** | Canada-only organizations |
| **Export Format** | Structured text application drafts |

---

## Getting Started

### Prerequisites

1. **Python Environment**: Poetry-managed Python 3.12+ environment
2. **ADK Setup**: Google Agent Development Kit configured
3. **Environment Variables**: ADK endpoint configuration

### Installation

```bash
# Navigate to project directory
cd c:\Hackaton\travel-concierge

# Install dependencies with Poetry
poetry install

# Set up environment variables
# Create .env file with:
ADK_ENDPOINT=http://127.0.0.1:8080
```

### Running the Application

```bash
# Start the Streamlit application
poetry run streamlit run grant_research_app.py

# Access the application
# Default: http://localhost:8501
```

---

## User Interface Guide

### Main Interface Layout

```
🇨🇦 Grant Research Agent
Canada-Focused Grant Research with Human-in-the-Loop

[Progress Bar: Step X of 4]
[Current Step Title and Description]

[Main Content Area]
- Form inputs for current step
- Validation results
- Action buttons

[Sidebar]
├── 📊 Workflow Summary
├── 📄 Final Application Export
├── 🔧 Debug Mode Toggle
└── 🔗 Connection Status
```

### Navigation Elements

- **Progress Bar**: Visual indicator of workflow completion
- **Step Counter**: Shows current position (Step X of 4)
- **Navigation Buttons**: Step-specific proceed/back options
- **Reset Option**: Restart workflow from beginning

---

## Workflow Steps

### Step 1: Organization Verification 🏛️

**Purpose**: Verify your organization is located in Canada and eligible for Canadian grants.

**Required Information**:
- Organization Name (e.g., "University of Toronto")
- Organization Type (University, College, Research Institute, Non-profit, Government Agency, Hospital)
- Location (City and province in Canada)
- Primary Research Areas (optional multi-select)

**Validation Process**:
1. **ADK Agent Verification**: Calls organization_verifier_agent for comprehensive validation
2. **Canada Location Validation**: Uses intelligent heuristics to confirm Canadian location
3. **Manual Override**: Option to manually confirm Canadian location if automated validation fails

**Validation Confidence Levels**:
- **High**: Location explicitly mentions Canada or Canadian province/territory
- **Medium**: Location mentions major Canadian city
- **Low**: No clear Canadian indicators found

**Example Valid Locations**:
- "Toronto, Ontario, Canada"
- "Montreal, Quebec"
- "Vancouver, British Columbia"
- "Calgary, Alberta"

**Outputs**:
- Organization verification status
- Canada location confirmation
- Institutional details validation

### Step 2: Grant Information 📄

**Purpose**: Provide details about the specific grant you're interested in.

**Input Methods**:

#### Option A: Describe Grant
- **Text Area**: Large text field for grant description
- **Recommended Content**:
  - Grant name and funder
  - Eligibility requirements
  - Funding amount and range
  - Application deadline
  - Focus areas and priorities
  - Special requirements or criteria

#### Option B: Upload File
- **Supported Formats**: PDF, TXT, DOCX
- **File Processing**: Automatic content extraction and preview
- **File Information**: Name, type, size stored for reference

**State Management**:
- Persistent text content across mode switches
- File object retention until submission
- Debug information for troubleshooting

**Outputs**:
- Structured grant information storage
- Method tracking (description vs. file upload)
- Content preview and validation

### Step 3: Eligibility Check ✅

**Purpose**: Verify your organization meets the grant requirements.

**Assessment Factors**:
- Located in Canada ✓
- Registered non-profit or educational institution
- Has research capacity
- Meets minimum funding requirements
- Within grant's target sectors

**Validation Logic**:
- **Minimum Threshold**: 3+ factors required
- **Canada Location**: Mandatory requirement
- **Eligibility Score**: Based on number of confirmed factors

**Results**:
- **Eligible**: 3+ factors including Canada location
- **Not Eligible**: <3 factors or missing Canada requirement
- **Conditional**: Additional review recommended

**Outputs**:
- Eligibility determination
- Factors assessment summary
- Recommendation for next steps

### Step 4: Project Description & Suggestions 🎯

**Purpose**: Describe your project and receive qualification suggestions.

**Project Information Required**:

#### Basic Details
- **Project Title**: Clear, descriptive title
- **Project Description**: Comprehensive project overview including:
  - Objectives and goals
  - Methodology and approach
  - Expected outcomes
  - Timeline considerations
  - Budget considerations

#### Project Specifications
- **Requested Funding**: Amount in CAD (minimum $1,000)
- **Project Duration**: 6 months, 1 year, 2 years, or 3 years
- **Primary Research Area**: Main focus (e.g., AI, Health, Climate)
- **Team Size**: Number of team members

**Qualification Suggestions**:
Upon submission, the system provides strategic recommendations:

1. ✅ Ensure project timeline aligns with grant reporting requirements
2. 📊 Include detailed budget breakdown with justifications
3. 🤝 Consider partnerships with other institutions to strengthen application
4. 📚 Highlight previous relevant research experience and publications
5. 🎯 Clearly articulate the impact and benefits of your research
6. 📋 Prepare all required documentation well before the deadline

**Outputs**:
- Complete project profile
- Customized suggestions list
- Application readiness assessment

---

## ADK Integration

### Architecture Overview

The application integrates with Google's Agent Development Kit (ADK) through a multi-layered approach:

```
Streamlit UI
    ↓
ADK Integration Layer (grant_research_app.py)
    ↓
Root Agent (grant_research_agent/agent.py)
    ↓
Sub-Agents (specialized agents)
    ↓
Tools & External APIs
```

### ADK Agents

#### Root Agent
- **Model**: gemini-2.5-flash
- **Name**: grant_research_agent
- **Purpose**: Coordinates multiple specialized sub-agents
- **Context Management**: Loads grant research context and preferences

#### Sub-Agents

1. **Organization Verifier Agent**
   - **Purpose**: Verify and validate organization details
   - **Tools**: Google Search integration
   - **Focus**: Institutional legitimacy and Canadian location

2. **Grant Search Agent**
   - **Purpose**: Find relevant grants based on criteria
   - **Capabilities**: Database search and filtering

3. **Eligibility Checker Agent**
   - **Purpose**: Assess organization eligibility for specific grants
   - **Analysis**: Requirements matching and gap identification

4. **Proposal Analyzer Agent**
   - **Purpose**: Review and improve grant proposals
   - **Features**: Content analysis and enhancement suggestions

5. **Deadline Tracker Agent**
   - **Purpose**: Monitor application deadlines and milestones
   - **Alerts**: Timeline management and reminders

### Canada Validation System

#### Intelligent Heuristics
The system uses comprehensive location validation:

```python
# Canadian provinces and territories
provinces = [
    "ontario", "quebec", "british columbia", "alberta", 
    "manitoba", "saskatchewan", "nova scotia", "new brunswick",
    "prince edward island", "pei", "newfoundland", "labrador",
    "yukon", "nunavut", "northwest territories"
]

# Major Canadian cities
major_cities = [
    "toronto", "montreal", "vancouver", "calgary", "ottawa",
    "edmonton", "winnipeg", "halifax", "mississauga", "brampton",
    "hamilton", "london", "kitchener", "windsor", "regina",
    "saskatoon", "st. johns", "fredericton", "charlottetown",
    "victoria", "whitehorse", "yellowknife", "iqaluit"
]
```

#### Validation Logic
1. **Explicit Canada Check**: Searches for "canada" in location string
2. **Province/Territory Check**: Matches against provincial names
3. **Major City Check**: Identifies major Canadian cities
4. **Confidence Scoring**: High/Medium/Low based on match type

---

## Configuration

### Environment Variables

```bash
# .env file configuration
ADK_ENDPOINT=http://127.0.0.1:8080  # ADK server endpoint
DEBUG_MODE=false                     # Enable debug logging
```

### ADK Connection

The application automatically tests ADK connectivity:

- **Endpoint Test**: HTTP GET to root endpoint
- **Status Codes**: 200 or 307 (redirect) indicate success
- **Fallback Mode**: Intelligent mock responses when ADK unavailable
- **Connection Display**: Real-time status in sidebar

### Session Configuration

```python
# Automatic session initialization
session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
```

---

## Export and Output

### Application Document Generation

The system generates structured grant application drafts:

#### Document Structure
```
Grant Application Draft - Generated [Timestamp]
===============================================

[1] Organization Verification
Name: [Organization Name]
Location: [Location]
Type: [Organization Type]
Canada Verified: Yes/No
Research Areas: [List]

[2] Grant Information
Provided: Description/File Upload
[Grant Details or File Reference]

[3] Eligibility Assessment
Status: Eligible/Conditional
Factors Confirmed: [List]

[4] Project Description
Title: [Project Title]
Funding Requested: [Amount] CAD
Duration: [Duration]
Research Area: [Area]
Team Size: [Number]
Description: [Full Description]

[5] Qualification Suggestions
[Generated recommendations]

---
Status: [Completion Summary]
```

#### Export Options
- **Text Format**: Plain text (.txt) download
- **Filename**: `grant_application_[session_id].txt`
- **Content**: Complete application draft with all collected data

---

## Troubleshooting

### Common Issues

#### ADK Connection Problems
**Symptoms**: "❌ Cannot connect to ADK" message
**Solutions**:
1. Verify ADK server is running on specified endpoint
2. Check `ADK_ENDPOINT` environment variable
3. Ensure network connectivity to ADK server
4. Review firewall settings

#### Canada Validation Failures
**Symptoms**: Organization not recognized as Canadian
**Solutions**:
1. Include province name in location field
2. Add "Canada" to location string
3. Use manual override checkbox
4. Verify location spelling

#### Form Data Loss
**Symptoms**: Information disappears when switching between options
**Solutions**:
1. Submit forms before changing modes
2. Use browser back button instead of refresh
3. Enable debug mode for state inspection

#### File Upload Issues
**Symptoms**: Files not processing correctly
**Solutions**:
1. Use supported formats (PDF, TXT, DOCX)
2. Check file size limitations
3. Ensure file is not corrupted
4. Try text description instead

### Debug Mode

Enable debug mode through the sidebar checkbox for:
- **State Inspection**: View session state data
- **API Responses**: See raw ADK responses
- **Validation Details**: Detailed validation reasoning
- **Error Messages**: Enhanced error information

### Support Features

#### Connection Test
- **Button**: "🔄 Test ADK Connection" in sidebar
- **Purpose**: Verify ADK connectivity on demand
- **Results**: Real-time connection status display

#### Raw Data View
- **Location**: Debug expander in sidebar
- **Content**: JSON view of all workflow data
- **Usage**: Troubleshooting and state verification

---

## Technical Details

### Technology Stack
- **Frontend**: Streamlit 
- **Backend**: Python 3.12+
- **AI Integration**: Google ADK with Gemini models
- **Package Management**: Poetry
- **Environment**: .env configuration

### Dependencies
```toml
[tool.poetry.dependencies]
python = "^3.12"
streamlit = "^1.28.0"
google-adk = "*"
requests = "^2.31.0"
python-dotenv = "^1.0.0"
```

### File Structure
```
grant_research_agent/
├── grant_research_app.py          # Main Streamlit application
├── grant_research_agent/
│   ├── agent.py                   # Root ADK agent
│   ├── prompt.py                  # Agent instructions
│   ├── sub_agents/                # Specialized agents
│   │   ├── organization_verifier/
│   │   ├── grant_search/
│   │   ├── eligibility_checker/
│   │   ├── proposal_analyzer/
│   │   └── deadline_tracker/
│   └── tools/                     # Agent tools
├── pyproject.toml                 # Poetry configuration
├── .env                          # Environment variables
└── README.md                     # Project documentation
```

### Session State Management
```python
# Key session state variables
st.session_state.current_step      # Workflow position (1-4)
st.session_state.workflow_data     # All collected data
st.session_state.debug_mode        # Debug toggle
st.session_state.session_id        # Unique session identifier
```

### Data Flow
1. **User Input** → Form submission
2. **Validation** → ADK agent processing
3. **Storage** → Session state management
4. **Navigation** → Step progression
5. **Export** → Document generation

---

## Best Practices

### For Users
1. **Complete Information**: Provide detailed, accurate organization information
2. **Location Clarity**: Include province and "Canada" in location field
3. **Grant Details**: Be comprehensive in grant descriptions
4. **Save Progress**: Complete each step before navigating
5. **Export Early**: Generate application documents at completion

### For Administrators
1. **ADK Monitoring**: Ensure ADK server availability
2. **Environment Management**: Keep environment variables updated
3. **Debug Utilization**: Use debug mode for troubleshooting
4. **Regular Testing**: Verify connection status regularly

### For Developers
1. **Error Handling**: Comprehensive exception management
2. **State Persistence**: Maintain session state integrity
3. **Validation Logic**: Robust input validation
4. **Documentation**: Keep documentation updated with changes

---

## Future Enhancements

### Planned Features
- **Dynamic Suggestions**: LLM-generated suggestions based on specific grant requirements
- **Enhanced Export**: PDF and Markdown format options
- **Advanced Search**: Integration with grant databases
- **Deadline Integration**: Automated deadline tracking and alerts
- **Collaboration**: Multi-user application development

### Integration Opportunities
- **Grant Databases**: Direct integration with funding databases
- **Institution APIs**: Automated organization verification
- **Document Management**: Integration with document management systems
- **Notification Systems**: Email and SMS alerts for deadlines

---

*This documentation covers the Grant Research Agent as of September 30, 2025. For technical support or feature requests, please contact the development team.*
