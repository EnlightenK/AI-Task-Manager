import streamlit as st
from frontend.services.api_client import fetch_tasks, approve_task, fetch_projects, fetch_team, update_task_details, reject_task

def render_inbox_view():
    st.header("Inbox (Pending Triage)")
    
    tasks = fetch_tasks("PENDING")
    
    if not tasks:
        st.info("No pending tasks in the inbox.")
        return

    # Load options for dropdowns
    projects = fetch_projects()
    team = fetch_team()
    
    project_options = [p['id'] for p in projects]
    assignee_options = [t['name'] for t in team]

    for task in tasks:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"📄 {task['original_subject']}")
                st.caption(f"Source: {task['source_file']}")
                st.write(f"**AI Reasoning:** {task['reasoning']}")
                
                # Edit Fields
                c1, c2, c3 = st.columns(3)
                with c1:
                    new_project = st.selectbox(
                        "Project", 
                        options=project_options, 
                        index=project_options.index(task['project_id']) if task['project_id'] in project_options else 0,
                        key=f"proj_{task['id']}"
                    )
                with c2:
                    new_assignee = st.selectbox(
                        "Assignee", 
                        options=assignee_options, 
                        index=assignee_options.index(task['assignee']) if task['assignee'] in assignee_options else 0,
                        key=f"assign_{task['id']}"
                    )
                with c3:
                    new_deadline = st.text_input(
                        "Deadline", 
                        value=task['deadline'],
                        key=f"dead_{task['id']}"
                    )
                
                # Update Summary
                new_summary = st.text_area(
                    "Task Summary", 
                    value=task['summary'], 
                    key=f"sum_{task['id']}"
                )

            with col2:
                st.write("Actions")
                col_approve, col_reject = st.columns(2)
                with col_approve:
                    if st.button("Approve", key=f"btn_approve_{task['id']}", type="primary"):
                        updates = {
                            "project_id": new_project,
                            "assignee": new_assignee,
                            "deadline": new_deadline,
                            "summary": new_summary
                        }
                        approve_task(task['id'], updates)
                        st.rerun()
                
                with col_reject:
                    if st.button("Reject", key=f"btn_reject_{task['id']}", type="secondary"):
                        reject_task(task['id'])
                        st.rerun()