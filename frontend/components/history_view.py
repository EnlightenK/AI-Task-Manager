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

    # --- Filters ---
    with st.expander("🔍 Filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            search_query = st.text_input("Search History", placeholder="Type summary or source...").lower()
        with c2:
            unique_projects = ["All"] + sorted(display_df['Project'].unique().tolist())
            selected_project = st.selectbox("Filter by Project", unique_projects, key="hist_proj")
        with c3:
            unique_assignees = ["All"] + sorted(display_df['Assignee'].unique().tolist())
            selected_assignee = st.selectbox("Filter by Assignee", unique_assignees, key="hist_assign")

    # Apply Filters
    filtered_df = display_df.copy()
    
    if search_query:
        # Search in Summary OR Source File
        filtered_df = filtered_df[
            filtered_df['Summary'].str.lower().str.contains(search_query) | 
            filtered_df['Source File'].str.lower().str.contains(search_query)
        ]
        
    if selected_project != "All":
        filtered_df = filtered_df[filtered_df['Project'] == selected_project]
        
    if selected_assignee != "All":
        filtered_df = filtered_df[filtered_df['Assignee'] == selected_assignee]

    if "hist_selected_task_id" not in st.session_state:
        st.session_state["hist_selected_task_id"] = None

    event = st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        selection_mode="single-row",
        on_select="rerun"
    )

    selected_rows = event.selection.rows
    if selected_rows:
        index = selected_rows[0]
        selected_task_id = filtered_df.iloc[index]['ID']
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
                st.write(f"**AI Reasoning:** {selected_task.get('reasoning', 'N/A')}")
                
                if st.button("↩️ Undo (Move to Active)", key="undo_btn"):
                    update_task_details(selected_task['id'], {"status": "APPROVED"})
                    st.session_state["hist_selected_task_id"] = None
                    st.success("Task moved back to Active.")
                    st.rerun()
        else:
            st.info("Selected task not found.")
    elif filtered_df.empty:
        st.warning("No history items match the selected filters.")
    else:
        st.info("Select a task to view details or undo archival.")