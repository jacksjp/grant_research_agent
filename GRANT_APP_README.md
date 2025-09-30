# Grant Research Agent Streamlit App

A comprehensive Streamlit application that provides an interactive interface for the Grant Research Agent with human-in-the-loop functionality at each step of the grant research process.

## Features

🔍 **Grant Discovery**: Search for relevant funding opportunities across multiple agencies  
✅ **Eligibility Assessment**: Check qualification requirements for selected grants  
📝 **Proposal Analysis**: Analyze proposal requirements and create templates  
⏰ **Timeline Planning**: Create application timeline and deadline management  
👤 **Human-in-the-Loop**: Manual approval and review at each critical step  
📊 **Progress Tracking**: Visual workflow progress and step completion status  
📥 **Export Results**: Download complete grant research reports  

## Workflow Steps

1. **Research Context Setup**: Define research areas, funding needs, and preferences
2. **Grant Discovery**: AI-powered search for relevant funding opportunities
3. **Eligibility Assessment**: Automated checking of qualification requirements
4. **Proposal Analysis**: Detailed breakdown of application requirements
5. **Timeline Planning**: Creation of realistic application schedules
6. **Final Review**: Comprehensive strategy review and export

## Human-in-the-Loop Features

At each step, the application requires human approval and review:

- ✅ **Manual Approval**: Each agent output requires human confirmation
- 🔄 **Revision Options**: Ability to request modifications or adjustments
- 📝 **Custom Input**: Add additional requirements or constraints
- 🎯 **Selection Control**: Choose which results to proceed with
- 💡 **Expert Guidance**: Human oversight for critical decisions

## Installation & Setup

### Prerequisites

1. **Python 3.11+** installed
2. **Poetry** package manager
3. **Google Cloud credentials** configured (optional for demo mode)

### Installation

```bash
# Install dependencies
poetry install

# Add Streamlit (if not already added)
poetry add streamlit

# Set up environment variables
cp .env.example .env
# Edit .env with your Google Cloud project settings
```

### Environment Configuration

Create a `.env` file with:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

## Running the Application

### Method 1: Using the Launcher Script (Recommended)

```bash
# Run the launcher script
poetry run python run_grant_app.py
```

### Method 2: Direct Streamlit Command

```bash
# Run Streamlit directly
poetry run streamlit run grant_research_app.py
```

### Method 3: Without Poetry

```bash
# If you prefer pip
pip install streamlit google-adk python-dotenv
python -m streamlit run grant_research_app.py
```

## Application Interface

### Main Dashboard

- **Sidebar**: Workflow progress tracker and step status
- **Main Area**: Current step interface with agent interactions
- **Progress Bar**: Visual completion status
- **Step Navigation**: Clear indication of current and completed steps

### Step-by-Step Workflow

#### 1. Research Context Setup
- Multi-select research areas
- Career stage selection
- Organization type
- Funding range specification
- Project description input

#### 2. Grant Discovery
- AI-powered grant search
- Agency filtering options
- Custom keyword input
- Results review and selection
- Human approval of selected grants

#### 3. Eligibility Assessment
- Automated requirement checking
- Eligibility scoring
- Missing requirement identification
- Recommendation generation
- Human review and approval

#### 4. Proposal Analysis
- Detailed requirement breakdown
- Template availability check
- Preparation time estimation
- Section-by-section guidance
- Human confirmation of approach

#### 5. Timeline Planning
- Automated timeline generation
- Risk assessment
- Milestone identification
- Resource allocation planning
- Human timeline approval

#### 6. Final Review
- Complete strategy summary
- Export options
- Final human approval
- Report generation

## Demo Mode

The application can run in **demo mode** when Google ADK is not available:

- ✅ Full UI functionality
- 🤖 Simulated agent responses
- 📊 Complete workflow demonstration
- 💾 Export capabilities
- 🎯 Human-in-the-loop features

## Export Features

- **JSON Report**: Complete workflow data and decisions
- **Timeline Export**: Detailed project timelines
- **Grant Summary**: Selected opportunities and analysis
- **Human Decisions**: All approval points and feedback

## Configuration Options

### Streamlit Configuration

The app runs with these default settings:
- **Port**: 8501
- **Address**: localhost
- **Auto-reload**: Enabled
- **Theme**: Light mode
- **Layout**: Wide

### Customization

You can customize the application by modifying:

- `grant_research_app.py`: Main application logic
- CSS styles in the `st.markdown()` sections
- Workflow steps in the `GrantResearchWorkflow` class
- Agent interactions and responses

## Troubleshooting

### Common Issues

1. **Streamlit not found**:
   ```bash
   poetry add streamlit
   # or
   pip install streamlit
   ```

2. **ADK import errors**: 
   - App will run in demo mode automatically
   - Check Google Cloud credentials if needed

3. **Port already in use**:
   ```bash
   streamlit run grant_research_app.py --server.port 8502
   ```

4. **Environment variables**:
   - Ensure `.env` file exists and is properly configured
   - Check Google Cloud project settings

### Logs and Debugging

- Streamlit logs appear in the terminal
- Use browser developer tools for client-side debugging
- Check the sidebar for workflow state information

## Architecture

### Components

- **GrantResearchWorkflow**: Main workflow management class
- **Streamlit UI**: Interactive web interface
- **ADK Integration**: Agent orchestration (when available)
- **Human-in-the-Loop**: Approval and review mechanisms
- **State Management**: Session state persistence

### Data Flow

1. User input → Workflow state
2. Agent processing → AI responses
3. Human review → Approval decisions
4. State updates → Progress tracking
5. Export generation → Final reports

## Development

### Adding New Steps

1. Add step definition to `workflow_steps` array
2. Implement step logic in the main workflow
3. Add human approval mechanisms
4. Update progress tracking

### Customizing Agents

1. Modify agent queries in step implementations
2. Adjust response processing logic
3. Update UI display of results
4. Add new approval criteria

## Support

For issues and questions:

1. Check this README for common solutions
2. Review Streamlit documentation
3. Check Google ADK documentation
4. Examine application logs for error details

## License

This project follows the same license as the parent travel-concierge project.
