import json
import os
from pathlib import Path
from typing import List, Dict, Any

# Define base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INBOX_DIR = BASE_DIR / "inbox"
STAGING_DIR = BASE_DIR / "staging"
PROCESSED_DIR = BASE_DIR / "processed"

PROJECTS_FILE = DATA_DIR / "projects.json"
TEAM_FILE = DATA_DIR / "team.json"

def load_projects() -> List[Dict[str, Any]]:
    """Loads projects from data/projects.json"""
    if not PROJECTS_FILE.exists():
        return []
    try:
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("projects", [])
    except Exception as e:
        print(f"Error loading projects: {e}")
        return []

def save_projects(projects: List[Dict[str, Any]]):
    """Saves projects to data/projects.json"""
    try:
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"projects": projects}, f, indent=4)
    except Exception as e:
        print(f"Error saving projects: {e}")
        raise e

def load_team() -> List[Dict[str, Any]]:
    """Loads team members from data/team.json"""
    if not TEAM_FILE.exists():
        return []
    try:
        with open(TEAM_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("team", [])
    except Exception as e:
        print(f"Error loading team: {e}")
        return []

def save_team(team: List[Dict[str, Any]]):
    """Saves team members to data/team.json"""
    try:
        with open(TEAM_FILE, 'w', encoding='utf-8') as f:
            json.dump({"team": team}, f, indent=4)
    except Exception as e:
        print(f"Error saving team: {e}")
        raise e
