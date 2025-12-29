import streamlit as st
import pandas as pd
from frontend.services.api_client import fetch_tasks, update_task_details, archive_task, fetch_projects, fetch_team

def render_active_view():
    st.header("Active Tasks (Execution)")
    
    tasks = fetch_tasks("APPROVED")
    
    if not tasks:
        st.info("No active tasks.")
        return

    # --- Part 1: Task Table ---
    st.subheader("Overview")
    
    # Create DataFrame for display
    df = pd.DataFrame(tasks)
    
    # Select columns to display
    display_df = df[['id', 'summary', 'project_id', 'assignee', 'deadline']].copy()
    display_df.rename(columns={
        'id': 'ID',
        'summary': 'Summary',
        'project_id': 'Project',
        'assignee': 'Assignee',
        'deadline': 'Due Date'
    }, inplace=True)

    # Use session state to track selection
    if "selected_task_id" not in st.session_state:
        st.session_state["selected_task_id"] = None

    # Use dataframe with selection
    # Note: selection_mode="single-row" is available in newer Streamlit versions.
    event = st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun"
    )

    # Handle selection
    selected_rows = event.selection.rows
    if selected_rows:
        index = selected_rows[0]
        selected_task_id = display_df.iloc[index]['ID']
        st.session_state["selected_task_id"] = selected_task_id
    
    # --- Part 2: Detail/Edit View ---
    st.divider()
    
    if st.session_state["selected_task_id"]:
        # Find the full task object
        selected_task = next((t for t in tasks if t['id'] == st.session_state["selected_task_id"]), None)
        
        if selected_task:
            st.subheader(f"Editing: {selected_task['summary']}")
            
            # Load options
            projects = fetch_projects()
            team = fetch_team()
            project_options = [p['id'] for p in projects]
            assignee_options = [t['name'] for t in team]

            with st.container(border=True):
                # Actions Bar
                c_done, c_space = st.columns([1, 5])
                with c_done:
                    if st.button("✅ Mark as Complete", type="primary"):
                        archive_task(selected_task['id'])
                        st.session_state["selected_task_id"] = None
                        st.rerun()

                with st.form(key="edit_task_form"):
                    new_summary = st.text_input("Summary", value=selected_task['summary'])
                    
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        # Handle case where current value isn't in options
                        curr_proj = selected_task['project_id']
                        p_idx = project_options.index(curr_proj) if curr_proj in project_options else 0
                        new_project = st.selectbox("Project", project_options, index=p_idx)
                        
                    with c2:
                        curr_assignee = selected_task['assignee']
                        a_idx = assignee_options.index(curr_assignee) if curr_assignee in assignee_options else 0
                        new_assignee = st.selectbox("Assignee", assignee_options, index=a_idx)
                        
                    with c3:
                        new_deadline = st.text_input("Deadline", value=selected_task['deadline'])
                    
                    st.text_area("AI Reasoning / Notes", value=selected_task.get('reasoning', ''), disabled=True)
                    st.caption(f"Source File: {selected_task['source_file']}")

                    if st.form_submit_button("Save Changes"):
                        update_task_details(selected_task['id'], {
                            "summary": new_summary,
                            "project_id": new_project,
                            "assignee": new_assignee,
                            "deadline": new_deadline
                        })
                        st.success("Task updated successfully!")
                        st.rerun()
        else:
            st.info("Selected task not found (it might have been completed).")
    else:
        st.info("Select a task from the table above to view details and edit.")
