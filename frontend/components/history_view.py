import streamlit as st
import pandas as pd
from frontend.services.api_client import fetch_tasks, update_task_details

def render_history_view():
    st.header("History (Archived)")
    
    tasks = fetch_tasks("COMPLETED")
    
    if not tasks:
        st.info("No archived tasks found.")
        return

    # Create DataFrame for display
    df = pd.DataFrame(tasks)
    
    # Select columns to display
    display_df = df[['id', 'summary', 'project_id', 'assignee', 'deadline', 'source_file']].copy()
    display_df.rename(columns={
        'id': 'ID',
        'summary': 'Summary',
        'project_id': 'Project',
        'assignee': 'Assignee',
        'deadline': 'Due Date',
        'source_file': 'Source File'
    }, inplace=True)

    # Use session state to track selection if we want to add "Undo" functionality via selection
    # For history, maybe just a table is fine, but "Undo" is useful.
    # Let's use the same pattern: Table -> Detail/Action
    
    if "hist_selected_task_id" not in st.session_state:
        st.session_state["hist_selected_task_id"] = None

    event = st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun"
    )

    selected_rows = event.selection.rows
    if selected_rows:
        index = selected_rows[0]
        selected_task_id = display_df.iloc[index]['ID']
        st.session_state["hist_selected_task_id"] = selected_task_id

    st.divider()

    if st.session_state["hist_selected_task_id"]:
        selected_task = next((t for t in tasks if t['id'] == st.session_state["hist_selected_task_id"]), None)
        
        if selected_task:
            st.subheader(f"Details: {selected_task['summary']}")
            with st.container(border=True):
                st.write(f"**Project:** {selected_task['project_id']}")
                st.write(f"**Assignee:** {selected_task['assignee']}")
                st.write(f"**Due Date:** {selected_task['deadline']}")
                st.write(f"**Source File:** {selected_task['source_file']}")
                
                if st.button("↩️ Undo (Move to Active)", key="undo_btn"):
                    update_task_details(selected_task['id'], {"status": "APPROVED"})
                    st.session_state["hist_selected_task_id"] = None
                    st.success("Task moved back to Active.")
                    st.rerun()
        else:
            st.info("Selected task not found.")
    else:
        st.info("Select a task to view details or undo archival.")
