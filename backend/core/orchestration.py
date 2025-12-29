import logging
from pathlib import Path
import extract_msg
import email
from email import policy
from backend.services.ai_service import analyze_content
from backend.services.db_service import create_task
from backend.utils.file_ops import move_to_processed
from backend.utils.config import PROCESSED_DIR

# Setup logging
logger = logging.getLogger(__name__)

def extract_content(file_path: Path) -> tuple[str, str]:
    """
    Extracts subject and body from .txt, .msg, or .eml files.
    Returns: (subject, body)
    """
    try:
        if file_path.suffix.lower() == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                return file_path.name, content
        
        elif file_path.suffix.lower() == '.msg':
            # extract_msg requires string path
            msg = extract_msg.Message(str(file_path))
            subject = msg.subject if msg.subject else file_path.name
            body = msg.body if msg.body else ""
            msg.close()
            return subject, body
            
        elif file_path.suffix.lower() == '.eml':
            with open(file_path, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=policy.default)
                subject = msg['subject'] or file_path.name
                body_part = msg.get_body(preferencelist=('plain', 'html'))
                body = body_part.get_content() if body_part else ""
                return subject, body
        else:
            return file_path.name, f"Unsupported file type: {file_path.suffix}"
            
    except Exception as e:
        logger.error(f"Error extracting from {file_path}: {e}")
        return file_path.name, ""

async def process_file(file_path: Path):
    """
    Orchestrates the processing of a single file:
    1. Extract content
    2. AI Analysis
    3. DB Insertion
    4. File Movement
    """
    logger.info(f"Processing file: {file_path}")
    
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return

    # 1. Extract Content
    subject, content = extract_content(file_path)
    if not content:
        logger.warning(f"No content extracted from {file_path}. Skipping.")
        return

    # 2. AI Analysis
    logger.info("Running AI analysis...")
    analysis = await analyze_content(content)
    
    # 3. DB Insertion
    logger.info("Saving to database...")
    try:
        task_id = create_task(
            source_file=file_path.name,
            original_subject=subject,
            summary=analysis.summary,
            deadline=analysis.deadline,
            project_id=analysis.project_id,
            assignee=analysis.assignee,
            reasoning=analysis.reasoning,
            status="PENDING"
        )
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        return
    
    # 4. File Movement
    logger.info(f"Moving file (Task ID: {task_id})...")
    try:
        new_path = move_to_processed(file_path, PROCESSED_DIR, analysis.project_id, task_id)
        logger.info(f"File processed and moved to: {new_path}")
    except Exception as e:
        logger.error(f"Failed to move file: {e}")