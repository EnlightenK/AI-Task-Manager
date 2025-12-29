import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path to ensure imports work correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.utils.config import INBOX_DIR
from backend.services.db_service import init_db
from backend.core.watcher import start_watcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting AI Sentinel Backend Service...")
    
    # 1. Initialize Database
    init_db()
    logger.info("Database initialized.")

    # 2. Start Watcher
    loop = asyncio.get_running_loop()
    observer = start_watcher(INBOX_DIR, loop)
    
    # 3. Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logger.info("Stopping service...")
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass