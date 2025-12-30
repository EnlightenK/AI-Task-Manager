import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure backend is in path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.services.db_service import get_tasks, update_task, delete_task as db_delete_task
from backend.utils.config import load_projects, load_team, save_projects as db_save_projects, save_team as db_save_team

def fetch_tasks(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetches tasks from the database, optionally filtering by status.
    """
    return get_tasks(status)

def update_task_details(task_id: int, updates: Dict[str, Any]):
    """
    Updates a task with new details.
    """
    update_task(task_id, updates)

def archive_task(task_id: int):
    """
    Moves a task to COMPLETED status.
    """
    update_task(task_id, {"status": "COMPLETED"})

def approve_task(task_id: int, updates: Optional[Dict[str, Any]] = None):
    """
    Moves a task to APPROVED status, optionally applying updates first.
    """
    if updates:
        update_task(task_id, updates)
    update_task(task_id, {"status": "APPROVED"})

def reject_task(task_id: int):
    """
    Permanently deletes a task.
    """
    db_delete_task(task_id)

def fetch_projects() -> List[Dict[str, Any]]:
    """
    Fetches the list of active projects.
    """
    return load_projects()

def update_projects(projects: List[Dict[str, Any]]):
    """
    Saves the list of projects.
    """
    db_save_projects(projects)

def fetch_team() -> List[Dict[str, Any]]:
    """
    Fetches the list of team members.
    """
    return load_team()

def update_team(team: List[Dict[str, Any]]):
    """
    Saves the list of team members.
    """
    db_save_team(team)