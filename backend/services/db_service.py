import sqlite3
from typing import List, Dict, Optional, Any
from backend.utils.config import DATA_DIR

DB_PATH = DATA_DIR / "tasks.db"

def init_db():
    """Initializes the database table if it doesn't exist."""
    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            original_subject TEXT,
            summary TEXT,
            deadline TEXT,
            project_id TEXT,
            assignee TEXT,
            reasoning TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_task(source_file: str, original_subject: str, summary: str, 
                deadline: str, project_id: str, assignee: str, reasoning: str, 
                status: str = "PENDING") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (source_file, original_subject, summary, deadline, project_id, assignee, reasoning, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (source_file, original_subject, summary, deadline, project_id, assignee, reasoning, status))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    if task_id is None:
        raise ValueError("Failed to retrieve task ID after insertion")
    return task_id

def get_tasks(status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if status:
        cursor.execute("SELECT * FROM tasks WHERE status = ? ORDER BY id DESC", (status,))
    else:
        cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_task(task_id: int, updates: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    
    if not updates:
        conn.close()
        return

    set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
    values = list(updates.values())
    values.append(task_id)
    
    cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    """Delete a task (mostly for testing or cleanup if needed)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()