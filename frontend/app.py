import sys
from pathlib import Path
import streamlit as st

# Ensure backend/root is in path for imports to work
sys.path.append(str(Path(__file__).resolve().parent.parent))

from frontend.components.inbox_view import render_inbox_view
from frontend.components.active_view import render_active_view
from frontend.components.history_view import render_history_view
from frontend.services.watcher_manager import get_watcher_manager

st.set_page_config(
    page_title="AI Sentinel",
    page_icon="🏗️",
    layout="wide"
)

def main():
    st.title("🏗️ AI Sentinel: Design Office Task Manager")
    
    # Sidebar: System Status
    with st.sidebar:
        st.header("System Status")
        manager = get_watcher_manager()
        
        if manager.is_running:
            st.success("🟢 Watcher: Running")
            if st.button("Stop Watcher"):
                manager.stop()
                st.rerun()
        else:
            st.error("🔴 Watcher: Stopped")
            if st.button("Start Watcher", type="primary"):
                manager.start()
                st.rerun()
        
        st.divider()
        st.info("The watcher monitors the `inbox/` folder for new files.")

    # Simple Tab Layout
    tab1, tab2, tab3 = st.tabs(["Inbox (Triage)", "Active Tasks", "History"])
    
    with tab1:
        render_inbox_view()
        
    with tab2:
        render_active_view()
        
    with tab3:
        render_history_view()

if __name__ == "__main__":
    main()