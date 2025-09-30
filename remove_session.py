#!/usr/bin/env python3
"""Remove session JSON loading section from grant_research_app.py"""

with open('grant_research_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find start and end of session loading section
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if '# Load saved session JSON' in line:
        start_idx = i
    elif start_idx is not None and 'Final Application Export' in line and 'st.markdown' in line:
        end_idx = i
        break

if start_idx is not None and end_idx is not None:
    print(f"Removing lines {start_idx} to {end_idx-1}")
    # Keep the Final Application Export line but remove everything before it
    lines = lines[:start_idx] + lines[end_idx:]
    
    with open('grant_research_app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("Session JSON section removed successfully!")
else:
    print("Could not locate session loading section")
