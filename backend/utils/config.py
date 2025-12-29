import json
import os
from pathlib import Path

# Define base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INBOX_DIR = BASE_DIR / "inbox"
PROCESSED_DIR = BASE_DIR / "processed"

PROJECTS_FILE = DATA_DIR / "projects.json"
TEAM_FILE = DATA_DIR / "team.json"

def load_projects():
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

def load_team():
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