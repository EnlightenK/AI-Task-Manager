import streamlit as st
from frontend.services.api_client import fetch_tasks, update_task_details, archive_task, fetch_projects, fetch_team

def render_active_view():
    st.header("Active Tasks (Execution)")
    
    tasks = fetch_tasks("APPROVED")
    
    if not tasks:
        st.info("No active tasks.")
        return

    # Load options
    projects = fetch_projects()
    team = fetch_team()
    project_options = [p['id'] for p in projects]
    assignee_options = [t['name'] for t in team]

    for task in tasks:
        with st.container(border=True):
            # Unique key for edit mode state
            edit_key = f"edit_mode_{task['id']}"
            if edit_key not in st.session_state:
                st.session_state[edit_key] = False

            # Layout: Checkbox | Content
            col_check, col_content = st.columns([0.5, 11.5])
            
            with col_check:
                # Using a callback or checking logic after rendering
                # Note: modifying state during render can be tricky, but checkbox returns bool.
                # If checked, we archive.
                is_done = st.checkbox("Mark as done", key=f"done_{task['id']}", label_visibility="collapsed")
                if is_done:
                    archive_task(task['id'])
                    st.rerun()

            with col_content:
                if st.session_state[edit_key]:
                    # --- Edit Mode ---
                    with st.form(key=f"form_{task['id']}"):
                        new_summary = st.text_input("Summary", value=task['summary'])
                        
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            new_project = st.selectbox("Project", project_options, index=project_options.index(task['project_id']) if task['project_id'] in project_options else 0)
                        with c2:
                            new_assignee = st.selectbox("Assignee", assignee_options, index=assignee_options.index(task['assignee']) if task['assignee'] in assignee_options else 0)
                        with c3:
                            new_deadline = st.text_input("Deadline", value=task['deadline'])
                        
                        col_save, col_cancel = st.columns([1, 1])
                        
                        if col_save.form_submit_button("Save Changes", type="primary"):
                            update_task_details(task['id'], {
                                "summary": new_summary,
                                "project_id": new_project,
                                "assignee": new_assignee,
                                "deadline": new_deadline
                            })
                            st.session_state[edit_key] = False
                            st.rerun()
                            
                        # Note: 'Cancel' button inside a form behaves like submit. 
                        # We use a standard button outside or rely on form logic.
                        # For simplicity in Streamlit forms, usually just 'Save'. 
                        # If we want a cancel, we might need a workaround or just toggle state outside form.
                        # Let's add a "Stop Editing" button outside the form if needed, or just let user Save.
                        # Actually, let's keep it simple: Save updates and closes.
                    
                else:
                    # --- View Mode ---
                    st.subheader(task['summary'])
                    
                    info_cols = st.columns([3, 3, 3, 1])
                    info_cols[0].write(f"**Project:** {task['project_id']}")
                    info_cols[1].write(f"**Assignee:** {task['assignee']}")
                    info_cols[2].write(f"**Due:** {task['deadline']}")
                    
                    if info_cols[3].button("✏️", key=f"edit_btn_{task['id']}"):
                        st.session_state[edit_key] = True
                        st.rerun()
                    
                    st.caption(f"Source: {task['source_file']}")