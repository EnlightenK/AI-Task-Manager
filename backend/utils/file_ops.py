import shutil
from pathlib import Path
import logging

def move_to_processed(source_path: Path, processed_dir: Path, project_id: str, task_id: int) -> Path:
    """
    Moves a file from inbox to processed directory with ISO 9001 compliant renaming.
    Format: [Project_ID]-#[Task_ID].[ext]
    
    Args:
        source_path: Path to the original file in inbox.
        processed_dir: Directory to move the file to.
        project_id: The ID of the project (e.g., 'SB-01').
        task_id: The unique ID of the task from the database.
        
    Returns:
        Path: The new path of the moved/renamed file.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    if not processed_dir.exists():
        processed_dir.mkdir(parents=True, exist_ok=True)

    # Handle cases where project_id might be None (e.g. AI failed)
    safe_project_id = project_id if project_id else "UNKNOWN"
    
    # Clean project_id to ensure it's filename safe (basic check)
    safe_project_id = "".join(c for c in safe_project_id if c.isalnum() or c in ('-', '_'))

    # Extract extension
    suffix = source_path.suffix
    
    # Construct new filename
    new_filename = f"{safe_project_id}-#{task_id}{suffix}"
    destination_path = processed_dir / new_filename

    try:
        shutil.move(str(source_path), str(destination_path))
        logging.info(f"Moved and renamed file to: {destination_path}")
        return destination_path
    except Exception as e:
        logging.error(f"Failed to move file {source_path} to {destination_path}: {e}")
        raise e