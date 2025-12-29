import logging
import shutil
from pathlib import Path
import extract_msg
import email
from email import policy
import codecs
from backend.services.ai_service import analyze_content
from backend.services.db_service import create_task
from backend.utils.file_ops import move_to_processed
from backend.utils.config import PROCESSED_DIR, STAGING_DIR

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
                raw_data = f.read()
            
            # Remove UTF-8 BOM if present
            if raw_data.startswith(codecs.BOM_UTF8):
                raw_data = raw_data[len(codecs.BOM_UTF8):]

            msg = email.message_from_bytes(raw_data, policy=policy.default)
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
    1. Move to Staging (Atomic Claim)
    2. Extract content
    3. AI Analysis
    4. DB Insertion
    5. File Movement to Processed
    """
    if not file_path.exists():
        logger.warning(f"File not found (race condition): {file_path}")
        return

    # Ensure staging directory exists
    STAGING_DIR.mkdir(exist_ok=True)
    
    # 1. Move to Staging
    try:
        staging_path = STAGING_DIR / file_path.name
        # If file already exists in staging, append timestamp or unique ID, but for now overwrite or skip
        # shutil.move will fail if dest exists on some OS, or overwrite. 
        # Ideally we want unique names.
        if staging_path.exists():
            import uuid
            staging_path = STAGING_DIR / f"{file_path.stem}_{uuid.uuid4().hex[:6]}{file_path.suffix}"
            
        shutil.move(str(file_path), str(staging_path))
        logger.info(f"Moved {file_path.name} to staging: {staging_path}")
    except Exception as e:
        logger.error(f"Failed to move to staging (race condition lost?): {e}")
        return

    # From now on, use staging_path
    
    # 2. Extract Content
    subject, content = extract_content(staging_path)
    if not content:
        logger.warning(f"No content extracted from {staging_path}. Skipping.")
        return

    # 3. AI Analysis
    logger.info("Running AI analysis...")
    try:
        analysis = await analyze_content(content)
    except Exception as e:
        logger.error(f"AI Analysis failed for {staging_path}: {e}")
        # Consider moving to an 'error' folder?
        return
    
    # 4. DB Insertion
    logger.info("Saving to database...")
    try:
        # Convert datetime to string for SQLite
        deadline_str = analysis.deadline.strftime("%Y-%m-%d") if analysis.deadline else "None"
        
        task_id = create_task(
            source_file=file_path.name, # Keep original name for record
            original_subject=subject,
            summary=analysis.title,
            deadline=deadline_str,
            project_id=analysis.project_id,
            assignee=analysis.assigned_to,
            reasoning=f"{analysis.description}\n(Confidence: {analysis.confidence:.2f})",
            status="PENDING"
        )
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")
        return
    
    # 5. File Movement
    logger.info(f"Moving file (Task ID: {task_id})...")
    try:
        # Move from STAGING to PROCESSED
        new_path = move_to_processed(staging_path, PROCESSED_DIR, analysis.project_id, task_id)
        logger.info(f"File processed and moved to: {new_path}")
    except Exception as e:
        logger.error(f"Failed to move file: {e}")
