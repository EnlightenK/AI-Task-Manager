import asyncio
import threading
import logging
import streamlit as st
from pathlib import Path
from backend.core.watcher import start_watcher
from backend.utils.config import INBOX_DIR
from backend.services.db_service import init_db

logger = logging.getLogger(__name__)

class WatcherManager:
    def __init__(self):
        self.observer = None
        self.loop = None
        self.thread = None
        self._running = False

    def _run_event_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def start(self):
        if self._running:
            return

        # 1. Initialize DB (safe to call multiple times)
        init_db()

        # 2. Start a background thread for the asyncio loop
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
            self.thread.start()
            # Give the loop a moment to start
            import time
            time.sleep(0.5)

        # 3. Start the watchdog observer
        self.observer = start_watcher(INBOX_DIR, self.loop)
        self._running = True
        logger.info("Watcher Manager started successfully.")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self._running = False
        logger.info("Watcher Manager stopped.")

    @property
    def is_running(self):
        return self._running and self.observer and self.observer.is_alive()

@st.cache_resource
def get_watcher_manager():
    return WatcherManager()
