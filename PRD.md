Here is the consolidated, final **Product Requirements Document (PRD v7)** for your application.

This document unifies every feature we discussed: PydanticAI integration, Multi-Project Routing, Deadline Extraction, and the full "Pending → Active → Complete" lifecycle with Edit capabilities, tailored for **Civil Engineering Design Consultants**.

---

# Product Requirements Document (PRD)

**Project Name:** AI Sentinel (Design Office Task Manager)
**Version:** 7.0 (Final)
**Platform:** Local Desktop (Python)

## 1. Executive Summary

**AI Sentinel** is a privacy-first, local automation tool for **Civil Engineering Design Firms**. It eliminates manual data entry by "watching" a folder for incoming emails, RFIs, and design instructions.

When a file is detected, an AI Agent analyzes the content, cross-references it with your **Active Design Projects** and **Engineering Discipline Leads**, and proposes a structured task. The user reviews these proposals in a local dashboard, where they can edit details, approve them for execution, and eventually mark them as complete.

## 2. User Workflow

The system operates in three distinct stages:

1.  **Ingestion (The Sentinel):**
    *   User drags an email or text file (`.msg`, `.eml`, `.txt`)—containing Client Briefs, RFIs, or Design Feedback—into the `/inbox` folder.
    *   System automatically detects the file, parses it, and runs AI analysis.
    *   Status: **PENDING** (Draft).

2.  **Triage (The Dashboard):**
    *   User opens the "Inbox" view.
    *   User sees the AI's proposed Project (e.g., "BRIDGE-01"), Assignee (e.g., "Senior Structural Eng."), Deadline, and Reasoning.
    *   User can Edit any field or click "Approve".
    *   Status: **APPROVED** (Active).

3.  **Execution (The Work):**
    *   User views the "Active Tasks" list (e.g., "Update Pier Calculations", "Review Rebar Detailing").
    *   User can Edit task details (if design criteria change) using the ✏️ button.
    *   User marks the task as done via a checkbox.
    *   Status: **COMPLETED** (Archived).

---

## 3. Functional Requirements

### 3.1 The Sentinel (Backend Service)

*   **File Watching:** Must monitor `./inbox` for new files recursively.
*   **Context Loading:** Must load `projects.json` (Design Contracts) and `team.json` (Design Team) before every analysis.
*   **AI Processing (PydanticAI + Ollama):**
    *   **Local Inference:** Must use a local **Ollama** instance (e.g., running `llama3` or `mistral`) instead of cloud APIs for data privacy.
    *   **Project filtering:** Must only assign tasks to team members who are explicitly listed as working on that specific **Project ID** in `team.json`.
    *   **Extraction:**
        *   Extract a **10-20 word summary**.
        *   Extract **Deadlines** (converting relative dates to `YYYY-MM-DD`).
        *   Provide **Reasoning** based on technical discipline and project assignment.
*   **Safety:** If AI fails, create a task with "Manual Review Needed".

### 3.2 The Dashboard (Frontend UI)

*   **Inbox Section:**
    *   Display "Reasoning" as a caption to help the user trust the AI's routing logic.
    *   Allow immediate modification of Project/Assignee before approval.
*   **Active Section:**
    *   **Edit Mode:** Clicking an "Edit" button transforms the row into input fields to update Summary, Deadline, or Assignee.
    *   **Completion:** A checkbox that immediately moves the task to history.
*   **History Section:**
    *   Read-only view of completed tasks with an "Undo" button.

### 3.3 Data Management

*   **Storage:** Local SQLite database (`tasks.db`) located in `/data`.
*   **File Handling:** After processing, source files must be moved from `/inbox` to `/processed`.
*   **Renaming Strategy:** To maintain traceability for ISO 9001 audits, the source file must be renamed to `[Project_ID]-#[Task_ID].[ext]` (e.g., `SB-01-#42.msg`) before archiving.

---

## 4. Technical Specifications

### 4.1 Tech Stack

*   **Language:** Python 3.9+
*   **Package Manager:** `uv` (Required for virtual environment management).
*   **File System:** `watchdog` library.
*   **Parsing Libraries:** `extract-msg` (for Outlook), `email` (standard lib for .eml).
*   **AI Engine:** `pydantic-ai` (configured for **Local Ollama**).
*   **Database:** `sqlite3` (Standard library).
*   **UI Framework:** `streamlit`.

### 4.2 Database Schema

Table Name: `tasks`

| Column | Type | Description |
| --- | --- | --- |
| `id` | INTEGER PK | Unique ID. |
| `source_file` | TEXT | Filename of the dropped email/file. |
| `original_subject` | TEXT | Email subject line or file content header. |
| `summary` | TEXT | **AI Generated:** Action-oriented design task. |
| `deadline` | TEXT | **AI Extracted:** ISO Date or "None". |
| `project_id` | TEXT | **AI Matched:** Project ID (e.g., "SB-01"). |
| `assignee` | TEXT | **AI Matched:** Design Engineer Name. |
| `reasoning` | TEXT | **AI Generated:** Why this discipline/project? |
| `status` | TEXT | `PENDING`, `APPROVED`, or `COMPLETED`. |

---

## 5. Directory Structure

The project is structured with a modular architecture to support future scaling (e.g., replacing Streamlit with React, or scaling the AI service independently).

```text
/AI_Sentinel
│
├── /backend
│   ├── main.py                # [ENTRY POINT] Starts the watcher service
│   ├── /core
│   │   ├── watcher.py         # File system event handling logic
│   │   └── orchestration.py   # Coordinates AI, DB, and File Ops
│   ├── /services
│   │   ├── ai_service.py      # PydanticAI + Ollama implementation
│   │   └── db_service.py      # Database CRUD operations
│   └── /utils
│       ├── config.py          # Loads projects.json and team.json
│       └── file_ops.py        # Safe file moving and renaming
│
├── /frontend
│   ├── app.py                 # [ENTRY POINT] Streamlit Main Application
│   ├── /components
│   │   ├── inbox_view.py      # UI for Pending tasks
│   │   ├── active_view.py     # UI for Active tasks
│   │   └── history_view.py    # UI for Archived tasks
│   └── /services
│       └── api_client.py      # Interface for Frontend to read DB/Config
│
├── /inbox                     # Drop emails (.msg, .eml) or .txt here
├── /processed                 # Files moved here after AI reads them
│
├── /data
│   ├── projects.json          # Configuration (Design Projects with IDs)
│   ├── team.json              # Configuration (Engineers & Project Assignments)
│   └── tasks.db               # Auto-generated Database
│
├── requirements.txt           # Dependencies
```

## 6. Configuration Files (Templates)

**`/data/projects.json`**

```json
{
  "projects": [
    { 
      "id": "SB-01", 
      "name": "Suspension Bridge Feasibility", 
      "context": "Preliminary design phase, focus on cable anchorage and pylon aesthetics." 
    },
    { 
      "id": "DDU-99", 
      "name": "Downtown Drainage Upgrade", 
      "context": "Hydraulic modeling and stormwater pipe sizing for City Center." 
    }
  ]
}
```

**`/data/team.json`**

```json
{
  "team": [
    { 
      "name": "Alice", 
      "role": "Senior Structural Engineer", 
      "duties": ["Finite Element Analysis", "Code Compliance", "Steel Design"],
      "projects": ["SB-01"]
    },
    { 
      "name": "Bob", 
      "role": "Civil/Hydraulic Engineer", 
      "duties": ["Stormwater Modeling", "Grading Plans", "Utility Coordination"],
      "projects": ["DDU-99"] 
    },
    { 
      "name": "Charlie", 
      "role": "CAD/BIM Manager", 
      "duties": ["Drawing Standards", "Clash Detection", "Revit/Civil3D Model Management"],
      "projects": ["SB-01", "DDU-99"]
    }
  ]
}
```

## 7. Next Steps (Implementation Order)

1.  **Environment Setup:**
    *   Install `uv`.
    *   Initialize: `uv venv .venv`.
    *   Install dependencies (including `extract-msg`).
    *   **Ollama:** Ensure `llama3` model is pulled and running.
2.  **Scaffolding:** Create the directory tree exactly as shown in Section 5.
3.  **Backend Implementation:**
    *   Implement `utils/config.py` first to ensure context loading works.
    *   Build `services/ai_service.py` to test Ollama connectivity.
    *   Wire it all together in `main.py` with parsing logic for `.msg`/`.eml`.
4.  **Frontend Implementation:**
    *   Build `services/api_client.py` to read the shared database.
    *   Create the UI components in `components/`.
    *   Launch the UI via `streamlit run frontend/app.py`.