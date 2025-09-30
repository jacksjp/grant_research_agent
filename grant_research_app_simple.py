#!/usr/bin/env python3
"""
Grant Research Agent - Minimalistic Streamlit App

A streamlined interface for the 5-step Canada-focused grant research workflow.
"""

import streamlit as st
import json
import asyncio
from datetime import datetime
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="🇨🇦 Grant Research Agent",
    page_icon="🇨🇦",
    layout="centered"
)

# Initialize ADK availability
ADK_AVAILABLE = False
try:
    from google.adk.sessions import Session
    from grant_research_agent.agent import root_agent
    ADK_AVAILABLE = True
    st.sidebar.success("✅ ADK Available")
except ImportError:
    st.sidebar.warning("⚠️ ADK Demo Mode")

# App Header
st.title("🇨🇦 Grant Research Agent")
st.subheader("Canada-Focused Grant Research with Human-in-the-Loop")

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'workflow_data' not in st.session_state:
    st.session_state.workflow_data = {}

# Step definitions
STEPS = {
    1: {
        "title": "🏛️ Organization Verification",
        "subtitle": "Verify your organization is located in Canada",
        "description": "We'll validate your organization details and confirm it's eligible for Canadian grants."
    },
    2: {
        "title": "📝 Research Profile",
        "subtitle": "Create JSON profile for grant matching",
        "description": "Define your research areas, needs, and preferences in a structured format."
    },
    3: {
        "title": "🔍 Grant Search",
        "subtitle": "Find relevant Canadian grants using Vertex search",
        "description": "Search through Canadian grant databases for opportunities matching your profile."
    },
    4: {
        "title": "👤 Human Selection",
        "subtitle": "Review and select grants to pursue",
        "description": "Examine found grants and choose which ones to focus on for applications."
    },
    5: {
        "title": "📄 Application Generation",
        "subtitle": "Generate grant application materials",
        "description": "Create tailored application drafts for your selected grants."
    }
}

# Progress indicator
st.progress(st.session_state.current_step / 5)
st.write(f"**Step {st.session_state.current_step} of 5**")

# Current step display
current_step = STEPS[st.session_state.current_step]
st.markdown(f"## {current_step['title']}")
st.markdown(f"*{current_step['subtitle']}*")
st.write(current_step['description'])

# Step 1: Organization Verification
if st.session_state.current_step == 1:
    with st.form("org_verification"):
        st.markdown("### Organization Details")
        
        org_name = st.text_input(
            "Organization Name *",
            placeholder="e.g., University of Toronto",
            help="Enter your institution's official name"
        )
        
        org_type = st.selectbox(
            "Organization Type *",
            ["University", "College", "Research Institute", "Non-profit", "Government Agency", "Hospital"],
            help="Select your organization type"
        )
        
        org_location = st.text_input(
            "Location *",
            placeholder="e.g., Toronto, Ontario",
            help="City and province in Canada"
        )
        
        research_areas = st.multiselect(
            "Primary Research Areas",
            ["Health Sciences", "Engineering", "Computer Science", "Social Sciences", 
             "Natural Sciences", "Arts & Humanities", "Business", "Education"],
            help="Select your main research focus areas"
        )
        
        submitted = st.form_submit_button("🔍 Verify Organization", type="primary")
        
        if submitted and org_name and org_type and org_location:
            # Mock verification result (replace with real agent call)
            with st.spinner("Verifying organization in Canada..."):
                # Simulate verification
                if "canada" in org_location.lower() or any(prov in org_location.lower() for prov in ["ontario", "quebec", "bc", "alberta", "manitoba", "saskatchewan", "nova scotia", "new brunswick", "pei", "newfoundland", "yukon", "nwt", "nunavut"]):
                    st.success("✅ Organization verified as located in Canada!")
                    
                    # Store data
                    st.session_state.workflow_data['organization'] = {
                        'name': org_name,
                        'type': org_type,
                        'location': org_location,
                        'research_areas': research_areas,
                        'canada_verified': True,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    st.info("**Verification Complete**")
                    st.write(f"• **Organization:** {org_name}")
                    st.write(f"• **Type:** {org_type}")
                    st.write(f"• **Location:** {org_location}")
                    st.write(f"• **Research Areas:** {', '.join(research_areas)}")
                    
                    if st.button("✅ Proceed to Next Step"):
                        st.session_state.current_step = 2
                        st.rerun()
                else:
                    st.error("❌ Organization does not appear to be located in Canada. Only Canadian organizations are eligible.")

# Step 2: Research Profile JSON
elif st.session_state.current_step == 2:
    st.markdown("### Research Profile Setup")
    
    # Show verified organization
    org_data = st.session_state.workflow_data.get('organization', {})
    with st.expander("📋 Verified Organization", expanded=False):
        st.write(f"**{org_data.get('name')}** - {org_data.get('location')}")
    
    with st.form("research_profile"):
        project_title = st.text_input(
            "Project Title *",
            placeholder="Enter your research project title"
        )
        
        project_description = st.text_area(
            "Project Description *",
            placeholder="Describe your research project, objectives, and methodology...",
            height=120
        )
        
        col1, col2 = st.columns(2)
        with col1:
            funding_min = st.number_input("Minimum Funding ($)", min_value=1000, value=50000, step=10000)
            career_stage = st.selectbox("Career Stage", ["Graduate Student", "Postdoc", "Early Career", "Mid Career", "Senior"])
        
        with col2:
            funding_max = st.number_input("Maximum Funding ($)", min_value=1000, value=500000, step=10000)
            duration = st.selectbox("Project Duration", ["1 year", "2 years", "3 years", "4-5 years"])
        
        keywords = st.text_input(
            "Keywords",
            placeholder="artificial intelligence, machine learning, health informatics",
            help="Comma-separated keywords for your research"
        )
        
        submitted = st.form_submit_button("📝 Generate Research Profile JSON", type="primary")
        
        if submitted and project_title and project_description:
            # Generate JSON profile
            profile = {
                "organization": org_data,
                "project": {
                    "title": project_title,
                    "description": project_description,
                    "keywords": [k.strip() for k in keywords.split(",") if k.strip()],
                    "duration": duration,
                    "career_stage": career_stage
                },
                "funding": {
                    "minimum": funding_min,
                    "maximum": funding_max,
                    "currency": "CAD"
                },
                "eligibility": {
                    "canada_only": True,
                    "research_areas": org_data.get('research_areas', [])
                },
                "generated": datetime.now().isoformat()
            }
            
            st.session_state.workflow_data['profile'] = profile
            
            st.success("✅ Research profile generated!")
            st.json(profile, expanded=False)
            
            if st.button("✅ Proceed to Grant Search"):
                st.session_state.current_step = 3
                st.rerun()

# Step 3: Grant Search
elif st.session_state.current_step == 3:
    st.markdown("### Grant Discovery")
    
    profile = st.session_state.workflow_data.get('profile', {})
    
    with st.expander("📋 Search Profile", expanded=False):
        if profile:
            st.write(f"**Project:** {profile['project']['title']}")
            st.write(f"**Funding Range:** ${profile['funding']['minimum']:,} - ${profile['funding']['maximum']:,}")
            st.write(f"**Keywords:** {', '.join(profile['project']['keywords'])}")
    
    if st.button("🔍 Search Canadian Grants", type="primary"):
        with st.spinner("🤖 Searching grant databases..."):
            # Mock search results (replace with real Vertex search)
            mock_grants = [
                {
                    "title": "CIHR Project Grant",
                    "agency": "Canadian Institutes of Health Research", 
                    "amount": "$100,000 - $1,000,000",
                    "deadline": "2025-03-15",
                    "match_score": 0.92,
                    "description": "Supports health research projects across all areas of health research"
                },
                {
                    "title": "NSERC Discovery Grant",
                    "agency": "Natural Sciences and Engineering Research Council",
                    "amount": "$25,000 - $500,000",
                    "deadline": "2025-02-01", 
                    "match_score": 0.88,
                    "description": "Funds ongoing programs of research with long-term goals"
                },
                {
                    "title": "SSHRC Insight Grant",
                    "agency": "Social Sciences and Humanities Research Council",
                    "amount": "$7,000 - $400,000",
                    "deadline": "2025-02-15",
                    "match_score": 0.75,
                    "description": "Supports research in social sciences and humanities"
                }
            ]
            
            st.session_state.workflow_data['found_grants'] = mock_grants
            
            st.success(f"✅ Found {len(mock_grants)} relevant Canadian grants!")
            
            for i, grant in enumerate(mock_grants):
                with st.expander(f"💰 {grant['title']} - Match: {grant['match_score']:.0%}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Agency:** {grant['agency']}")
                        st.write(f"**Amount:** {grant['amount']}")
                    with col2:
                        st.write(f"**Deadline:** {grant['deadline']}")
                        st.write(f"**Match:** {grant['match_score']:.0%}")
                    st.write(f"**Description:** {grant['description']}")
            
            if st.button("✅ Proceed to Grant Selection"):
                st.session_state.current_step = 4
                st.rerun()

# Step 4: Human Selection
elif st.session_state.current_step == 4:
    st.markdown("### Grant Selection")
    
    found_grants = st.session_state.workflow_data.get('found_grants', [])
    
    if found_grants:
        st.write("Select which grants you'd like to pursue:")
        
        selected_grants = []
        for i, grant in enumerate(found_grants):
            if st.checkbox(f"**{grant['title']}** ({grant['agency']}) - Match: {grant['match_score']:.0%}", key=f"grant_{i}"):
                selected_grants.append(grant)
        
        if selected_grants:
            st.write(f"**Selected {len(selected_grants)} grant(s):**")
            for grant in selected_grants:
                st.write(f"• {grant['title']}")
            
            if st.button("✅ Proceed with Selected Grants", type="primary"):
                st.session_state.workflow_data['selected_grants'] = selected_grants
                st.session_state.current_step = 5
                st.rerun()
        else:
            st.info("👆 Please select at least one grant to proceed.")
    else:
        st.error("❌ No grants found. Please go back to Step 3.")

# Step 5: Application Generation
elif st.session_state.current_step == 5:
    st.markdown("### Application Generation")
    
    selected_grants = st.session_state.workflow_data.get('selected_grants', [])
    profile = st.session_state.workflow_data.get('profile', {})
    
    if selected_grants:
        grant_to_generate = st.selectbox(
            "Select grant to generate application for:",
            options=selected_grants,
            format_func=lambda x: x['title']
        )
        
        if st.button("📄 Generate Application Draft", type="primary"):
            with st.spinner("🤖 Generating application materials..."):
                # Mock application generation
                application = {
                    "grant": grant_to_generate['title'],
                    "agency": grant_to_generate['agency'],
                    "project_title": profile['project']['title'],
                    "sections": {
                        "project_summary": f"Summary for {profile['project']['title']}...",
                        "objectives": "1. Primary objective...\n2. Secondary objective...",
                        "methodology": "Detailed methodology based on project description...",
                        "timeline": "Year 1: ...\nYear 2: ...",
                        "budget": f"Total requested: {profile['funding']['minimum']:,} CAD",
                        "team": "Principal Investigator and team details..."
                    },
                    "generated": datetime.now().isoformat()
                }
                
                st.session_state.workflow_data['application'] = application
                
                st.success("✅ Application draft generated!")
                
                with st.expander("📄 Application Draft", expanded=True):
                    st.write(f"**Grant:** {application['grant']}")
                    st.write(f"**Agency:** {application['agency']}")
                    st.write(f"**Project:** {application['project_title']}")
                    
                    for section, content in application['sections'].items():
                        st.markdown(f"**{section.replace('_', ' ').title()}:**")
                        st.text_area(f"{section}", value=content, height=80, key=f"edit_{section}")
                
                # Download options
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download complete workflow data
                    workflow_json = json.dumps(st.session_state.workflow_data, indent=2)
                    st.download_button(
                        "📥 Download Complete Workflow",
                        data=workflow_json,
                        file_name=f"grant_workflow_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        mime="application/json"
                    )
                
                with col2:
                    # Download just the application
                    app_json = json.dumps(application, indent=2)
                    st.download_button(
                        "📝 Download Application Draft",
                        data=app_json,
                        file_name=f"application_draft_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                        mime="application/json"
                    )
                
                st.balloons()
                
                if st.button("🔄 Start New Workflow"):
                    st.session_state.current_step = 1
                    st.session_state.workflow_data = {}
                    st.rerun()
    else:
        st.error("❌ No grants selected. Please go back to Step 4.")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.current_step > 1:
        if st.button("⬅️ Previous Step"):
            st.session_state.current_step -= 1
            st.rerun()

with col2:
    if st.button("🔄 Reset Workflow"):
        st.session_state.current_step = 1
        st.session_state.workflow_data = {}
        st.rerun()

with col3:
    # Next step button (only if current step is complete)
    can_proceed = False
    if st.session_state.current_step == 1 and 'organization' in st.session_state.workflow_data:
        can_proceed = True
    elif st.session_state.current_step == 2 and 'profile' in st.session_state.workflow_data:
        can_proceed = True
    elif st.session_state.current_step == 3 and 'found_grants' in st.session_state.workflow_data:
        can_proceed = True
    elif st.session_state.current_step == 4 and 'selected_grants' in st.session_state.workflow_data:
        can_proceed = True
    
    if can_proceed and st.session_state.current_step < 5:
        if st.button("➡️ Next Step"):
            st.session_state.current_step += 1
            st.rerun()

# Sidebar with workflow summary
with st.sidebar:
    st.markdown("### 📊 Workflow Summary")
    
    for step_num, step_info in STEPS.items():
        if step_num == st.session_state.current_step:
            st.markdown(f"**🔄 {step_num}. {step_info['title'].split(' ', 1)[1]}**")
        elif step_num < st.session_state.current_step:
            st.markdown(f"✅ {step_num}. {step_info['title'].split(' ', 1)[1]}")
        else:
            st.markdown(f"⏳ {step_num}. {step_info['title'].split(' ', 1)[1]}")
    
    # Show current data
    if st.session_state.workflow_data:
        st.markdown("### 📁 Current Data")
        if 'organization' in st.session_state.workflow_data:
            st.write(f"**Org:** {st.session_state.workflow_data['organization']['name']}")
        if 'profile' in st.session_state.workflow_data:
            st.write(f"**Project:** {st.session_state.workflow_data['profile']['project']['title']}")
        if 'found_grants' in st.session_state.workflow_data:
            st.write(f"**Found:** {len(st.session_state.workflow_data['found_grants'])} grants")
        if 'selected_grants' in st.session_state.workflow_data:
            st.write(f"**Selected:** {len(st.session_state.workflow_data['selected_grants'])} grants")
