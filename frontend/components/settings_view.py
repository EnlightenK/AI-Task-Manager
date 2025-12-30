import streamlit as st
import pandas as pd
from frontend.services.api_client import fetch_projects, update_projects, fetch_team, update_team

def render_settings_view():
    st.header("⚙️ Settings")
    
    tab_projects, tab_team = st.tabs(["Projects", "Team Members"])
    
    # --- Projects Tab ---
    with tab_projects:
        st.subheader("Manage Projects")
        st.info("Edit the table below to add, modify, or remove projects. Changes are saved automatically when you click 'Save Changes'.")
        
        current_projects = fetch_projects()
        
        # Prepare DataFrame
        if current_projects:
            df_projects = pd.DataFrame(current_projects)
        else:
            df_projects = pd.DataFrame(columns=["id", "name", "context"])
            
        # Data Editor
        edited_df_projects = st.data_editor(
            df_projects,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "id": st.column_config.TextColumn("Project ID", help="Unique ID (e.g., SB-01)", required=True),
                "name": st.column_config.TextColumn("Project Name", required=True),
                "context": st.column_config.TextColumn("Context/Description", width="large")
            },
            key="projects_editor"
        )
        
        if st.button("Save Project Changes", type="primary"):
            # Convert back to list of dicts
            updated_projects_list = edited_df_projects.to_dict(orient="records")
            # Filter out empty rows if any (though required=True helps)
            valid_projects = [p for p in updated_projects_list if p.get("id") and p.get("name")]
            
            update_projects(valid_projects)
            st.success("Projects updated successfully!")
            st.rerun()

    # --- Team Tab ---
    with tab_team:
        st.subheader("Manage Team")
        st.info("Edit the table below to manage team members. 'Projects' should be a comma-separated list of Project IDs.")
        
        current_team = fetch_team()
        
        # Prepare DataFrame
        # Flatten 'projects' list to string for editing, or handle it carefully
        # Simple approach: convert list to comma-separated string
        processed_team = []
        for t in current_team:
            t_copy = t.copy()
            if isinstance(t_copy.get('projects'), list):
                t_copy['projects'] = ", ".join(t_copy['projects'])
            if isinstance(t_copy.get('duties'), list):
                t_copy['duties'] = ", ".join(t_copy['duties'])
            processed_team.append(t_copy)
            
        if processed_team:
            df_team = pd.DataFrame(processed_team)
        else:
            df_team = pd.DataFrame(columns=["name", "role", "duties", "projects"])
            
        # Data Editor
        edited_df_team = st.data_editor(
            df_team,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "name": st.column_config.TextColumn("Name", required=True),
                "role": st.column_config.TextColumn("Role", required=True),
                "duties": st.column_config.TextColumn("Duties (comma-separated)", width="medium"),
                "projects": st.column_config.TextColumn("Assigned Projects (comma-separated)", width="medium")
            },
            key="team_editor"
        )
        
        if st.button("Save Team Changes", type="primary"):
            # Convert back and process lists
            raw_team_list = edited_df_team.to_dict(orient="records")
            final_team_list = []
            
            for t in raw_team_list:
                if not t.get("name"): continue
                
                # Convert strings back to lists
                proj_str = t.get("projects", "")
                duties_str = t.get("duties", "")
                
                t['projects'] = [p.strip() for p in proj_str.split(",") if p.strip()] if isinstance(proj_str, str) else []
                t['duties'] = [d.strip() for d in duties_str.split(",") if d.strip()] if isinstance(duties_str, str) else []
                
                final_team_list.append(t)
            
            update_team(final_team_list)
            st.success("Team updated successfully!")
            st.rerun()
