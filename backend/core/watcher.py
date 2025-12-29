import time
import logging
import asyncio
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.core.orchestration import process_file

# Setup logging
logger = logging.getLogger(__name__)

class InboxHandler(FileSystemEventHandler):
    """
    Handles file creation events in the inbox directory.
    """
    def __init__(self, loop):
        self.loop = loop

    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        logger.info(f"New file detected: {file_path}")
        
        # We need to wait a brief moment to ensure the file is fully written (especially for large files)
        # However, blocking here stops the observer.
        # Since process_file is async, we schedule it on the event loop.
        asyncio.run_coroutine_threadsafe(self._process_with_delay(file_path), self.loop)

    async def _process_with_delay(self, file_path: Path):
        """Wait for file write to complete then process."""
        await asyncio.sleep(1) # Simple debounce/wait for write
        await process_file(file_path)

def start_watcher(inbox_path: Path, loop: asyncio.AbstractEventLoop) -> Observer:
    """
    Starts the watchdog observer on the inbox directory.
    Returns the observer instance.
    """
    if not inbox_path.exists():
        inbox_path.mkdir(parents=True, exist_ok=True)
        
    event_handler = InboxHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, str(inbox_path), recursive=True)
    observer.start()
    logger.info(f"Watcher started on: {inbox_path}")
    return observer