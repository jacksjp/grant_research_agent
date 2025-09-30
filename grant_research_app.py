#!/usr/bin/env python3
"""
Grant Research Agent - Minimalistic Streamlit App

A streamlined interface for the 4-step Canada-focused grant research workflow.
"""

import streamlit as st
import json
import asyncio
from datetime import datetime
from typing import Dict, Any
import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="🇨🇦 Grant Research Agent",
    page_icon="🇨🇦",
    layout="centered"
)

# ADK Configuration
ADK_BASE_URL = os.getenv("ADK_ENDPOINT", "http://127.0.0.1:8080")
ADK_AVAILABLE = False

# Test ADK connection
def test_adk_connection():
    """Test if ADK is available and responding."""
    global ADK_AVAILABLE
    try:
        logger.debug(f"Testing ADK connection at {ADK_BASE_URL}")
        # Try the root endpoint which should redirect or return something
        response = requests.get(f"{ADK_BASE_URL}/", timeout=5)
        if response.status_code in [200, 307]:  # 307 is temporary redirect
            ADK_AVAILABLE = True
            logger.info("ADK connection successful")
            return True, "✅ ADK Connected"
        else:
            logger.warning(f"ADK responded with status {response.status_code}")
            return False, f"⚠️ ADK Error: {response.status_code}"
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to ADK at {ADK_BASE_URL}")
        return False, f"❌ Cannot connect to ADK at {ADK_BASE_URL}"
    except Exception as e:
        logger.error(f"ADK connection error: {e}")
        return False, f"❌ ADK Error: {str(e)}"

async def validate_canada_location_with_llm(org_location: str, agent_response: any, debug: bool = True) -> dict:
    """Validate if organization is in Canada using ONLY the ADK 2-step verification results.
    NO FALLBACK - if ADK verification fails or is unclear, report as not in Canada.

    Returns structure: {"is_in_canada": bool, "confidence": level, "reasoning": str}
    """
    
    # Convert agent response to string for processing
    if agent_response:
        if isinstance(agent_response, dict):
            response_text = str(agent_response).lower()
        else:
            response_text = str(agent_response).lower()
    else:
        return {
            "is_in_canada": False,
            "confidence": "high",
            "reasoning": "No ADK verification response received - cannot confirm Canadian location"
        }
    
    # Check for new 2-step verification results
    if "✅ verification status: passed - organization confirmed in canada" in response_text:
        return {
            "is_in_canada": True,
            "confidence": "high",
            "reasoning": "ADK 2-step verification passed: Organization and location match verified, and location confirmed in Canada"
        }
    
    elif "❌ verification status: failed - organization/location mismatch" in response_text:
        return {
            "is_in_canada": False,
            "confidence": "high",
            "reasoning": "ADK 2-step verification failed: Organization name or location does not match Google search results"
        }
    
    elif "❌ verification status: failed - organization not in canada" in response_text:
        return {
            "is_in_canada": False,
            "confidence": "high", 
            "reasoning": "ADK 2-step verification failed: Organization exists but is not located in Canada"
        }
    
    elif "🔍 verification status: inconclusive - manual verification required" in response_text:
        return {
            "is_in_canada": False,
            "confidence": "high",
            "reasoning": "ADK verification inconclusive: Unable to verify Canadian location - treating as not in Canada"
        }
    
    # Check for old format (legacy support)
    elif "confirmed in canada" in response_text or "verification status: confirmed in canada" in response_text:
        return {
            "is_in_canada": True,
            "confidence": "medium",
            "reasoning": "Agent verification confirms Canadian location (legacy format)"
        }
    
    elif "not located in canada" in response_text or "not in canada" in response_text:
        return {
            "is_in_canada": False,
            "confidence": "high",
            "reasoning": "Agent verification confirms organization is not in Canada"
        }
    
    # NO FALLBACK - if we can't determine from ADK verification, treat as not in Canada
    else:
        return {
            "is_in_canada": False,
            "confidence": "high",
            "reasoning": "ADK verification response unclear or unrecognized format - treating as not in Canada"
        }


async def call_adk_agent_async(agent_name: str, query: str, debug: bool = True) -> dict:
    """Call ADK via HTTP API server with auto-discovery and session creation.
    
    Tries multiple app names, creates session if needed, and discovers endpoints.
    """
    if not ADK_AVAILABLE:
        return {"success": False, "response": "ADK agent not available. Start ADK API server.", "error": "ADK_NOT_AVAILABLE"}

    import json, uuid
    import requests

    session_id = st.session_state.get('session_id', f"session_{uuid.uuid4().hex[:8]}")
    user_id = st.session_state.get('user_id', 'ui_user')
    
    # Try multiple app names that might be configured
    app_candidates = ['grant_research_agent', 'travel_concierge', 'grant_research']
    base = ADK_BASE_URL.rstrip('/')
    
    # Auto-discover endpoints from OpenAPI if available
    discovered_endpoints = []
    try:
        openapi_resp = requests.get(f"{base}/openapi.json", timeout=10)
        if openapi_resp.status_code == 200:
            openapi_data = openapi_resp.json()
            paths = openapi_data.get("paths", {})
            for path in paths:
                if "run" in path.lower():
                    discovered_endpoints.append(f"{base}{path}")
                    if debug:
                        logger.debug(f"Discovered endpoint: {base}{path}")
    except Exception as e:
        if debug:
            logger.debug(f"OpenAPI discovery failed: {e}")

    diagnostics = []
    
    for app_name in app_candidates:
        # Try to create session first
        session_url = f"{base}/apps/{app_name}/users/{user_id}/sessions/{session_id}"
        try:
            session_resp = requests.post(session_url, timeout=10)
            if session_resp.status_code in [200, 201]:
                if debug:
                    logger.debug(f"Session created for app {app_name}")
            diagnostics.append(f"Session {session_url}: {session_resp.status_code}")
        except Exception as se:
            diagnostics.append(f"Session {session_url}: ERROR {se}")
        
        # Build message payload
        full_user_text = f"[AGENT:{agent_name}]\n{query}" if agent_name else query
        payload = {
            "session_id": session_id,
            "app_name": app_name,
            "user_id": user_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": full_user_text}]
            }
        }
        
        # Build endpoint candidates for this app
        stream_endpoints = [
            f"{base}/run_sse",
            f"{base}/apps/{app_name}/users/{user_id}/sessions/{session_id}/run_sse",
            f"{base}/apps/{app_name}/run_sse",
        ] + [ep for ep in discovered_endpoints if "sse" in ep.lower()]
        
        non_stream_endpoints = [
            f"{base}/run",
            f"{base}/apps/{app_name}/users/{user_id}/sessions/{session_id}/run",
            f"{base}/apps/{app_name}/run",
        ] + [ep for ep in discovered_endpoints if "sse" not in ep.lower() and "run" in ep.lower()]
        
        headers = {"Content-Type": "application/json; charset=UTF-8", "Accept": "text/event-stream"}
        
        def parse_event_line(raw: bytes) -> str | None:
            try:
                line = raw.decode('utf-8').removeprefix('data: ').strip()
                if not line or line == "[DONE]":
                    return None
                event = json.loads(line)
                content = event.get("content", {})
                parts = content.get("parts", []) if isinstance(content, dict) else []
                if parts and isinstance(parts, list):
                    first = parts[0]
                    if isinstance(first, dict) and 'text' in first:
                        return first['text']
                return None
            except Exception:
                return None

        aggregated = []
        
        # Try streaming endpoints
        for s_url in stream_endpoints:
            try:
                with requests.post(s_url, data=json.dumps(payload), headers=headers, stream=True, timeout=60) as r:
                    diagnostics.append(f"Stream {s_url}: {r.status_code}")
                    if r.status_code == 200:
                        for chunk in r.iter_lines():
                            if not chunk:
                                continue
                            text_piece = parse_event_line(chunk)
                            if text_piece:
                                aggregated.append(text_piece)
                        if aggregated:
                            break
            except Exception as se:
                diagnostics.append(f"Stream {s_url}: ERROR {se}")
        
        # Try non-streaming endpoints if no streamed content
        if not aggregated:
            for n_url in non_stream_endpoints:
                try:
                    r2 = requests.post(n_url, json=payload, timeout=60)
                    diagnostics.append(f"NonStream {n_url}: {r2.status_code}")
                    if r2.status_code == 200:
                        try:
                            data = r2.json()
                            if isinstance(data, dict):
                                # Extract text from various possible response formats
                                text_val = (data.get('text') or 
                                          data.get('response') or 
                                          data.get('content') or 
                                          str(data.get('result', data)))
                                aggregated.append(str(text_val))
                            else:
                                aggregated.append(str(data))
                        except Exception:
                            aggregated.append(r2.text)
                        if aggregated:
                            break
                except Exception as ne:
                    diagnostics.append(f"NonStream {n_url}: ERROR {ne}")
        
        # If we got a response with this app, return it
        if aggregated:
            full_response = "\n".join(aggregated).strip()
            if debug:
                logger.debug(f"ADK success with app {app_name}, response length={len(full_response)}")
            
            # Store successful app name for future use
            if 'adk_app_name' not in st.session_state:
                st.session_state.adk_app_name = app_name
            
            return {
                "success": True, 
                "response": full_response, 
                "mock": False, 
                "agent": agent_name,
                "app_used": app_name,
                "diagnostics": diagnostics
            }
    
    # If we get here, no app worked
    return {
        "success": False, 
        "response": f"All ADK endpoints failed for all apps. Diagnostics: {'; '.join(diagnostics[-10:])}", 
        "error": "ADK_HTTP_ERROR",
        "diagnostics": diagnostics
    }

def call_adk_agent(agent_name: str, query: str, debug=True):
    """Synchronous wrapper for calling ADK agent."""
    return asyncio.run(call_adk_agent_async(agent_name, query, debug))

# Initialize ADK connection test
try:
    from google.adk.sessions import Session
    from grant_research_agent.agent import root_agent
    
    # Test API connection
    adk_connected, adk_status = test_adk_connection()
    
    if adk_connected:
        st.sidebar.success(f"✅ ADK Available at {ADK_BASE_URL}")
    else:
        st.sidebar.warning(f"⚠️ ADK Demo Mode - {adk_status}")
        
except ImportError:
    st.sidebar.warning("⚠️ ADK Demo Mode - Import Error")

# App Header
st.title("🇨🇦 Grant Research Agent")
st.subheader("Canada-Focused Grant Research with Human-in-the-Loop")

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'workflow_data' not in st.session_state:
    st.session_state.workflow_data = {}
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False

# Step definitions
STEPS = {
    1: {
        "title": "🏛️ Organization Verification",
        "subtitle": "Verify your organization is located in Canada",
        "description": "We'll validate your organization details and confirm it's eligible for Canadian grants."
    },
    2: {
        "title": "� Grant Information",
        "subtitle": "Upload grant file or provide grant description",
        "description": "Provide details about the specific grant you're interested in."
    },
    3: {
        "title": "✅ Eligibility Check",
        "subtitle": "Verify organization eligibility for the grant",
        "description": "We'll check if your organization meets the grant requirements."
    },
    4: {
        "title": "� Project Description",
        "subtitle": "Describe your project and get qualification suggestions",
        "description": "Provide project details and receive suggestions to strengthen your application."
    },
    5: {
        "title": "📄 Application Generation",
        "subtitle": "Generate grant application materials",
        "description": "Create tailored application drafts for your selected grants."
    }
}

# Progress indicator
st.progress(st.session_state.current_step / 4)
st.write(f"**Step {st.session_state.current_step} of 4**")

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
            # Call organization verification agent via ADK API
            with st.spinner("Verifying organization in Canada..."):
                
                import textwrap
                verification_query = textwrap.dedent(f"""
                Please perform 2-step verification for this organization:
                
                Organization Details:
                - Organization Name: {org_name}
                - Institution Type: {org_type}
                - Location: {org_location}
                - Research Areas: {', '.join(research_areas) if research_areas else 'Not specified'}

                STEP 1: Verify organization name and location match Google search results
                STEP 2: Verify the location is in Canada
                
                Use the 2-step verification process:
                1. First verify the organization exists at the provided location
                2. Then verify the location is in Canada
                
                Return structured verification results showing both step outcomes.
                """)
                
                # Show debug info
                with st.expander("🔍 Debug Info", expanded=False):
                    st.write(f"**ADK Endpoint:** {ADK_BASE_URL}")
                    st.write(f"**ADK Available:** {ADK_AVAILABLE}")
                    st.write("**Query:**")
                    st.text(verification_query)
                
                # Call ADK agent
                result = call_adk_agent("organization_verifier", verification_query, debug=True)
                
                # Show API response and diagnostics in debug
                with st.expander("🔧 API Response & Diagnostics", expanded=False):
                    st.json(result)
                    if "diagnostics" in result:
                        st.write("**Endpoint Attempts:**")
                        for diag in result["diagnostics"]:
                            st.text(diag)
                
                if result["success"]:
                    # Use LLM to validate Canada location
                    with st.spinner("🤖 Validating Canada location..."):
                        validation_result = asyncio.run(validate_canada_location_with_llm(
                            org_location, result["response"], debug=st.session_state.debug_mode
                        ))
                    
                    # Show LLM validation results
                    with st.expander("🧠 Validation Results", expanded=st.session_state.debug_mode):
                        st.json(validation_result)
                    
                    is_in_canada = validation_result.get("is_in_canada", False)
                    confidence = validation_result.get("confidence", "unknown")
                    reasoning = validation_result.get("reasoning", "No reasoning provided")
                    
                    # Display results based on validation
                    if is_in_canada:
                        confidence_color = "🟢" if confidence == "high" else "🟡" if confidence == "medium" else "🟠"
                        st.success(f"✅ Organization verified as located in Canada! {confidence_color} {confidence.title()} confidence")
                        
                        # Show detailed 2-step verification results if available
                        response_text = str(result["response"]) if result["response"] else ""
                        response_text_lower = response_text.lower()
                        
                        if "step 1 verification" in response_text_lower and "step 2 verification" in response_text_lower:
                            st.info("**📋 2-Step Verification Results:**")
                            
                            # Extract step results
                            if "step 1 verification: ✅" in response_text_lower:
                                st.write("**Step 1:** ✅ Organization & location match confirmed")
                            elif "step 1 verification: ❌" in response_text_lower:
                                st.write("**Step 1:** ❌ Organization & location mismatch detected")
                            
                            if "step 2 verification: ✅" in response_text_lower:
                                st.write("**Step 2:** ✅ Location confirmed in Canada")
                            elif "step 2 verification: ❌" in response_text_lower:
                                st.write("**Step 2:** ❌ Location not in Canada")
                        
                        # Show reasoning
                        with st.expander("💡 Validation Reasoning"):
                            st.write(reasoning)
                            
                        # Show raw verification results
                        with st.expander("📄 Detailed Verification Results"):
                            st.text(response_text)
                        
                        # Store data
                        st.session_state.workflow_data['organization'] = {
                            'name': org_name,
                            'type': org_type,
                            'location': org_location,
                            'research_areas': research_areas,
                            'canada_verified': True,
                            'verification_result': result["response"],
                            'llm_validation': validation_result,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        st.info("**Verification Complete**")
                        st.write(f"• **Organization:** {org_name}")
                        st.write(f"• **Type:** {org_type}")
                        st.write(f"• **Location:** {org_location}")
                        st.write(f"• **Research Areas:** {', '.join(research_areas)}")
                        
                        # Store data in session state to use outside form
                        st.session_state.temp_org_data = {
                            'name': org_name,
                            'type': org_type,
                            'location': org_location,
                            'research_areas': research_areas,
                            'canada_verified': True,
                            'verification_result': result["response"],
                            'llm_validation': validation_result,
                            'timestamp': datetime.now().isoformat()
                        }
                        st.session_state.verification_complete = True
                        
                    else:
                        # Enhanced failure display for 2-step verification
                        st.error(f"❌ Organization verification failed. ({confidence.title()} confidence)")
                        
                        # Show detailed failure information if available
                        response_text = str(result["response"]) if result["response"] else ""
                        response_text_lower = response_text.lower()
                        
                        if "step 1 verification: ❌" in response_text_lower:
                            st.error("**Step 1 Failed:** Organization name or location does not match Google search results")
                        elif "step 2 verification: ❌" in response_text_lower:
                            st.error("**Step 2 Failed:** Organization exists but is not located in Canada")
                        elif "inconclusive" in response_text_lower:
                            st.warning("**Verification Inconclusive:** Manual verification required")
                        
                        # Show reasoning
                        with st.expander("❓ Why was this rejected?"):
                            st.write(reasoning)
                            
                        # Show detailed verification results
                        with st.expander("📄 Detailed Verification Results"):
                            st.text(response_text)
                        
                        # Store override data for use outside form
                        st.session_state.temp_override_data = {
                            'name': org_name,
                            'type': org_type,
                            'location': org_location,
                            'research_areas': research_areas,
                            'canada_verified': True,
                            'verification_method': 'manual_override',
                            'timestamp': datetime.now().isoformat()
                        }
                        st.session_state.show_override = True
                else:
                    # Handle ADK errors
                    error_type = result.get("error", "UNKNOWN")
                    
                    if error_type == "ADK_NOT_AVAILABLE":
                        st.error("❌ ADK Agent Not Available")
                        st.warning("**Issue:** The ADK (Agent Development Kit) service is not running or not connected.")
                        st.info("**Solution:** Please ensure the ADK service is started and accessible.")
                        
                        with st.expander("🔧 Technical Details"):
                            st.write(f"**ADK Endpoint:** {ADK_BASE_URL}")
                            st.write(f"**ADK Status:** Not Available")
                            st.write(f"**Error:** {result['response']}")
                    
                    elif error_type == "ADK_CALL_FAILED":
                        st.error("❌ ADK Agent Call Failed")
                        st.warning("**Issue:** The ADK service is available but the agent call failed.")
                        
                        with st.expander("🔧 Error Details"):
                            st.write(f"**Error:** {result['response']}")
                            st.write("This could be due to:")
                            st.write("- Agent configuration issues")
                            st.write("- Network connectivity problems")
                            st.write("- Internal ADK service errors")
                    
                    else:
                        st.error(f"❌ Verification failed: {result['response']}")
                        st.error("Please check your organization details and try again, or contact support if the issue persists.")
        else:
            st.info("👆 Please enter your organization name to begin verification.")
    
    # Handle buttons outside the form
    if hasattr(st.session_state, 'verification_complete') and st.session_state.verification_complete:
        if st.button("✅ Proceed to Next Step", type="primary"):
            st.session_state.workflow_data['organization'] = st.session_state.temp_org_data
            st.session_state.current_step = 2
            # Clean up temporary state
            del st.session_state.verification_complete
            del st.session_state.temp_org_data
            st.rerun()
    
    if hasattr(st.session_state, 'show_override') and st.session_state.show_override:
        # Manual override option (outside form)
        st.info("� **Tip:** Make sure your location includes:")
        st.write("• Province name (e.g., Ontario, Quebec, British Columbia)")
        st.write("• City name (e.g., Toronto, Montreal, Vancouver)")  
        st.write("• 'Canada' in the location field")
        st.write("• Examples: 'Toronto, Ontario, Canada' or 'Montreal, Quebec'")
        
        if st.checkbox("🔧 Manual Override: Confirm this organization IS in Canada"):
            st.warning("⚠️ Using manual override for Canada verification")
            if st.button("✅ Override and Proceed"):
                st.session_state.workflow_data['organization'] = st.session_state.temp_override_data
                st.session_state.current_step = 2
                # Clean up temporary state
                del st.session_state.show_override
                del st.session_state.temp_override_data
                st.rerun()

# Step 2: Research Profile JSON
elif st.session_state.current_step == 2:
    st.markdown("### Grant Information")
    
    # Show verified organization
    org_data = st.session_state.workflow_data.get('organization', {})
    with st.expander("📋 Verified Organization", expanded=False):
        st.write(f"**{org_data.get('name')}** - {org_data.get('location')}")
    
    # Initialize state
    st.session_state.setdefault('grant_mode', 'describe')  # 'describe' or 'file'
    st.session_state.setdefault('grant_description_text', '')
    st.session_state.setdefault('grant_file_obj', None)

    # Selection outside form (avoids rerender issues inside form)
    mode = st.radio(
        "Grant input method",
        ["Describe Grant", "Upload File"],
        index=0 if st.session_state.grant_mode == 'describe' else 1,
        horizontal=True,
        key="grant_mode_selector"
    )
    st.session_state.grant_mode = 'describe' if mode == "Describe Grant" else 'file'

    # Display inputs (not inside the form so switching doesn't lose state)
    if st.session_state.grant_mode == 'describe':
        st.session_state.grant_description_text = st.text_area(
            "Grant Description *",
            value=st.session_state.grant_description_text,
            placeholder="Grant name, funder, eligibility, funding amount, deadline, focus areas, special requirements...",
            height=180,
            key="grant_description_main"
        )
    else:
        uploaded = st.file_uploader(
            "Grant Document (pdf / txt / docx)",
            type=['pdf', 'txt', 'docx'],
            key="grant_file_main"
        )
        if uploaded is not None:
            st.session_state.grant_file_obj = uploaded
            st.info(f"Selected file: {uploaded.name}")

    # Simple form just for submission button
    with st.form("grant_info"):
        submitted = st.form_submit_button("✅ Save Grant Information", type="primary")
        if submitted:
            if st.session_state.grant_mode == 'describe':
                desc = st.session_state.grant_description_text.strip()
                if not desc:
                    st.error("Please enter a grant description.")
                else:
                    st.session_state.workflow_data['grant_info'] = {
                        'method': 'description',
                        'description': desc,
                        'timestamp': datetime.now().isoformat()
                    }
                    st.success("✅ Grant description saved!")
                    st.session_state.grant_processed = True
            else:
                file_obj = st.session_state.grant_file_obj
                if file_obj is None:
                    st.error("Please upload a grant file.")
                else:
                    # Read once and store content summary
                    if getattr(file_obj, 'type', '') == 'text/plain':
                        try:
                            content = file_obj.read().decode('utf-8', errors='ignore')
                        except Exception:
                            content = "(Unable to decode text)"
                    else:
                        content = "Binary or non-text file uploaded"
                    st.session_state.workflow_data['grant_info'] = {
                        'method': 'file_upload',
                        'filename': file_obj.name,
                        'file_type': getattr(file_obj, 'type', 'unknown'),
                        'file_size': getattr(file_obj, 'size', 0),
                        'content_preview': content[:800],
                        'timestamp': datetime.now().isoformat()
                    }
                    st.success(f"✅ File '{file_obj.name}' saved!")
                    st.session_state.grant_processed = True

    # Debug info
    if st.session_state.get('debug_mode', False):
        st.caption(f"[Debug] grant_mode={st.session_state.grant_mode} has_file={st.session_state.grant_file_obj is not None} desc_len={len(st.session_state.grant_description_text)}")
    
    # Handle proceed button outside the form
    if hasattr(st.session_state, 'grant_processed') and st.session_state.grant_processed:
        if st.button("➡️ Check Eligibility"):
            st.session_state.current_step = 3
            # Clean up temporary state
            del st.session_state.grant_processed
            st.rerun()

elif st.session_state.current_step == 3:
    st.markdown("### Eligibility Check")
    
    # Show organization and grant info
    org_data = st.session_state.workflow_data.get('organization', {})
    grant_info = st.session_state.workflow_data.get('grant_info', {})
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📋 Organization", expanded=False):
            st.write(f"**{org_data.get('name')}**")
            st.write(f"Location: {org_data.get('location')}")
            st.write(f"Type: {org_data.get('type')}")
    
    with col2:
        with st.expander("📄 Grant Info", expanded=False):
            if grant_info.get('method') == 'file_upload':
                st.write(f"File: {grant_info.get('filename')}")
            else:
                st.write("Description provided")
    
    with st.form("eligibility_check"):
        st.info("🔍 Checking organization eligibility for this grant...")
        
        # Simple eligibility simulation
        eligibility_factors = st.multiselect(
            "Confirm your organization meets these common requirements:",
            [
                "Located in Canada",
                "Registered non-profit or educational institution", 
                "Has research capacity",
                "Meets minimum funding requirements",
                "Within grant's target sectors"
            ],
            default=["Located in Canada"]
        )
        
        submitted = st.form_submit_button("✅ Verify Eligibility", type="primary")
        
        if submitted:
            # Basic eligibility logic
            is_eligible = len(eligibility_factors) >= 3 and "Located in Canada" in eligibility_factors
            
            eligibility_result = {
                "eligible": is_eligible,
                "factors_met": eligibility_factors,
                "total_factors": len(eligibility_factors),
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.workflow_data['eligibility'] = eligibility_result
            
            if is_eligible:
                st.success("✅ Your organization appears to be eligible for this grant!")
                st.session_state.eligibility_confirmed = True
            else:
                st.error("❌ Your organization may not meet all requirements for this grant.")
                st.warning("Consider reviewing the grant requirements or consulting with a grant specialist.")
    
    # Handle proceed button outside the form
    if hasattr(st.session_state, 'eligibility_confirmed') and st.session_state.eligibility_confirmed:
        if st.button("➡️ Describe Project"):
            st.session_state.current_step = 4
            # Clean up temporary state
            del st.session_state.eligibility_confirmed
            st.rerun()

elif st.session_state.current_step == 4:
    st.markdown("### Project Description & Qualification Suggestions")
    
    # Show previous data
    org_data = st.session_state.workflow_data.get('organization', {})
    grant_info = st.session_state.workflow_data.get('grant_info', {})
    
    with st.expander("📋 Summary", expanded=False):
        st.write(f"**Organization:** {org_data.get('name')}")
        st.write(f"**Grant:** {grant_info.get('filename', 'Description provided')}")
        st.write("**Eligibility:** ✅ Confirmed")
    
    with st.form("project_description"):
        project_title = st.text_input(
            "Project Title *",
            placeholder="Enter your project title"
        )
        
        project_description = st.text_area(
            "Project Description *",
            placeholder="Describe your project including:\n• Objectives and goals\n• Methodology and approach\n• Expected outcomes\n• Timeline\n• Budget considerations",
            height=120
        )
        
        col1, col2 = st.columns(2)
        with col1:
            funding_amount = st.number_input("Requested Funding ($)", min_value=1000, value=50000, step=5000)
            project_duration = st.selectbox("Project Duration", ["6 months", "1 year", "2 years", "3 years"])
        
        with col2:
            research_area = st.text_input("Primary Research Area", placeholder="e.g., AI, Health, Climate")
            team_size = st.number_input("Team Size", min_value=1, value=3, step=1)
        
        submitted = st.form_submit_button("🎯 Get Qualification Suggestions", type="primary")
        
        if submitted and project_title and project_description:
            project_data = {
                "title": project_title,
                "description": project_description,
                "funding_amount": funding_amount,
                "duration": project_duration,
                "research_area": research_area,
                "team_size": team_size,
                "timestamp": datetime.now().isoformat()
            }
            
            st.session_state.workflow_data['project'] = project_data
            
            # Generate simple suggestions
            suggestions = [
                "✅ Ensure your project timeline aligns with grant reporting requirements",
                "📊 Include detailed budget breakdown with justifications",
                "🤝 Consider partnerships with other institutions to strengthen your application", 
                "📚 Highlight previous relevant research experience and publications",
                "🎯 Clearly articulate the impact and benefits of your research",
                "📋 Prepare all required documentation well before the deadline"
            ]
            
            st.success("✅ Project information saved!")
            st.markdown("### 🎯 Qualification Suggestions")
            
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
            
            st.session_state.suggestions_generated = True
    
    # Handle completion outside the form
    if hasattr(st.session_state, 'suggestions_generated') and st.session_state.suggestions_generated:
        st.markdown("### 🎉 Workflow Complete!")
        st.info("You now have a comprehensive analysis of your grant application readiness.")
        
        if st.button("🔄 Start New Analysis"):
            # Reset workflow
            for key in ['workflow_data', 'suggestions_generated']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_step = 1
            st.rerun()

# Placeholder for remaining steps (if any)
else:
    st.info(f"Step {st.session_state.current_step} is under development. Coming soon!")
    
    if st.button("⬅️ Back to Step 1"):
        st.session_state.current_step = 1
        st.rerun()

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

# Sidebar with workflow summary
with st.sidebar:
    st.markdown("### 📊 Workflow Summary")

    st.markdown("#### � Final Application Export")
    wf = st.session_state.workflow_data
    if st.button("Generate Application Document", key="export_application"):
        lines = []
        lines.append(f"Grant Application Draft - Generated {datetime.now().isoformat()}")
        lines.append("=" * 70)
        # Organization
        org = wf.get('organization')
        if org:
            lines.append("\n[1] Organization Verification")
            lines.append(f"Name: {org.get('name')}")
            lines.append(f"Location: {org.get('location')}")
            lines.append(f"Type: {org.get('type')}")
            lines.append(f"Canada Verified: {'Yes' if org.get('canada_verified') else 'No'}")
            ra = org.get('research_areas') or []
            if ra:
                lines.append(f"Research Areas: {', '.join(ra)}")
        else:
            lines.append("\n[1] Organization Verification: MISSING")
        # Grant info
        grant_info = wf.get('grant_info')
        if grant_info:
            lines.append("\n[2] Grant Information")
            if grant_info.get('method') == 'file_upload':
                lines.append(f"Provided: File Upload ({grant_info.get('filename')})")
            else:
                desc = grant_info.get('description', '')
                lines.append("Provided: Description")
                lines.append("Description:")
                lines.append(desc[:4000])
        else:
            lines.append("\n[2] Grant Information: MISSING")
        # Eligibility
        elig = wf.get('eligibility')
        if elig:
            lines.append("\n[3] Eligibility Assessment")
            lines.append(f"Status: {'Eligible' if elig.get('eligible') else 'Conditional / Not Confirmed'}")
            fm = elig.get('factors_met')
            if fm:
                lines.append("Factors Confirmed: " + ", ".join(fm))
        else:
            lines.append("\n[3] Eligibility Assessment: MISSING")
        # Project
        proj = wf.get('project')
        if proj:
            lines.append("\n[4] Project Description")
            lines.append(f"Title: {proj.get('title','(untitled)')}")
            lines.append(f"Funding Requested: {proj.get('funding_amount','N/A')} CAD")
            lines.append(f"Duration: {proj.get('duration','N/A')}")
            lines.append(f"Research Area: {proj.get('research_area','N/A')}")
            lines.append(f"Team Size: {proj.get('team_size','N/A')}")
            lines.append("Description:")
            lines.append(proj.get('description','')[:6000])
        else:
            lines.append("\n[4] Project Description: MISSING")
        # Suggestions (if generated)
        if st.session_state.get('suggestions_generated'):
            lines.append("\n[5] Qualification Suggestions")
            lines.append("Refer to on-screen suggestions captured during session.")
        # Gaps summary
        gaps = []
        if not org: gaps.append("Organization details")
        if not grant_info: gaps.append("Grant info")
        if not elig: gaps.append("Eligibility assessment")
        if not proj: gaps.append("Project description")
        lines.append("\n---")
        if gaps:
            lines.append("Missing Sections: " + ", ".join(gaps))
        else:
            lines.append("All core sections completed.")
        st.session_state.generated_application_doc = "\n".join(lines)
        st.success("Application document generated below.")

    if 'generated_application_doc' in st.session_state:
        st.download_button(
            label="⬇️ Download Application (.txt)",
            data=st.session_state.generated_application_doc,
            file_name=f"grant_application_{st.session_state.session_id}.txt",
            mime="text/plain",
            key="download_application_txt"
        )
    
    # Debug toggle
    st.session_state.debug_mode = st.checkbox("🔧 Debug Mode", value=st.session_state.debug_mode)
    
    # Connection status
    st.markdown("### 🔗 Connection Status")
    st.write(f"**ADK Endpoint:** {ADK_BASE_URL}")
    
    if st.button("🔄 Test ADK Connection"):
        with st.spinner("Testing connection..."):
            connected, status = test_adk_connection()
            if connected:
                st.success(status)
            else:
                st.error(status)
    
    # Workflow progress
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
        
        # Debug data view
        if st.session_state.debug_mode:
            with st.expander("🔍 Raw Data"):
                st.json(st.session_state.workflow_data)
